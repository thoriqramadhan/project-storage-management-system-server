import socket
import threading
import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
BUFFER_SIZE = int(os.getenv('BUFFER_SIZE'))
MAX_CONN = int(os.getenv('MAX_CONN'))

def client_handler(client_socket: socket.socket , client_address: tuple[str, int]):

    client_ip, client_port = client_address

    print(
        f"\n[+] [THREAD BARU] Terhubung dengan: {client_ip}:{client_port} "
        f"(Total Thread A ktif: {threading.active_count() - 1})"
    )

    try : 
        while True:
            # read client data raw (blocking)
            raw_bytes = client_socket.recv(BUFFER_SIZE)

            if not raw_bytes: 
                print(f"Client {client_ip}:{client_port} disconnected")
                break

            client_message = raw_bytes.decode('utf-8')
            print(f'CLIENT MESSAGES {client_ip}:{client_message}')

            response = f"server accept request : {client_message}"

            client_socket.sendall(response.encode('utf-8')) 
    except ConnectionResetError:
    # handle client force close connection
        print(f'Client force quit {client_ip}:{client_port}')
    except Exception as e:
        print(f'Error on client {client_ip}:{client_port} : {e}')
    finally:
        client_socket.close()
        print(f'END SESSION {client_ip}:{client_port}')

def start_server():
    server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try: 
        server_socket.bind((HOST , PORT))
        server_socket.listen(MAX_CONN)
        print(f"==================================================")
        print(f"[*] SERVER STORAGE SYSTEM AKTIF")
        print(f"[*] Alamat Host : {HOST}")
        print(f"[*] Port Layanan: {PORT}")
        print(f"[*] Status      : Siap Menerima Panggilan Client...")
        print(f"[*] Tekan Ctrl+C untuk mematikan server.")
        print(f"==================================================")

        while True:
            client_socket , clinet_adress = server_socket.accept()

            worker_thread = threading.Thread(
                target=client_handler,
                args=(client_socket, clinet_adress),
                daemon=True
            )
            worker_thread.start()
    except KeyboardInterrupt: 
        print('Client force disconnect')
    except Exception as e :
         print(f"[FATAL ERROR pada Server]: {e}")
    finally:
        server_socket.close()
        print("[*] Socket server berhasil ditutup secara aman.")

if __name__ == '__main__':
    start_server()
