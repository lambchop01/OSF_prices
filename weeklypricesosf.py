import requests
from bs4 import BeautifulSoup
from pathlib import Path


headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
url = "https://www.ontariosheep.org/weekly-market-summaries"
req = requests.get(url, headers)
soup = BeautifulSoup(req.content, 'html.parser')

href = []
names = []
for file in soup.find_all('p'):
    for list in file.find_all('a'):
        href.append(list.get('href'))
        names.append(list.string)
        
n=4
del names[-n:]
del href[-n:]

i=0
for x in href:
    filename = Path('./prices/'+names[i]+'.pdf')
    url = 'https://www.ontariosheep.org'+x
    response = requests.get(url)
    filename.write_bytes(response.content)
    i=i+1
    print(str(i)+' downloaded : '+str(filename))

print('All Done! '+str(i)+' files downloaded')
    
