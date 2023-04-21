import os

import psutil

# Get the process ID of the current Python process
pid = os.getpid()

# Use the psutil library to get the process object for the current process
process = psutil.Process(pid)

# Get the memory info for the process
mem_info = process.memory_info()

# Print out the memory layout of the process
print("Text segment size:", mem_info.rss)
print("Data segment size:", mem_info.data)
print(f"Process Status: {process.status()}")
print(f"Process Memory Information: {process.memory_info()}")
print(f"checking process is running: {process.is_running()}")
