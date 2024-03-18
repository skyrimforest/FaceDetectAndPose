import functools
import time

# 包装函数的计时器
def tick_tok(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t1=time.time()
        func(*args, **kwargs)
        t2=time.time()
        # todo
        # 根据工作的编号,将两个时间都发送到数据库中,进行持久化存储.
        # 数据库可以采用mongodb等
        print(f"{func.__name__}总共执行了:{t2-t1}秒")
    return wrapper