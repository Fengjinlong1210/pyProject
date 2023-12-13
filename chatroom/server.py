import threading
from typing import Callable
import socket
import logging
import thread
import time
import buffer
import user


addr = '0.0.0.0'
port = 8888
SEP = ': '


class UdpServer:
    user_manager = user.UserManager()

    # 传递服务器ip，port和处理客户端消息的handle函数
    def __init__(self, svr_addr, svr_port, svr_handle: Callable[[str], str]):
        # 创建类成员变量
        self.handle = svr_handle
        self.addr = svr_addr
        self.port = svr_port
        # 创建两个线程，一个用来接受所有客户端发来的消息，另一个用来把所有的消息派发到多个客户端中
        self._recv_thread = thread.MyThread('接受消息线程', thread_func = self.receive_msg)
        self._cast_thread = thread.MyThread('派发消息线程', thread_func = self.broadcast_msg)
        # 消息缓冲区，用来存放客户端发送过来的消息
        self._msg_buffer = buffer.Buffer(50)
        # 锁
        self._lock = threading.Lock()
        # 初始化套接字
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except Exception as e:
            logging.log(level = logging.ERROR, msg = f'socket error: {e}')
        else:
            logging.log(level = logging.INFO, msg = 'socket initialization succeed')
        # 绑定端口
        self.server.bind((addr, port))

    def start(self):
        # 启动两个线程
        self._recv_thread.start()
        self._cast_thread.start()

    def receive_msg(self):
        """
        接受消息的线程，处理接收到的消息，进行用户管理
        """
        while True:
            data, client = self.server.recvfrom(2048)
            user_name, user_msg = self.parse_data(data)
            self.user_manager.add_user(user_name = user_name, user_addr = client)
            msg = user_name + ' >> ' + user_msg
            self._msg_buffer.push(msg)

    def broadcast_msg(self):
        """
        派发消息的线程，从缓冲区中拿取数据，发送给所有用户
        """
        while True:
            data = self._msg_buffer.pop()   # 拿到信息，向每个用户发送
            if data:
                print(data)
                users = self.user_manager.get_all_user()
                for usr in users:
                    user_addr = users[usr]
                    user_ip = user_addr[0]
                    user_port = user_addr[1]
                    self.server.sendto(data.encode('utf-8'), (user_ip, user_port))

    @staticmethod
    def parse_data(data):
        data = data.decode('utf-8')
        sep_index = data.find(SEP)
        user_name = data[:sep_index]
        msg = data[sep_index + len(SEP):]
        return user_name, msg


def handle(msg: str):
    msg = msg.upper()
    return msg


if __name__ == '__main__':
    server = UdpServer(svr_addr = addr, svr_port = port, svr_handle = handle)
    # print(type(handle))
    server.start()
