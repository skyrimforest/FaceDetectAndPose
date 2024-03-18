import multiprocessing
import time
import psutil

# 定义一个函数，用于让进程占用 CPU
def cpu_bound_task(usage):
    while True:
        start_time = time.time()
        while time.time() - start_time < 1:
            pass
        time.sleep(1 - usage / 100)

# 定义一个函数，用于创建并启动多个进程
def start_processes(num_processes, usage):
    processes = []
    for _ in range(num_processes):
        p = multiprocessing.Process(target=cpu_bound_task, args=(usage,))
        p.start()
        processes.append(p)
    return processes

# 控制 CPU 利用率的主函数
def control_cpu_utilization(target_utilization, num_processes=4):
    processes = start_processes(num_processes, target_utilization)
    while True:
        current_utilization = psutil.cpu_percent()
        if current_utilization < target_utilization:
            # 如果当前 CPU 利用率低于目标利用率，则增加一个进程
            p = multiprocessing.Process(target=cpu_bound_task, args=(target_utilization,))
            p.start()
            processes.append(p)
        elif current_utilization > target_utilization and len(processes) > 1:
            # 如果当前 CPU 利用率高于目标利用率且存在多个进程，则停止一个进程
            p = processes.pop()
            p.terminate()
        time.sleep(1)

# 在这里设置目标 CPU 利用率（0-100 之间的整数）
target_cpu_utilization = 80

# 启动 CPU 利用率控制程序
control_cpu_utilization(target_cpu_utilization)
