import mysql.connector
import os 
from dotenv import load_dotenv

load_dotenv()

passwd = os.getenv('DB_PASSWD')
print(passwd)
db_con = mysql.connector.connect(
    user='root',
    host='localhost',
    passwd=passwd
)
if db_con.is_connected:
    print('Connected')


cursor = db_con.cursor()
try:
    # cursor.execute('create database storage_management_system')
    print('')
except: 
    db_con.rollback()
