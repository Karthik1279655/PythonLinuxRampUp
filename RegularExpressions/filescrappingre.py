import re
import urllib.request

url = urllib.request.urlopen("https://www.redbus.in/info/contactus")
text = url.read().decode('utf-8')  # Decode the byte string to UTF-8 text
pincodes = re.findall(r'\b\d{6}\b', text)  # Find all 6-digit numbers that are not part of a longer sequence
for pincode in pincodes:
    print(pincode)
