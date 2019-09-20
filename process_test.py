from multiprocessing import Pool, cpu_count, Process
import os
import time


def long_time_task(i):
    print('子进程: {} - 任务{}'.format(os.getpid(), i))
    time.sleep(2)
    print("结果: {}".format(8 ** 20))


if __name__ == '__main__':
    print("CPU内核数:{}".format(cpu_count()))
    print('当前母进程: {}'.format(os.getpid()))
    start = time.time()
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('等待所有子进程完成。')
    p.close()
    p.join()
    end = time.time()
    print("总共用时{}秒".format((end - start)))

    # print('当前母进程: {}'.format(os.getpid()))
    # start = time.time()
    # p1 = Process(target=long_time_task, args=(1,))
    # p2 = Process(target=long_time_task, args=(2,))
    # print('等待所有子进程完成。')
    # p1.start()
    # p2.start()
    # p1.join()
    # p2.join()
    # end = time.time()
    # print("总共用时{}秒".format((end - start)))