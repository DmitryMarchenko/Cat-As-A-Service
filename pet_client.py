from socket import *

host = 'localhost'
port = 8070
addr = (host, port)

tcp_socket = socket(AF_INET, SOCK_STREAM)
tcp_socket.connect(addr)

try:
    while True:
        data = input('Your name: ')
        data = str.encode(data)
        tcp_socket.send(data)
        print(f'sent: {bytes.decode(data)}')
        data = tcp_socket.recv(1024)
        data = bytes.decode(data)
        print(f'received: {data}')

finally:
    tcp_socket.close()
