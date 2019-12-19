from socket import *

host = 'localhost'
port = 8070
addr = (host, port)

tcp_socket = socket(AF_INET, SOCK_STREAM)
tcp_socket.bind(addr)
tcp_socket.listen(1)
conn, addr = tcp_socket.accept()


def write_to_log(msg):
    with open('log.txt', 'a') as log:
        log.write(f'{msg}\n')
        print(msg)


def names_to_answers(names_):
    answers_ = []
    for name in names_:
        prev_line_with_cur_name = False
        success = False
        with open('log.txt', 'r') as log_r:
            lines = log_r.readlines()
        for line in lines:
            if prev_line_with_cur_name:
                if line.strip().endswith('Eaten by the Cat'):
                    success = True
                    answers_.append('Tolerated by the Cat')
                    break
            if line.strip().startswith(name):
                prev_line_with_cur_name = True
            else:
                prev_line_with_cur_name = False
        if not success:
            answers_.append('Scratched by the Cat')
    assert len(names_) == len(answers_)
    return answers_


try:
    while True:
        all_data = ''
        data = ''
        while len(data) == 0 or data[-1] != '~':
            data = conn.recv(1024)
            data = bytes.decode(data)
            if len(data) == 0 or data[-1] != '~':
                conn.send(str.encode('Waiting for the end of the message...'))
            all_data += data
            write_to_log(f'Segment received: {data}')
        write_to_log(all_data)
        names = all_data[:-1].split('~')
        answers = names_to_answers(names)
        ans = '\n'.join(answers)
        write_to_log(f'Reply: {ans}')
        ans = str.encode(ans)
        conn.send(ans)
finally:
    conn.close()
    tcp_socket.close()
