import threading
import time

'''
创建两个线程，间隔指定时间交替打印信息

def thread_routine(thread_name, delay_time):
    cnt = 0
    while cnt < 5:
        time.sleep(delay_time)
        print('线程id: %s, 时间: %s' % (thread_name, time.ctime(time.time())))
        cnt += 1


def main():
    t1 = threading.Thread(target = thread_routine, args = ('1号线程', 1))
    t2 = threading.Thread(target = thread_routine, args = ('2号线程', 2))
    t1.start()
    t2.start()

    t1.join()
    t2.join()

if __name__ == '__main__':
    main()
'''

"""
创建三个线程，执行任务队列中的任务
"""