from mysql import connector
from enum import Enum
from pathlib import Path
from typing import Generic, TypeVar, Optional, Any
from common_methods import AwsCommonMethods
from dbImxLog import LogHandler


# region ProcessingEnums
class QueryType(Enum):
    NONE = 0
    SELECT = 1
    INSERT = 2
    UPDATE = 3
    DELETE = 4


class SectionType(Enum):
    NONE = 0
    WHERE = 1
    SET = 2
    INSERT = 3


# endregion


class DbHandler:
    # region Global variables
    # Internal properties
    _conn_props: dict[str, str]
    _values_dict: dict[str, str] = {}
    _query_type: QueryType = QueryType.NONE
    _acm_handler: AwsCommonMethods

    # Global consts
    _WHERE_SECTION: SectionType = SectionType.WHERE
    _SET_SECTION: SectionType = SectionType.SET
    _INSERT_SECTION: SectionType = SectionType.INSERT
    # endregion

    # region Constructor
    def __init__(self, conn_props: dict[str, str]) -> None:
        """DbHandler Constructor

        Args:
            conn_props (dict[str, str]): Dictionary of connection properties, should contain host, database, username, and password
        """
        self._conn_props = conn_props
        logger_handler = LogHandler()
        self._db_logger = logger_handler.create_logger(
            "DbHandler", "info", useDefaultFormat=True
        )
        
        #comment to force lambda layer to actually update

    # endregion

    def update_table(
        self,
        table_name: str,
        update_values: dict[str, str],
        where_values: Optional[dict[str, str]] = None,
    ) -> tuple[int, str | list[dict[str, str]]]:
        """Method used to update SQL tables

        Args:
            table_name (str): Name of table to perform update on
            update_values (dict[str, str]): Dictionary of column names and values to be updated
            where_values (Optional[dict[str, str]], optional): Dictionary of column and values for where clause. Defaults to None.

        Returns:
            dict[str, str | int]: _description_
        """
        self._values_dict.clear()
        self._query_type = QueryType.UPDATE

        query = self.__build_query(
            table_name=table_name,
            section_values=update_values,
            where_values=where_values,
        )

        results = self.__run_query(query)

        return results

    def select_from_table(
        self,
        table_name: str,
        where_values: dict[str, str] | None = None,
        filter_columns: list[str] | None = None,
    ) -> tuple[int, str | list[dict[str, str]]]:
        """Method used to run simple SQL select query

        Args:
            table_name (str): Name of the table that the select will be run against.
            where_values (Optional[dict[str, str]], optional): The columns and values used in a where clause. Defaults to None.
            filter_columns (Optional[list[str]], optional): List of column names the SQL query should return. Defaults to None.

        Returns:
            list[dict[str,str]]: returns a list of dictionaries, each dictionary is a row and consists of string column name and a sting value
        """
        # Clear the dictionary to make sure no values are left over from previous cmd
        self._values_dict.clear()
        self._query_type = QueryType.SELECT

        # build query string and run the query
        query = self.__build_query(
            table_name=table_name,
            where_values=where_values,
            filter_columns=filter_columns,
        )
        self._db_logger.info(query)
        results = self.__run_query(query)

        return results

    def insert_into_table(
        self, table_name: str, keyword_values: dict[str, str]
    ) -> tuple[int, str | list[dict[str, str]]]:
        """Method used to create a basic instert query for sql

        Args:
            table_name (str): Name of the table that the entry will be inserted into.
            keyword_values (dict[str, str]): Dictionary of column names as key and values that will be inserted.

        Returns:
            dict[str,str]: Dictionary containing the Status Code and either the success or error message.
        """
        # Clear the dictionary and QueryType for new execution
        self._values_dict.clear()
        self._query_type = QueryType.INSERT

        # build query string and run the query
        query = self.__build_query(table_name=table_name, section_values=keyword_values)

        results = self.__run_query(query)

        return results

    def delete_from_table(
        self, table_name: str, where_values: dict[str, str]
    ) -> tuple[int, str | list[dict[str, str]]]:
        """Method to delete entry from SQL table

        Args:
            table_name (str): Name of the table the entry should be removed from.
            where_values (dict[str, str]): dictionary of the column name and value for the entry that should be removed

        Returns:
            dict[str, str]: Dictionary containing the Status Code and either the success or error message.
        """
        # Clear the dictionary and QueryType for new execution
        self._values_dict.clear()
        self._query_type = QueryType.DELETE

        # build query string and run the query
        query = self.__build_query(table_name=table_name, where_values=where_values)

        results = self.__run_query(query)

        return results

    # TODO Need to update method, currently not being used
    def execute_sql_file(self, file: str) -> tuple[int, str]:
        """Method to execute a SQL File. This method's logic is still a work in progress.

        Args:
            file (str): filePath of the SQL file to execute

        Returns:
            str | list[dict[str,str]]: _description_
        """
        res = (-2, "")

        try:
            contents = Path(file)
            with connector.connect(**self._conn_props) as conn:
                with conn.cursor() as cursor:
                    result_iterator = cursor.execute(contents.read_text(), multi=True)
                    for res in result_iterator:
                        # Will print out a short representation of the query
                        print("Running query: ", res)
                        print(f"Affected {res.rowcount} rows")

                    conn.commit()
        except connector.Error as ex:
            return (-1, f"{ex}")
        except Exception as ex:
            return (-1, f"{self._acm_handler.format_error(ex)}")  # type: ignore

        return res

    def __build_query(
        self,
        table_name,
        section_values: dict[str, str] | None = None,
        where_values: dict[str, str] | None = None,
        filter_columns: list[str] | None = None,
    ) -> str:
        # Create empty string variables for building
        query_string = ""
        where_section = ""
        
        table_name = self.__sanatize_table_columns(table_name)

        if where_values is not None and len(where_values) != 0:
            where_section = self.__build_section(where_values, self._WHERE_SECTION)

        match self._query_type:
            case QueryType.SELECT:
                filter_section = (
                    "*"
                    if filter_columns == None or len(filter_columns) == 0
                    else ",".join([self.__sanatize_table_columns(column) for column in filter_columns])
                )
                query_string = (
                    f"SELECT {filter_section} FROM {table_name} {where_section}"
                )
            case QueryType.UPDATE:
                set_section = self.__build_section(section_values, self._SET_SECTION)
                query_string = f"UPDATE {table_name} SET {set_section}{where_section}"
                self._db_logger.info(f"Update Query: {query_string}")
            case QueryType.INSERT:
                insert_section = self.__build_section(
                    section_values, self._INSERT_SECTION
                )
                query_string = f"INSERT INTO {table_name} {insert_section}"
                self._db_logger.info(f"Insert Query: {query_string}")
            case QueryType.DELETE:
                query_string = f"DELETE FROM {table_name}{where_section}"

        return query_string

    def __build_section(
        self, section_values: dict[str, str] | None, section_type: SectionType
    ) -> str:
        section = ""

        if section_values is None: return section
        
        match section_type:
            case SectionType.WHERE:
                section = " WHERE"
                for key, value in section_values.items():
                    key = self.__sanatize_table_columns(key)
                    where_key = f"where_{key}"
                    section += f" {key}=%({where_key})s AND"
                    self._values_dict[where_key] = value
                    print(f"Where section chunk: [{section}]")
                return section[:-3]
            case SectionType.SET:
                for key, value in section_values.items():
                    key = self.__sanatize_table_columns(key)
                    set_key = f"set_{key}"
                    section += f" {key}=%({set_key})s,"
                    self._values_dict[set_key] = value
                    
                return section[:-1]
            case SectionType.INSERT:
                columns_list = []
                values_list = []

                for key, value in section_values.items():
                    key = self.__sanatize_table_columns(key)
                    insert_key = f"{key}"
                    columns_list.append(insert_key)
                    values_list.append(f"%({insert_key})s")
                    self._values_dict[insert_key] = value
                    
                    print(f"Insert_key: [{key}], Insert_value: [{value}]")

                columns_string = ",".join(columns_list)
                values_string = ",".join(values_list)

                return f"({columns_string}) VALUES ({values_string})"


    def __run_query(self, query: str) -> tuple[int, str | list[dict[str, str]]]:
        results: str | list[dict[str, str]] = ""
        status = 0
        try:
            with connector.connect(**self._conn_props) as conn:
                if self._query_type == QueryType.SELECT:
                    with conn.cursor(dictionary=True, buffered=True) as cursor:
                        cursor.execute(query, self._values_dict)
                        row_count = cursor.rowcount

                        if row_count == 0:
                            results = "No records found"
                        else:
                            results = [
                                {f"{key}": f"{value}" for key, value in row.items() if value is not None}
                                for row in cursor  # type: ignore
                            ]
                else:
                    with conn.cursor() as cursor:
                        cursor.execute(query, self._values_dict)
                        results = "Update Successful"
                        conn.commit()

        except connector.Error as err:
            if err.errno == connector.errorcode.ER_ACCESS_DENIED_ERROR:  # type: ignore
                status = -1
                results = f"{err}"
            elif err.errno == connector.errorcode.ER_BAD_DB_ERROR:  # type: ignore
                status = -1
                results = f"{err}"
            else:
                status = -1
                results = f"{err}"
        self._db_logger.info(f"Status {status}")
        return (status, results)

    def __sanatize_table_columns(self, value: str):
        """Sanatizese the table name and column values that are pulled in from the .env file"""
        sanatized_value = ""
        bad_characters = ("%", "\\", "@", ";", "'", '"', "`")
        sanatized_value = "".join([ch for ch in value if ch not in bad_characters])
        return sanatized_value
