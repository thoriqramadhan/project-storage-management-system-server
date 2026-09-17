import socket

SERVER_IP: str = '127.0.0.1'
SERVER_PORT: int = 5000
BUFFER_SIZE: int = 4096


def run_test_client() -> None:
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  try:
    print(f'[*] Menghubungkan ke {SERVER_IP}:{SERVER_PORT}...')
    client.connect((SERVER_IP, SERVER_PORT))
    print('[+] Terhubung! Ketik pesan (atau ketik "exit" untuk keluar).\n')

    while True:
      pesan = input('Client > ')
      if pesan.strip().lower() == 'exit':
        break
      if not pesan.strip():
        continue

      client.sendall(pesan.encode('utf-8'))
      balasan = client.recv(BUFFER_SIZE).decode('utf-8')
      print(f'Server Response < {balasan}\n')

  except ConnectionRefusedError:
    print('[-] Gagal: Server belum aktif.')
  except Exception as e:
    print(f'[-] Error: {e}')
  finally:
    client.close()
    print('[*] Koneksi ditutup.')


if __name__ == '__main__':
  run_test_client()