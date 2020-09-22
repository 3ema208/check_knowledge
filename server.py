import threading
import socket
import enum


class Command(enum.Enum):
    GET_IMAGE = 'get_image'


def run_server():
    clients = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 8877))
    sock.listen(10)
    while True:
        try:
            conn, add = sock.accept()
            t = threading.Thread(target=handler_client, args=(conn, add))
            clients.append(t)
            t.start()
        except Exception:
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
                d = read_images('image.jpg')
                r = list(zip([i + 1 for i in range(len(d))], d))
                for number_chunk, d in r:
                    conn.send(bytes(number_chunk) + d + b'\r\n')
                conn.close()
                return
        except ValueError:
            conn.send(b'CMD not found!\r\n')


def read_images(path) -> list:
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

