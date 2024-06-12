import os
import pyodbc
class DatabaseConnectionManager:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = pyodbc.connect(self.connection_string)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()
                print(f'Error executing SQL files: {exc_val}')
        finally:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()

class DB:
    def __init__(self, conn_str):
        self.conn_str = conn_str
        self.context = DatabaseConnectionManager(conn_str)
    
    def fetchall(self, sql):
        with self.context as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
        
    def execute(self, query):
        with self.context as cursor:
            cursor.__execute(cursor,query)
    
    def __execute(self, cursor, query):
        cursor.execute(query)

    def execute_sql_file(self, file_path):
        with self.context as cursor:
            self.__execute_sql_file(cursor,file_path)

    def __execute_sql_file(self,cursor, file_path):
        with open(file_path, 'r') as file:
            sql = file.read()
            self.__execute(cursor,sql)

    def execute_query_from_directory(self,directory):
        
        with self.context as cursor:

            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith('.sql'):
                        file_path = os.path.join(root, file)
                        print(f'Executing {file_path}...')
                        self.__execute_sql_file(cursor, file_path)
                        print(f'{file_path} executed successfully.')
