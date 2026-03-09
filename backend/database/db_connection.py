import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

#connect to postgresql database using psycopg2, and gets credentials from env file
def get_connection():
    return psycopg2.connect(   
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        host=os.getenv("DB_HOST"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
)
