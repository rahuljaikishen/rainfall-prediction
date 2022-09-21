import psycopg2
from common.config import config

#establishing the connection
# class Db:
    
def create_connection():
    try:
        conn = psycopg2.connect(database=config['DATABASE']['DB_NAME'], user=config['DATABASE']['USERNAME'], password=config['DATABASE']['PASSWORD'], host=config['DATABASE']['HOSTNAME'], port= config['DATABASE']['PORT'])
        return conn
    except (Exception, psycopg2.Error) as error:
        print('DB connection error ---',error)
        return False

def write_data(query):
    connection = create_connection()
    if connection is not False:
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            connection.close()
            return True
        except (Exception, psycopg2.Error) as error:
            print('Write query failure ---',error)
            connection.close()
            return False

def read_data(query):
    connection = create_connection()
    if connection is not False:
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            connection.close()
            return result
        except Exception:
            print('Read query failure ---',Exception)
            connection.close()
            return False

