import socket
import threading

from server import SEP, UdpServer
import thread

addr = '43.138.29.200'
port = 8888


def recv_from_server(sock):
    """
    客户端创建一个额外的线程用来接收服务端发来的消息
    """
    _client = sock
    while True:
        msgs, address = _client.recvfrom(1024)
        if msgs:
            print(msgs)


if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    user_name = input('please input your name: ')
    recv = threading.Thread(target = recv_from_server, args = (client, ))
    recv.start()
    while True:
        data = input('please input: ')
        msg = user_name + SEP + data
        client.sendto(msg.encode('utf-8'), (addr, port))


