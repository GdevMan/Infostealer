import socket
import os

HOST = "0.0.0.0"
PORT = 8000
SAVE_DIR = "received_files"

os.makedirs(SAVE_DIR, exist_ok=True)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
print(f"Server listening on {HOST}:{PORT}...")

conn, addr = s.accept()
print(f"Connection accepted from {addr}")

def recv_exact(sock, num_bytes):
    """Receive exactly num_bytes from the socket"""
    data = b""
    while len(data) < num_bytes:
        packet = sock.recv(num_bytes - len(data))
        if not packet:
            break
        data += packet
    return data

while True:

    raw_name_len = recv_exact(conn, 4)
    if not raw_name_len:
        break
    name_len = int.from_bytes(raw_name_len, "big")

    filename = recv_exact(conn, name_len).decode()

    raw_content_len = recv_exact(conn, 8)
    if not raw_content_len:
        break
    content_len = int.from_bytes(raw_content_len, "big")

    content = recv_exact(conn, content_len)

    file_path = os.path.join(SAVE_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(content)
    print(f"Received file: {filename} ({content_len} bytes)")

raw_dir_len = recv_exact(conn, 4)
if raw_dir_len:
    dir_len = int.from_bytes(raw_dir_len, "big")
    directories_info = recv_exact(conn, dir_len).decode()
    print(f"Directories info received: {directories_info}")

conn.close()
s.close()
print("Server closed.")
