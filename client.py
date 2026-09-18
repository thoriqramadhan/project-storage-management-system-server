import socket
import json

SERVER_IP: str = '127.0.0.1'
SERVER_PORT: int = 5000
# SERVER_IP: str = 'zgcfn-182-253-161-60.run.pinggy-free.link'
# SERVER_PORT: int = 43555
BUFFER_SIZE: int = 4096


def run_test_client() -> None:
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  try:
    print(f'[*] Menghubungkan ke {SERVER_IP}:{SERVER_PORT}...')
    client.connect((SERVER_IP, SERVER_PORT))
    print('[+] Terhubung! Ketik pesan (atau ketik "exit" untuk keluar).\n')

    while True:
      # pesan = input('Client > ')
      pesan = {
          "action": "CHECK_STOCKS",
          # "payload": {
          #   "name": "Kabel UTP Cat 6",
          #   "category_id": 1,
          #   "quantity": 50
          # }
        }
      # if pesan.strip().lower() == 'exit':
      #   break
      # if not pesan.strip():
      #   continue

      client.sendall(json.dumps(pesan).encode('utf-8'))
      balasan = client.recv(BUFFER_SIZE).decode('utf-8')
      print(f'Server Response < {balasan}\n')
      break

  except ConnectionRefusedError:
    print('[-] Gagal: Server belum aktif.')
  except Exception as e:
    print(f'[-] Error: {e}')
  finally:
    client.close()
    print('[*] Koneksi ditutup.')


if __name__ == '__main__':
  run_test_client()