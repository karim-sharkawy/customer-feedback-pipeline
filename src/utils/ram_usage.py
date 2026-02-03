import os
import psutil
import time

def monitor_memory_usage():
    pid=os.getpid()
    process=psutil.Process(pid)

    while True:
        memory_info = process.memory_info()
        memory_use = memory_info.rss / (1024*1024) # in mib

        print(f"Current memory usage: {memory_use:.2f} MiB")
        time.sleep(1)

print("Starting memory monitoring...")

try:
    monitor_memory_usage()
except KeyboardInterrupt:
    print("Monitoring stopped.")