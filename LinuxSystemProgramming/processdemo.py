import os

# Get the PID of the current process
pid = os.getpid()

# Get the PPID of the current process
ppid = os.getppid()

# Get the process state of the current process
with open(f"/proc/{pid}/stat", "r") as f:
    state = f.read().split()[2]

print(f"PID: {pid}")
print(f"PPID: {ppid}")
print(f"State: {state}")
