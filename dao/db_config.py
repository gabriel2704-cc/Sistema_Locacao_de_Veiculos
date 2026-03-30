import psycopg2
from psycopg2 import Error

class DatabaseConfig:
    @staticmethod
    def get_connection():
        try:
            connection = psycopg2.connect(
                user="postgres",
                password="postgres",
                host="localhost",
                port = "5432",
                database="bd_lpoo_locadora_veiculos"
            )
            return connection
        except Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None