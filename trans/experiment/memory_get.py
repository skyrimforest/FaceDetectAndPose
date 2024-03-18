import time


# 1KB
size=1024
total_buf=[]
# 1024*1024能获得1GB
# [1,3.5,5，6.5，9]
count=1024*1024*9
cnt=0
while True:
    # time.sleep(0.1)
    buf=memoryview(bytearray(size))
    total_buf.append(buf)
    cnt+=1
    if cnt>=count:
        time.sleep(100000)