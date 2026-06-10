import socket
import struct
import os

SERVER_IP = "127.0.0.1"
PORT = 5000

filepath = "test.txt"

filename = os.path.basename(filepath)
filesize = os.path.getsize(filepath)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))

# 文件名
filename_bytes = filename.encode()

# 文件名长度 (4字节)
client.send(struct.pack("I", len(filename_bytes)))

# 文件名
client.send(filename_bytes)

# 文件大小 (8字节)
client.send(struct.pack("Q", filesize))

sent = 0

with open(filepath, "rb") as f:
    while True:
        chunk = f.read(4096)
        if not chunk:
            break
        client.sendall(chunk)
        sent += len(chunk)
        percent = sent * 100 / filesize
        print(f"\r发送进度: {percent:.2f}%", end="")

print("\n发送完成!")

client.close()