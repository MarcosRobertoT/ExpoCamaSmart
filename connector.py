import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def conectar():
    try:
        conexao = mysql.connector.connect(
            host=os.getenv("HOST"),
            port=os.getenv("PORT"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE")
        )
        return conexao
    except mysql.connector.Error as erro:
        print(f"Erro na conexão com o banco de dados: {erro}")
        raise
