from common.ai import AI, ChatGPT, ChatGPTModels
from common.config import Config
from common.db import DB
from common.file import File
from logic_migrator.prompts import  sqlserver_to_postgresql_sp_ix_1

class Converter:
    def __init__(self, conn_str):
        self.skipped_dir = f"procedures/skipped_procedures/{Config.ENV}"
        self.converted_dir = f"procedures/converted_procedures/{Config.ENV}"
        self.db = DB(conn_str)
        self.ai = AI(ChatGPT(ChatGPTModels.GPT_3_5_TURBO_INSTRUCT))

    def start(self):
        procedures = self.__get_stored_procedures()
        skipped_procedures=[]
        File.make_directory(self.skipped_dir)
        for proc_name, proc_def in procedures:
            
            base_dir = f"{self.converted_dir}/{proc_name.lower()}"
            
            File.make_directory(base_dir)
            sql_file_name = f"{base_dir}/sqlserver.sql"
            pg_file_name = f"{base_dir}/postgresql.sql"
            
            
            if not File.exists(sql_file_name):
                File.write(sql_file_name,proc_def)

            if File.exists(pg_file_name):
                print(f"PostgreSQL file '{pg_file_name}' already exists.")
                continue
            
            try:
                converted_proc = self.__convert_procedure_to_postgresql(proc_def)

                File.write(pg_file_name,converted_proc)
                
                print(f"Converted procedure saved to {pg_file_name}")
            except Exception as e:
                skipped_procedures.append(proc_name)
                File.write(f"{self.skipped_dir}/{proc_name.lower()}.sql",proc_def)
                print(e)
    
    def __get_stored_procedures(self):
        procedures = []
        already_explored_procedures  = File.list_folders(self.converted_dir) + File.list_files(self.skipped_dir)

        # Convert the combined list to a string suitable for the SQL IN clause
        if already_explored_procedures:
            exclusions = ', '.join(f"'{item}'" for item in already_explored_procedures)
            exclusion_clause = f"AND ROUTINE_NAME NOT IN ({exclusions})"
        else:
            exclusion_clause = ""

        sql = f"""
            SELECT ROUTINE_NAME
            FROM INFORMATION_SCHEMA.ROUTINES
            WHERE ROUTINE_TYPE = 'PROCEDURE'
            {exclusion_clause}
        """
        print(sql)
        rows = self.db.fetchall(sql)

        for row in rows:
            procedure_name=row.ROUTINE_NAME
            definitions = self.__get_procedure_definitions( procedure_name)
            if not definitions:
                print(f"Procedure Definition '{procedure_name}' not found.")
                return
            
            proc_def = '\n'.join(definitions)
            procedures.append((procedure_name, proc_def))
        return procedures

    def __get_procedure_definitions(self, procedure_name):
        definitions = []
        
        rows = self.db.fetchall(f"EXEC sp_helptext '{procedure_name}'")
        for row in rows:
            line = row[0].strip()
            if not line.startswith('--'):
                definitions.append(line)
        return definitions
      

    def __convert_procedure_to_postgresql(self,procedure_definition):
        prompt = f"""
        {sqlserver_to_postgresql_sp_ix_1}
        {procedure_definition}
        """

        procedure_tokens = self.ai.estimate_tokens(procedure_definition)
       
        return self.ai.ask_if_valid(prompt,procedure_tokens)
    



