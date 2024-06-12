
from dotenv import load_dotenv
import os


class Config:
    load_dotenv()
    OPEN_AI_API_KEY =os.getenv('OPEN_AI_API_KEY')
    SQL_CONN =os.getenv('SQL_CONNECTION_STRING')
    PG_CONN=os.getenv('PG_CONNECTION_STRING')
    ENV=os.getenv('ENV')