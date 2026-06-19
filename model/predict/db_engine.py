import os
import boto3
import psycopg2



from utils import Singleton, get_env_variable, get_secret_manager_value



class DatabaseConnection(Singleton):            
    def __init__(self, host, port, database, user, password, sslmode='verify-full', sslrootcert=None):
        if not hasattr(self, "_initialized"):
            self.host = host
            self.port = port
            self.database = database
            self.user = user
            self.password = password
            self.sslmode = sslmode
            self.sslrootcert = sslrootcert

    def connect(self):
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                sslmode=self.sslmode,
                sslrootcert=self.sslrootcert
            )
            return conn
        except Exception as e:
            print(f"Database connection error: {e}")
            raise e

    def close(self, conn):
        if conn:
            conn.close()
    
    def execute_query(self, query):
        conn = None
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute(query)
            result = cur.fetchall()
            cur.close()
            return result
        except Exception as e:
            print(f"Query execution error: {e}")
            raise e
        finally:
            self.close(conn)



db_engine = DatabaseConnection(
    host=get_env_variable('RDS_HOST'),
    port=get_env_variable('RDS_PORT'),
    database=get_env_variable('RDS_DB_NAME'),
    user=get_env_variable('RDS_USERNAME'),
    password=get_secret_manager_value('RDS_DB_PASSWORD')
)

db_engine.connect()