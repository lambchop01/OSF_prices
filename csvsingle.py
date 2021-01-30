import os
import csv
import logging
import datetime

#"September 18, 2017, 22:19:55" -> "%B %d, %Y, %H:%M:%S"

def csvstrings(all,olex,osi):
    filename = 'output.csv'
    
    # saves g as g[row][column] with 0 as row/column 1
    with open(filename) as csvDataFile:
        g=list(csv.reader(csvDataFile))
    dateobj = datetime.datetime.strptime(g[1][2], '%B %d, %Y')
    
    #all
    date = dateobj.strftime("'%Y-%m-%d'")+','
    lowhd = g[8][1]+','
    lowprice = str(float('0'+g[8][2].replace('-',''))/100)+','
    lowweight = g[8][8].replace('-','')+','
    medhd = g[9][1]+','
    medprice = str(float('0'+g[9][2].replace('-',''))/100)+','
    medweight = g[9][8].replace('-','')+','
    highhd = g[10][1]+','
    highprice = str(float('0'+g[10][2].replace('-',''))/100)+','
    highweight = g[10][8].replace('-','')+','
    sheephd = g[11][1]+','
    sheepprice = str(float('0'+g[10][2].replace('-',''))/100)+','
    sheepweight = g[11][8].replace('-','')
    
    str1 = date+lowhd+lowprice+lowweight+medhd+medprice+medweight+highhd+highprice+highweight+sheephd+sheepprice+sheepweight
    str2 = str1.replace(',,',',0,')
    str3 = str2.replace(',,',',0,')
    if (str3[-1] == ","):
        str4 = str3+'0'
    else: str4 = str3
    all.append(str4)
    
    #olex
    date = dateobj.strftime("'%Y-%m-%d'")+','
    lowhd = g[35][4]+','
    lowprice = str(float('0'+g[35][5].replace('-',''))/100)+','
    lowweight = g[35][6].replace('-','')+','
    medhd = g[36][4]+','
    medprice = str(float('0'+g[36][5].replace('-',''))/100)+','
    medweight = g[36][6].replace('-','')+','
    highhd = g[37][4]+','
    highprice = str(float('0'+g[37][5].replace('-',''))/100)+','
    highweight = g[37][6].replace('-','')+','
    sheephd = g[38][4]+','
    sheepprice = str(float('0'+g[38][5].replace('-',''))/100)+','
    sheepweight = g[38][6].replace('-','')
    
    str1 = date+lowhd+lowprice+lowweight+medhd+medprice+medweight+highhd+highprice+highweight+sheephd+sheepprice+sheepweight
    str2 = str1.replace(',,',',0,')
    str3 = str2.replace(',,',',0,')
    if (str3[-1] == ","):
        str4 = str3+'0'
    else: str4 = str3
    olex.append(str4)
    
    #osi
    date = dateobj.strftime("'%Y-%m-%d'")+','
    lowhd = g[35][7]+','
    lowprice = str(float('0'+g[35][8].replace('-',''))/100)+','
    lowweight = g[35][9].replace('-','')+','
    medhd = g[36][7]+','
    medprice = str(float('0'+g[36][8].replace('-',''))/100)+','
    medweight = g[36][9].replace('-','')+','
    highhd = g[37][7]+','
    highprice = str(float('0'+g[37][8].replace('-',''))/100)+','
    highweight = g[37][9].replace('-','')+','
    sheephd = g[38][7]+','
    sheepprice = str(float('0'+g[38][8].replace('-',''))/100)+','
    sheepweight = g[38][9].replace('-','')
    
    str1 = date+lowhd+lowprice+lowweight+medhd+medprice+medweight+highhd+highprice+highweight+sheephd+sheepprice+sheepweight
    str2 = str1.replace(',,',',0,')
    str3 = str2.replace(',,',',0,')
    if (str3[-1] == ","):
        str4 = str3+'0'
    else: str4 = str3
    osi.append(str4)
    
    
all=[]
olex=[]
osi=[]
csvstrings(all, olex, osi)
