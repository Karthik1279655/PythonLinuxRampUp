import os

# Open a file for reading
fd = os.open("test.txt", os.O_RDONLY)

# Get the file descriptor's position in the file table
pos = os.lseek(fd, 0, os.SEEK_CUR)

# Get the inode number of the file
inode = os.fstat(fd).st_ino

# Close the file
os.close(fd)

print(f"File descriptor: {fd}")
print(f"Position in file table: {pos}")
print(f"Inode number: {inode}")
