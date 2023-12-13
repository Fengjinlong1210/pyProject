import thread
import queue
import threading


class Buffer:
    """
    消息缓冲区：客户端向服务器发送的所有消息都会被保存到缓冲区中
    """
    def __init__(self, max_size: int):
        self.queue = queue.Queue(max_size)
        self.lock = threading.Lock()

    def push(self, data):
        self.lock.acquire()
        self.queue.put(data)
        self.lock.release()

    def pop(self):
        self.lock.acquire()
        data = ""
        if not self.queue.empty():
            data = self.queue.get()
        self.lock.release()
        if data:
            return data

