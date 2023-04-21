import urllib, re
import urllib.request

sites = ['https://www.google.com', 'https://www.rediff.com']
for site in sites:
    print('Searching....', site)
    u = urllib.request.urlopen(site)
    text = u.read()
    title = re.findall("<title>.*</title>", str(text), re.IGNORECASE)
    print(title[0])
