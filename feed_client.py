from socket import *

host = 'localhost'
port = 8080
addr = (host, port)

udp_socket = socket(AF_INET, SOCK_DGRAM)


try:
    while True:
        data = input('Your name and food: ')
        data = str.encode(data)
        udp_socket.sendto(data, addr)
        print(f'sent: {bytes.decode(data)}')
        data, address = udp_socket.recvfrom(1024)
        data = bytes.decode(data)
        print(f'received: {data}')

finally:
    udp_socket.close()
