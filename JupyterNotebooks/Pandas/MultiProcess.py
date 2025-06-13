import time
from multiprocessing import Process # 1) Importing module

def task_read_csv_file(file_name):
    print("File name:", file_name)
    time.sleep(1)


start = time.perf_counter()

pids = []

# ----- main process ------
# Need to process 10 files
for i in range(10):
    p = Process(target=task_read_csv_file, args=("file"+str(i+1)+".csv",)) # 2) Creating process
    p.start() # 3) Start the pricess
    pids.append(p)

# Parent waiting for child
# 4) Waiting for all child proccess's exit
for pid in pids:
    pid.join()

stop = time.perf_counter()
print("Time Taken:", stop-start)
