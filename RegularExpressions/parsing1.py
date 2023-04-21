import requests
from bs4 import BeautifulSoup

# Send a GET request to the web page
url = 'http://www.google.com'
response = requests.get(url)
print(response)


# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')
print(soup)

# Extract specific data from the web page
title = soup.title.text
print(title, flush=True)
links = [link['href'] for link in soup.find_all('a')]
paragraphs = [p.text for p in soup.find_all('p')]
