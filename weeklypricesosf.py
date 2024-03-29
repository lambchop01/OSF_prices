# bash command to run: bash /home/kevin/scripts/OSF_prices/osfprices.sh
import requests
from bs4 import BeautifulSoup
import tabula
import pandas as pd
import os
import logging
import csv
import csvsingle
from datetime import date
import pymysql.cursors
import gspread
from oauth2client.service_account import ServiceAccountCredentials


logging.basicConfig(filename='prices.log', filemode='a',format='%(asctime)s - %(message)s',level=logging.DEBUG)
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
logging.debug('remove '+str(n)+' href from bottom of the list, remaining = '+str(len(href)))


# remove week num from top to only get 1 week from this year
today= date.today()
weeknum = int(today.strftime("%W")) -1 +1 #1 weird extra...
if weeknum < 0:
  weeknum = 0
logging.debug('Weeknum = '+str(weeknum))
names = names[weeknum:]
href = href[weeknum:]
logging.debug('removed weeknum from top, remaining = '+str(len(href)))

# remove previous years from bottom
year = int(today.strftime("%Y"))
n=(year - 2015)*52
del names[-n:]
del href[-n:]
logging.debug('removed '+str(n)+' from bottom for previous year, remaining = '+str(len(href)))


logging.info('Got list of files to download, total of '+str(len(href)))

outcsv = 'output.csv'
i=0
all = []
olex = []
osi = []

def csvout(outcsv):
    tabula.convert_into(url, outcsv, output_format="csv", pages="all", guess=False, lattice=True)
#    df = tabula.read_pdf(url, encoding='utf-8', spreadsheet=True )
#    df.to_csv('output.csv', encoding='utf-8')

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
    logging.info(str(n)+' weeks processed')

def executeSql(sql):
    mariadb = pymysql.connect(
        host    = '192.168.2.16',
        port    = int('3306'),
        user    = 'prices',
        password= 'klamb',
        db      = 'osfprices',
        charset ='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with mariadb.cursor() as cursor:
            cursor.execute(sql)
        mariadb.commit()
    finally:
        mariadb.close()

def sheets(all, olex, osi): # Connect to Google Sheets
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive"]
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name("osf-cred.json", scope)
    gc = gspread.authorize(credentials)
    
    spreadsheetId = "1kRogkgxS1NJNxH2BYBI0mfI-xZ73B_sa0WgB1BiNfTM"
    
    # all prices
    list = [l.split(',') for l in ','.join(all).split('|')]
    logging.debug(list)
    range = "all!A:A";
    params = {
        "valueInputOption" : "USER_ENTERED"
    } 
    body = {
      "majorDimension": "ROWS",
      "values": list
    }
    sht = gc.open_by_key(spreadsheetId)
    response = sht.values_append(range, params, body)

    # olex prices
    list = [l.split(',') for l in ','.join(olex).split('|')]
    logging.debug(list)
    range = "olex!A:A";
    params = {
        "valueInputOption" : "USER_ENTERED"
    } 
    body = {
      "majorDimension": "ROWS",
      "values": list
    }
    sht = gc.open_by_key(spreadsheetId)
    response = sht.values_append(range, params, body)

    # osi prices
    list = [l.split(',') for l in ','.join(osi).split('|')]
    logging.debug(list)
    range = "osi!A:A";
    params = {
        "valueInputOption" : "USER_ENTERED"
    } 
    body = {
      "majorDimension": "ROWS",
      "values": list
    }
    sht = gc.open_by_key(spreadsheetId)
    response = sht.values_append(range, params, body)
    logging.info('Saved to Google Sheets')



def database(all, olex, osi):
    n=0
    for x in all:
        sql = ("INSERT IGNORE INTO `osfprices`.`all` " + "VALUES ("+x+")")
        n=n+1
        logging.debug(str(n)+' done:'+sql)
        executeSql(sql)
    logging.info('all prices uploaded to database')
    n=0
    for x in olex:
        sql = ("INSERT IGNORE INTO `osfprices`.`olex` " + "VALUES ("+x+")")
        n=n+1
        logging.debug(str(n)+' done:'+sql)
        executeSql(sql)
    logging.info('olex prices uploaded to database')
    n=0
    for x in osi:
        sql = ("INSERT IGNORE INTO `osfprices`.`osi` " + "VALUES ("+x+")")
        n=n+1
        logging.debug(str(n)+' done:'+sql)
        executeSql(sql)
    logging.info('osi prices uploaded to database')

def notification(message):
    requests.post('https://push.lambspork.ca/message?token=AqyLPxGXB..MSuT', data={'title':'OSF Prices','message':message, 'priority':'2'})
    
for x in href:
    url = 'https://www.ontariosheep.org'+x

    csvout(outcsv)
    
    name = names[i]
    i=i+1
    
    csvsingle.csvstrings(all,olex,osi)
    logging.info(str(i)+' converted : '+str(name))

message = (str(i)+' files downloaded and converted')
logging.info(message)


n=0
mastercsv(all,olex,osi,n)
#database(all,olex,osi) #upload to database
sheets(all,olex,osi) #uplaod to google sheets, requires "osf-cred.json"
logging.info('All Done!')
message = message + ', All done!'
notification(message)
    