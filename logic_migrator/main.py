from common.config import Config
from common.db import DB
from logic_migrator.stored_procedure_converter import Converter

class SQLLogicMigrator:
    def __init__(self):
        self.pg_db = DB(Config.PG_CONN)
        self.converter = Converter(Config.SQL_CONN)

    def migrate(self):
        self.converter.start()
        self.pg_db.execute_query_from_directory("procedures/converted_procedures")




