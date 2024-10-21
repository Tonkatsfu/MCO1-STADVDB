import mysql.connector
from mysql.connector import Error

# To connect to the server correcly fill up all information under create_connection which are : 
# host
# port
# user
# password
# database
def create_connection():
    return mysql.connector.connect(
        host="localhost",   
        port=3306,                    
        user="root",             
        password="123456",     
        database="mco1"     
    )

def execute_query(query):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    
    except Error as e:
        print(f"Error while executing query: {e}")
        return None
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()