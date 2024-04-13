import pymssql
from dbImxLog import LogHandler
from enum import Enum
from pathlib import Path
from typing import TypeVar, Any, Optional

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

class DbHandler:
    results_data = TypeVar("results_data")
    formatted_results = TypeVar("formatted_results")

    # Internal properties
    _conn_props: dict[str, str]
    _values_dict: dict[str, str] = {}
    _query_type: QueryType = QueryType.NONE

    # Global consts
    _WHERE_SECTION: SectionType = SectionType.WHERE
    _SET_SECTION: SectionType = SectionType.SET
    _INSERT_SECTION: SectionType = SectionType.INSERT

    # Constructor
    def __init__(self, conn_props) -> None:
        self._conn_props = conn_props
        logger_handler = LogHandler()
        self._db_logger = logger_handler.create_logger(
            "DbHandler", "info", useDefaultFormat=True
        )

    # region Simple Query Methods
    def update_table(
        self,
        table_name: str,
        update_values: dict[str, str],
        where_values: dict[str, str] | None = None,
    ) -> tuple[int, list[dict[str, str]] | str]:
        """Method used to update SQL tables

        Args:
            table_name (str): Name of table to perform update on
            update_values (dict[str, str]): Dictionary of column names and values to be updated
            where_values (dict[str, str] | None, optional): Dictionary of column and values for where clause. Defaults to None.

        Returns:
            bool: _description_
        """
        self._values_dict.clear()
        self._query_type = QueryType.UPDATE
        
        print(f"Update Values: {update_values}")
        
        query = self.__build_query(
            table_name=table_name,
            section_values=update_values,
            where_values=where_values,
        )
        
        print(query)
        print(self._values_dict)

        results = self.__run_query(query)

        return results

    def select_from_table(
        self,
        table_name: str,
        where_values: dict[str, str] | None = None,
        filter_columns: list[str] | None = None,
    ) -> tuple[int, list[dict[str, str]] | str]:
        # Clear the dictionary to make sure no values are left over from previous cmd
        self._values_dict.clear()
        self._query_type = QueryType.SELECT

        # build query string and run the query
        query = self.__build_query(
            table_name=table_name,
            where_values=where_values,
            filter_columns=filter_columns,
        )
        
        print(query)
        print(self._values_dict)

        results = self.__run_query(query)

        return results

    def insert_into_table(self, table_name: str, keyword_values: dict[str, str]) -> tuple[int, list[dict[str, str]] | str]:
        # Clear the dictionary and QueryType for new execution
        self._values_dict.clear()
        self._query_type = QueryType.INSERT

        # build query string and run the query
        query = self.__build_query(table_name=table_name, section_values=keyword_values)
        
        print(query)
        print(self._values_dict)

        results = self.__run_query(query)
        return results

    def delete_from_table(
        self, table_name: str, where_values: dict[str, str]
    ) -> tuple[int, list[dict[str, str]] | str]:
        # Clear the dictionary and QueryType for new execution
        self._values_dict.clear()
        self._query_type = QueryType.DELETE

        # build query string and run the query
        query = self.__build_query(table_name=table_name, where_values=where_values)

        results = self.__run_query(query)

        return results

    # endregion

    # region Public Execute Methods
    def execute_sql_file(
        self, file: str
    ) -> Optional[tuple[int, str | list[dict[str, str]]]]:
        try:
            contents = Path(file)
            with pymssql.connect(**self._conn_props) as conn:  # type: ignore
                with conn.cursor() as cursor:
                    result_iterator = cursor.execute(contents.read_text(), multi=True)
                    for res in result_iterator:
                        # Will print out a short representation of the query
                        print("Running query: ", res)
                        print(f"Affected {res.rowcount} rows")

                    conn.commit()
        except pymssql.Error as ex:  # type: ignore
            return (-1, f"{ex}")

    #TODO: TA - This needs to be reworked so that the image can be loaded,
    #? 
    def execute_stored_procedure(self, procedure_name: str, params: dict[str, Any] | None) -> Optional[tuple[int, str | list[dict[str, str]]]]:
        try:
            results = ""
            status = 0
            
            if params is None or not isinstance(params, dict):
                return (-1, "Error: Please check the passed parameters")
            with pymssql.connect(**self._conn_props) as conn:  # type: ignore
                with conn.cursor() as cursor:
                    cmd_params = (f"{params[param]}" for param in params)

                    cursor.callproc(procedure_name, cmd_params) if params is not None and len(params) > 0 else cursor.callproc(procedure_name)
                    results = cursor.fetchone()
                    #results = "No records found" if row_count == 0 else cursor.fetchone() 

                    conn.commit()
        except Exception as ex:
            print(f"Exception Type: {type(ex)}")
            status = -1
            results = f"{ex}"
        return (status, results)
    
    def execute_stored_procedure_json(self, procedure_name: str, params: dict[str, Any] | None) -> Optional[tuple[int, str | list[dict[str, str]]]]:
        results = ""
        status = 0
        try:
            if params is None or not isinstance(params, dict):
                return (-1, "Error: Please check the passed parameters")
            with pymssql.connect(**self._conn_props) as conn:  # type: ignore
                with conn.cursor() as cursor:
                    
                    cmd_params = (f"{params[param]}" for param in params)
                    cursor.callproc(procedure_name, cmd_params) if params is not None and len(params) > 0 else cursor.callproc(procedure_name)
                    
                    key = ""
                    json_string = ""
                    
                    for row in cursor:
                        if len(row) == 2:
                            key = row[0]
                            json_string = fr"{json_string}{row[1]}"
                        elif len(row) == 1:
                            json_string = fr"{json_string}{row[0]}"
                    
                    results = {key: [json_string]} if key != "" else [json_string]
                    conn.commit()
        except Exception as ex:
            print(f"Exception Type: {type(ex)}")
            status = -1
            results = f"{ex}"
        return (status, results)

    # endregion

    # region Internal methods for simple queries
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

        if where_values != None and len(where_values) != 0:
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
            case QueryType.INSERT:
                insert_section = self.__build_section(
                    section_values, self._INSERT_SECTION
                )
                query_string = f"INSERT INTO {table_name} {insert_section}"
                self._db_logger.info(query_string)
            case QueryType.DELETE:
                query_string = f"DELETE FROM {table_name}{where_section}"

        return query_string

    def __build_section(self, section_values: dict[str, str] | None, section_type: SectionType) -> str | None:
        section = ""

        if section_values is None:
            return section

        match section_type:
            case SectionType.WHERE:
                section = " WHERE"
                for key, value in section_values.items():
                    key = self.__sanatize_table_columns(key)
                    where_key = f"where_{key}"
                    section += f" {key}=%({where_key})s AND"
                    self._values_dict[where_key] = value

                return section[:-3]
            case SectionType.SET:
                for key, value in section_values.items():
                    print(f"Set Key: {key}, Set Value: {value}")
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

                columns_string = ",".join(columns_list)
                values_string = ",".join(values_list)

                return f"({columns_string}) VALUES({values_string})"

    def __run_query(self, query: str) -> tuple[int, list[dict[str, str]] | str]:
        status = 0
        results = ""

        # This try block catches any connection errors
        try:
            with pymssql.connect(**self._conn_props) as conn:  # type: ignore
                if self._query_type == QueryType.SELECT:
                    with conn.cursor(as_dict=True) as cursor:
                        cursor.execute(query, self._values_dict)
                        row_count = cursor.rowcount

                        results = (
                            "No records found"
                            if row_count == 0
                            else [
                                {key: f"{value}" for key, value in row.items()}
                                for row in cursor
                            ]
                        )
                else:
                    # This try block is used to rollback the sql connection if something occurs during execution
                    try:
                        with conn.cursor() as cursor:
                            cursor.execute(query, self._values_dict)

                            match self._query_type:
                                case QueryType.UPDATE:
                                    results = "Update Successful"
                                case QueryType.DELETE:
                                    results = "Delete Successful"
                                case QueryType.INSERT:
                                    results = "Insert Successful"

                            conn.commit()
                    except pymssql.Error as ex:  # type: ignore
                        conn.rollback()
                        status = -1
                        results = f"{ex}"

        except pymssql.Error as ex:  # type: ignore
            status = -1
            results = f"{ex}"

        return (status, results)

    # endregion

    # region HelperMethods
    def __sanatize_table_columns(self, value: str):
        """Sanatizese the table name and column values that are pulled in from the .env file"""
        sanatized_value = ""
        bad_characters = ("%", "\\", "@", ";", "'", '"', "`", ":")
        sanatized_value = "".join([ch for ch in value if ch not in bad_characters])
        sanatized_value = f"[{sanatized_value}]"
        return sanatized_value

    # endregion
