import mysql.connector
import os 
from dotenv import load_dotenv

load_dotenv()

passwd = os.getenv('DB_PASSWD')
db_con = mysql.connector.connect(
    user='root',
    host='localhost',
    passwd=passwd,
    database='storage_management_system'
)
if db_con.is_connected:
    print('Connected')

