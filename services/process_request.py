from typing import Any
import database.db_connection

db_con = database.db_connection.db_con
cursor = db_con.cursor()
def process_request(request_payload : dict[str , Any] , client_ip: int, hostname:str)-> dict[str , Any]: 
    action = request_payload.get('action')
    payload = request_payload.get('payload')
    result:dict[bool , Any]
    match action:
        case 'CHECK_STOCKS':
            print('called check')
            result = check_stocks()
        case 'ADD_ITEMS':
            print('ADD_ITEMS')
        case 'UPDATE_STOCKS':
            print('UPDATE_STOCKS')
        case 'DELETE_ITEMS':
            print('DELETE_ITEMS')
        case 'CHECK_SERVER_STATUS':
            print('CHECK_SERVER_STATUS')


    print(F'ACTION : {action}\n')
    print(F'PAYLOAD : {payload}\n')
    print(F'RESULT : {result}')
    access_logs(client_ip , hostname , action)
    return result

def access_logs(client_ip: int, hostname:str, action: str):
    print('CALEED ACESS LOGS')
    try: 
        cursor.execute('insert into access_logs (client_ip , client_hostname , action_performed ) values(%s , %s , %s)' , (client_ip , hostname , action))
        db_con.commit()
    except Exception as e:
        print(f'Error on creating logs : {e}') 
        db_con.rollback()
        return {
            'status': False,
        }

def check_stocks():
    try:
        cursor.execute('select id , name , stock, updated_at from items') 
        return {
                'status': True,
                'datas': cursor.fetchall(),
                'messages': 'Berhasil mengambil stock barang'
            }
    except Exception as e:
        print(f'Error on creating category : {e}') 
        return {
            'status': False,
        }

def add_category(name:str):
    try:
        cursor.execute('insert into categories (name) values (%s)', (name))
        db_con.commit()
        inserted_id = cursor.lastrowid
        return {
            'status' : True,
            'datas': {
                'inserted_id' : inserted_id
            },
            'messages' : 'Kategori berhasil ditambahkan'
            
        }
    except Exception as e:
        print(f'Error on creating category : {e}')
        db_con.rollback()
        return {
                    'status': False,
                }
        
# def add_category(name:str):
#     try:
#         cursor.execute('insert into categories (name) values (%s)', (name))
#         db_con.commit()
#         inserted_id = cursor.lastrowid
#         return {
#             'status' : True,
#             'datas': {
#                 'inserted_id' : inserted_id
#             },
#             'messages' : 'Kategori berhasil ditambahkan'
            
#         }
#     except Exception as e:
#         print(f'Error on creating category : {e}')
#         db_con.rollback()
#         return {
#                     'status': False,
#                 }
        
