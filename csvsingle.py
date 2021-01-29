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
    date = dateobj.strftime("%Y-%m-%d %H:%M:%S.%f")
    # headers --> date, 80-94, hd, price, weight, 95-109, hd, price, weight, 110+, hd, price, weight, sheep, hd, price, weight
    all.append(date+',80-94lbs,'+g[8][1]+','+g[8][2].replace('-','')+','+g[8][3].replace('-','')+',95-109lbs,'+g[9][1]+','+g[9][2].replace('-','')+','+g[9][3].replace('-','')+',110+lbs,'+g[10][1]+','+g[10][2].replace('-','')+','+g[10][3].replace('-','')+',sheep,'+g[11][1]+','+g[11][2].replace('-','')+','+g[11][3].replace('-',''))
    olex.append(date+',80-94lbs,'+g[35][1]+','+g[35][2].replace('-','')+','+g[35][3].replace('-','')+',95-109lbs,'+g[36][1]+','+g[36][2].replace('-','')+','+g[36][3].replace('-','')+',110+lbs,'+g[37][1]+','+g[37][2].replace('-','')+','+g[37][3].replace('-','')+',sheep,'+g[38][1]+','+g[38][2].replace('-','')+','+g[38][3].replace('-',''))
    osi.append(date+',80-94lbs,'+g[35][4]+','+g[35][5].replace('-','')+','+g[35][6].replace('-','')+',95-109lbs,'+g[36][4]+','+g[36][5].replace('-','')+','+g[36][6].replace('-','')+',110+lbs,'+g[37][4]+','+g[37][5].replace('-','')+','+g[37][6].replace('-','')+',sheep,'+g[38][4]+','+g[38][5].replace('-','')+','+g[38][6].replace('-',''))
