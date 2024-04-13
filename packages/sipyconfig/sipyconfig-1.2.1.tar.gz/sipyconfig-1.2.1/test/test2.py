# pylint: skip-file
# type: ignore
import socket
import time

HOST = "127.0.0.1"
PORT = 10000

prefix = b"\xb3\x9d\xbc\x0b\xad\x71\x06\xfe\xe9\x9d\x35\x60\x93\xce\x02\xf5"
a = [120, 198, 229, 181, 191, 246, 126, 186, 31, 118, 223, 60, 56, 23, 22, 129, 115, 104, 190, 180]

for x in range(len(a)):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        b = bytearray(a[:x]+[a[x]+1]+a[x:])
        s.sendall(prefix+b)
    time.sleep(0.5)
