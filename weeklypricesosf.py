import requests
from bs4 import BeautifulSoup
import tabula
import pandas as pd
import os
import logging
import csv
import csvsingle

logging.basicConfig(filename='prices.log', filemode='a',format='%(asctime)s - %(message)s',level=logging.INFO)
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

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
logging.info('Got list of files to download')

outcsv = 'output.csv'
i=0
all = []
olex = []
osi = []

def csvout(outcsv):
    tabula.convert_into(url, outcsv, output_format="csv", pages="all", guess=False, lattice=True)

def mastercsv(all,olex,osi,n):
    for week in all:
        f = open('allprices.csv','a+')
        f.write(week+'\r\n')
        f.close
    for week in olex:
        f = open('olexprices.csv','a+')
        f.write(week+'\r\n')
        f.close
    for week in osi:
        f = open('osiprices.csv','a+')
        f.write(week+'\r\n')
        f.close
    logging.info(str(n)+' weeks saved')
    
for x in href:
    url = 'https://www.ontariosheep.org'+x

    csvout(outcsv)
    
    name = names[i]
    i=i+1
    logging.info(str(i)+' converted : '+str(name))
    
    csvsingle.csvstrings(all,olex,osi)
    logging.debug(all)
    logging.info('collected: '+name)

logging.info(str(i)+' files downloaded and converted')

n=1
mastercsv(all,olex,osi,n)
logging.info('All Done!')
   
print('All Done! '+str(i)+' files downloaded')
    
