import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do .env

# Lê as variáveis do .env
host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")

def conectar():
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
    )
