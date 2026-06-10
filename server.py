import socket
import struct
import os

HOST = "0.0.0.0"
PORT = 5000

SAVE_DIR = "received_files"
os.makedirs(SAVE_DIR, exist_ok=True)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)

print("等待连接...")
conn, addr = server.accept()

print("连接来自:", addr)

# 接收文件名长度 (4字节)
raw_len = b''
while len(raw_len) < 4:
    packet = conn.recv(4 - len(raw_len))
    if not packet:
        break
    raw_len += packet
filename_len = struct.unpack("I", raw_len)[0]

# 接收文件名
filename = b''
while len(filename) < filename_len:
    packet = conn.recv(filename_len - len(filename))
    if not packet:
        break
    filename += packet
filename = filename.decode()

# 接收文件大小 (8字节)
raw_size = b''
while len(raw_size) < 8:
    packet = conn.recv(8 - len(raw_size))
    if not packet:
        break
    raw_size += packet
filesize = struct.unpack("Q", raw_size)[0]

print("文件名:", filename)
print("文件大小:", filesize, "字节")

save_path = os.path.join(SAVE_DIR, filename)

received = 0

with open(save_path, "wb") as f:
    while received < filesize:
        remaining = filesize - received
        chunk_size = min(4096, remaining)
        data = conn.recv(chunk_size)
        if not data:
            break
        f.write(data)
        received += len(data)
        percent = received * 100 / filesize
        print(f"\r接收进度: {percent:.2f}%", end="")

print("\n接收完成!")
print(f"文件保存到: {save_path}")

conn.close()
server.close()