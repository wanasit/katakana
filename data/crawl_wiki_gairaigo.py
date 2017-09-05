from bs4 import BeautifulSoup
import requests
import csv

URL = 'https://en.wikipedia.org/wiki/List_of_gairaigo_and_wasei-eigo_terms'
response = requests.get(URL)

soup = BeautifulSoup(response.content, 'html5lib')
table = soup.find(attrs={'class': 'wikitable'})

rows = table.find_all('tr')[1:]
rows = [[td.text for td in r.find_all('td')] for r in rows]

with open('gairaigo.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['katakana', 'origin', 'meaning', 'language'])
    for r in rows:
        r = [u.encode('utf-8') for u in r]
        writer.writerow(r)