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
            print('called add items')
            print(f'rackId:{payload.get('rack_id')} , category_id:{payload.get('category_id')}')
            result = add_item(payload.get('category_id') ,payload.get('rack_id') , payload.get('name') , payload.get('quantity') )
        case 'UPDATE_STOCKS':
            print('UPDATE_STOCKS')
            result = update_item(payload.get('category_id') ,payload.get('rack_id') , payload.get('name') , payload.get('stock') , payload.get('item_id'))
        case 'DELETE_ITEMS':
            print('DELETE_ITEMS')
            result = delete_item(payload.get('item_id'))
        case 'CHECK_SERVER_STATUS':
            print('CHECK_SERVER_STATUS')
            result = {'status': True, 'messages': 'Server is running'}
        case 'ADD_CATEGORY':
            print('called add category')
            result = add_category(payload.get('name'))
        case 'ADD_RACK':
            print('called add rack')
            result = add_rack(payload.get('name'))
        case 'GET_CATEGORY':
            print('called get category')
            result = get_category()
        case 'GET_RACK':
            print('called get rack')
            result = get_rack()
        case 'EDIT_CATEGORY':
            print('called edit category')
            result = edit_category(payload.get('category_id'), payload.get('name'))
        case 'EDIT_RACK':
            print('called edit rack')
            result = edit_rack(payload.get('rack_id'), payload.get('name'))
        case 'GET_ACCESS_LOGS':
            print('called get access logs')
            result = get_access_logs()
    print(F'ACTION : {action}\n')
    print(F'PAYLOAD : {payload}\n')
    print(F'RESULT : {result}')
    access_logs(client_ip , hostname , action)
    return result or {
                    'status': False,
                }

def access_logs(client_ip: int, hostname:str, action: str):
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
def add_rack(name:str):
    try:
        cursor.execute('insert into rack (name) values (%s)', (name))
        db_con.commit()
        inserted_id = cursor.lastrowid
        return {
            'status' : True,
            'datas': {
                'inserted_id' : inserted_id
            },
            'messages' : 'rak berhasil ditambahkan'
            
        }
    except Exception as e:
        print(f'Error on creating rack : {e}')
        db_con.rollback()
        return {
                    'status': False,
                }

def get_category():
    try:
        cursor.execute('select id, name from categories')
        return {
            'status': True,
            'datas': cursor.fetchall(),
            'messages': 'Berhasil mengambil data kategori'
        }
    except Exception as e:
        print(f'Error on get category : {e}') 
        return {
            'status': False,
        }

def get_rack():
    try:
        cursor.execute('select id, name from rack')
        return {
            'status': True,
            'datas': cursor.fetchall(),
            'messages': 'Berhasil mengambil data rak'
        }
    except Exception as e:
        print(f'Error on get rack : {e}') 
        return {
            'status': False,
        }
        
def edit_category(category_id, name):
    try:
        cursor.execute('update categories set name = %s where id = %s', (name, category_id))
        db_con.commit()
        return {
            'status' : True,
            'messages' : 'Kategori berhasil diupdate'
        }
    except Exception as e:
        print(f'Error on editing category : {e}')
        db_con.rollback()
        return {
                    'status': False,
                }
                
def edit_rack(rack_id, name):
    try:
        cursor.execute('update rack set name = %s where id = %s', (name, rack_id))
        db_con.commit()
        return {
            'status' : True,
            'messages' : 'Rak berhasil diupdate'
        }
    except Exception as e:
        print(f'Error on editing rack : {e}')
        db_con.rollback()
        return {
                    'status': False,
                }

def get_access_logs():
    try:
        cursor.execute('select id, client_ip, client_hostname, action_performed, created_at from access_logs order by created_at desc')
        return {
            'status': True,
            'datas': cursor.fetchall(),
            'messages': 'Berhasil mengambil data access logs'
        }
    except Exception as e:
        print(f'Error on get access logs : {e}') 
        return {
            'status': False,
        }
        
def add_item(category_id , rack_id , name , stock):
    try:
        cursor.execute('insert into items (name, stock , rack_id , category_id ) values (%s, %s ,%s ,%s)', (name , stock , rack_id , category_id))
        db_con.commit()
        inserted_id = cursor.lastrowid
        return {
            'status' : True,
            'datas': {
                'inserted_id' : inserted_id
            },
            'messages' : 'Barang berhasil ditambahkan'
            
        }
    except Exception as e:
        print(f'Error on creating item : {e}')
        db_con.rollback()
        return {
                    'status': False,
                }
        
def update_item(category_id , rack_id , name , stock , item_id):
    try:
        cursor.execute('update items set category_id = %s , rack_id = %s , name = %s , stock =  %s where id = %s' , (category_id , rack_id , name, stock , item_id))
        db_con.commit()
        inserted_id = cursor.lastrowid
        return {
            'status' : True,
            'datas': {
                'inserted_id' : inserted_id
            },
            'messages' : 'Barang berhasil diupdate'
            
        }
    except Exception as e:
        print(f'Error on updating item : {e}')
        db_con.rollback()
        return {
                    'status': False,
                }
        
def delete_item(item_id):
    try:
        cursor.execute('delete from items where id = %s', (item_id,))
        db_con.commit()
        return {
            'status' : True,
            'messages' : 'Barang berhasil dihapus'
        }
    except Exception as e:
        print(f'Error on deleting item : {e}')
        db_con.rollback()
        return {
                    'status': False,
                }
