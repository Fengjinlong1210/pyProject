import threading
from typing import Callable


class MyThread(threading.Thread):
    def __init__(self, thread_name: str, thread_func: Callable[[], None], ):
        threading.Thread.__init__(self)
        self.__name = thread_name
        self.__func = thread_func
        self.__tid = 0

    @staticmethod
    def call_thread_func(self):
        self.__func()

    def run(self):
        try:
            MyThread.call_thread_func(self)
        except Exception as e:
            print(e)


if __name__ == "__main__":

    def func():
        print('I am threading')

    thread1 = MyThread('1号线程', thread_func = func)
    thread1.start()
    thread1.join()

