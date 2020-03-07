import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

data = b'aaaaaaaa'
# 发送数据:
s.sendto(data, ('127.0.0.1', 9998))
# 接收数据:
print(s.recv(1024).decode('utf-8'))
b = b+"0"
print(len(b))
s.close()