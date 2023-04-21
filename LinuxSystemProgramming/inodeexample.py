import os

# Specify the path to the file you want to inspect
path = '/home/ee212783/PycharmProjects/PythonLinuxRampUp/LinuxSystemProgramming/inodeexample.py'

# Use the stat() system call to retrieve information about the file
stat_info = os.stat(path)

# Print out some information retrieved from the inode
print("File name:", os.path.basename(path))
print("File size (in bytes):", stat_info.st_size)
print("Owner user ID:", stat_info.st_uid)
print("Owner group ID:", stat_info.st_gid)
print("File mode (permissions):", oct(stat_info.st_mode))
print("Last access time:", stat_info.st_atime)
print("Last modification time:", stat_info.st_mtime)
print("Last status change time:", stat_info.st_ctime)
