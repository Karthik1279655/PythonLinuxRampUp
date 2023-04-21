import fcntl

# Open a file
file = open("test.txt", "r")
print(file)

# Get the file descriptor of the file
fd = file.fileno()
print(fd)

# Get the current flags of the file descriptor
flags = fcntl.fcntl(fd, fcntl.F_GETFD)
print(flags)

# Add the FD_CLOEXEC flag to the current flags
flags |= fcntl.FD_CLOEXEC
print(flags)

# Set the new flags for the file descriptor
fd1 = fcntl.fcntl(fd, fcntl.F_SETFD, flags)
print(fd1)

# Close the file
file.close()
