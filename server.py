import threading
import socket
import enum
import random


class Command(enum.Enum):
    GET_IMAGE = 'get_image'


def run_server():
    clients = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(
        ('localhost', 8877)
    )
    sock.listen(10)
    while True:
        try:
            conn, add = sock.accept()
            print("Connect new client -> {} {}".format(add, conn))
            t = threading.Thread(target=handler_client, args=(conn, add))
            clients.append(t)
            t.start()
        except Exception as e:
            print("error ->", e)
            break
    [c.join() for c in clients]


def handler_client(conn: socket.socket, add):
    while True:
        data = conn.recv(1024)
        if not data:
            conn.close()
            return
        try:
            cmd = Command(data.decode().strip())
            if cmd == Command.GET_IMAGE:
                print("Send image")
                d = read_image('image.jpg')
                r = list(zip(["{}".format(i + 1) for i in range(len(d))], d))
                random.shuffle(r)
                for number_chunk, d in r:
                    conn.send(number_chunk.encode() + d + b'\r\n')
                conn.close()
                return
        except ValueError:
            print("Cmd not found {} {}".format(add, conn))
            conn.send(b'CMD not found!\r\n')


def read_image(path) -> list:
    d = list()
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(32)
            if not chunk:
                break
            d.append(chunk)
    return d


if __name__ == '__main__':
    run_server()

