import re

valid_passwords = []

passwords = input("Enter the passwords (separated by commas): ").split(',')
for password in passwords:
    if (7 <= len(password) <= 12) and re.search("[a-z]", password) and re.search("[A-Z]", password) and re.search("[0-9]", password) and re.search("[#$@]", password):
        valid_passwords.append(password)

print("Valid passwords:", ", ".join(valid_passwords))


'''
Input >>>  Enter the passwords (separated by commas): Karthi@123,karthi@123,Karthi,karthi@,Karthi@,Karthi@1279655,Karthi@12796
Output >>>  Valid passwords: Karthi@123, Karthi@12796
'''

