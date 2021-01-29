import requests
from bs4 import BeautifulSoup
import tabula
import pandas as pd
import os
import logging
import csv
import csvsingle
from datetime import date

"""
to do:
2 a. insert into database
  b. import CSV into database instead
3 a. check with jenny on what data to pull out

"""

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
logging.debug('href = '+str(len(href)))

# remove 4 from the bottom for extraniuos links
n=4
del names[-n:]
del href[-n:]
logging.debug('href = '+str(len(href)))

"""
# remove week num from top to only get 1 week from this year
today= date.today()
weeknum = int(today.strftime("%W"))-1
logging.debug('Weeknum = '+str(weeknum))
names = names[weeknum:]
href = href[weeknum:]
logging.debug('href = '+str(len(href)))

# remove previous years from bottom
n=312
del names[-n:]
del href[-n:]
logging.debug('href = '+str(len(href)))
"""

logging.info('Got list of files to download, total of '+str(len(href)))

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
        n=n+1
    logging.info(str(n)+' weeks saved')
    
for x in href:
    url = 'https://www.ontariosheep.org'+x

    csvout(outcsv)
    
    name = names[i]
    i=i+1
    logging.info(str(i)+' converted : '+str(name))
    
    csvsingle.csvstrings(all,olex,osi)
    logging.info('collected: '+name)

logging.info(str(i)+' files downloaded and converted')

n=0
mastercsv(all,olex,osi,n)
logging.info('All Done!')
    
