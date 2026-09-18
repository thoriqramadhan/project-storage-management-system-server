from typing import Any
import database.db_connection

db_con = database.db_connection.db_con
cursor = db_con.cursor()
def process_request(request_payload : dict[str , Any])-> dict[str , Any]: 
    action = request_payload.get('action')
    payload = request_payload.get('payload')
    result:dict[bool , Any];
    match action:
        case 'CHECK_STOCKS':
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
    return result

def check_stocks():
    try:
        result = cursor.execute('select id , name , stock, updated_at from items') or []
        return {
                'status': True,
                'datas': result
            }
    except Exception as e:
        print(f'Error on creating category : {e}') 
        return {
            'status': False,
        }

def add_category(name:str):
    try:
        result = cursor.execute('insert into categories (name) values (%s)', (name))
        return {
            'status' : True,
            'datas': result
        }
    except Exception as e:
        print(f'Error on creating category : {e}')
        return {
                    'status': False,
                }
