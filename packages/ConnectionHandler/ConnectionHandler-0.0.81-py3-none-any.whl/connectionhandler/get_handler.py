from .connectiontypes.database_handler import Database_Handler

def get_handler(db_type, user_name, password, host, database, port):
    return Database_Handler(db_type, user_name, password, host, database, port)