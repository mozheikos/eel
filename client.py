import asyncio
from collections import deque
import socket
import sys
import eel


class ClientSocket:
    
    inbox = deque()
    outbox = deque()
    __buffer: int = 4096
    __host: str = '192.168.0.13'
    __port: int = 7777
    
    def __init__(self) -> None:
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def connect(self):
        self.__sock.connect((self.__host, self.__port))
    
    async def send_message(self):
        
        loop = asyncio.get_running_loop()
        
        while True:
            while len(self.outbox):
                
                msg = self.outbox.popleft().encode('unicode-escape')
                
                await loop.sock_sendall(self.sock, msg)
            eel.sleep(0.1)
            await asyncio.sleep(0.1)
    
    @property
    def sock(self):
        return self.__sock
    

@eel.expose
def send_msg(msg: str):
    print(msg)
    CLIENT.outbox.append(msg)

def recieve_mesg(client):
    print('in recv')
    data = client.recv(4096).decode('unicode-escape')
    eel.receive_msg(data)
    print('recev')

async def main():
    CLIENT.connect()
    sock = CLIENT.sock
    loop = asyncio.get_running_loop()
    loop.add_reader(sock, recieve_mesg, sock)
    
    await CLIENT.send_message()
    
            
if __name__ == '__main__':
    CLIENT = ClientSocket()
    eel.init('frontend')
    eel.start('index.html', block=False)
    eel.sleep(1)
    asyncio.run(main())
