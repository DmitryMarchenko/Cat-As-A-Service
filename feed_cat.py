from socket import *

host = 'localhost'
port = 8080
addr = (host, port)

udp_socket = socket(AF_INET, SOCK_DGRAM)
udp_socket.bind(addr)

preferred_food = {"Fish", "Meat", "Milk", "Bread", "Carrot", "Beer"}


def write_to_log(msg):
    with open('log.txt', 'a') as log:
        log.write(f'{msg}\n')
        print(msg)


with open('log.txt', 'w') as log_file:
    log_file.write(f'Preferred food: {preferred_food}\n')

cur_str = ''
try:
    while True:
        data, addr = udp_socket.recvfrom(1024)
        data = bytes.decode(data)
        write_to_log(f'Datagram received: {data}')
        answer = ''
        if data[-1] == '~':
            cur_str += data
            write_to_log(cur_str)
            user, food = cur_str.split(' - ', 2)
            food = food[:-1]
            if food in preferred_food:
                answer = 'Eaten by the Cat'
            else:
                answer = 'Ignored by the Cat'
            cur_str = ''
        elif len(data) > 1 and data[-2] == '~':
            num = data[-1]
            cur_str += data[:-2]
            answer = f'The Cat is amused by #{num}'
        else:
            answer = 'Incorrect message format!'
        write_to_log(f'Reply: {answer}')
        answer = str.encode(answer)
        udp_socket.sendto(answer, addr)
finally:
    udp_socket.close()
