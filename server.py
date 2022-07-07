import socket
import select


SOCKETS = []
CLIENTS = {}

def accept_connection():
    client, address = server.accept()
    print(address, 'connected')
    SOCKETS.append(client)


def receive(client: socket.socket):
    data = client.recv(4096).decode('unicode-escape')
    return data


def send(client: socket.socket, data: str):
    
    for sock in SOCKETS:
        if sock is not client:
            sock.send(data.encode('unicode-escape'))


def main():
    while True:
        to_read, _, _ = select.select(SOCKETS, [], [])
        
        for sock in to_read:
            if sock is server:
                accept_connection()
            else:
                data = receive(sock)
                if not data:
                    sock.close()
                    SOCKETS.remove(sock)
                else:
                    send(sock, data)


if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', 7777))
    server.listen(5)
    SOCKETS.append(server)
    main()