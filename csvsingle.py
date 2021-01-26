import os
import csv
import logging


def csvstrings(all,olex,osi):
    filename = 'output.csv'
    
    # saves g as g[row][column] with 0 as row/column 1
    with open(filename) as csvDataFile:
        g=list(csv.reader(csvDataFile))
    # headers --> date, 80-94, hd, price, 95-109, hd, price, 110+, hd, price, sheep, hd, price
    all.append(g[1][2].replace(',','')+',80-94lbs,'+g[8][1]+','+g[8][2].replace('-','')+',95-109lbs,'+g[9][1]+','+g[9][2].replace('-','')+',110+lbs,'+g[10][1]+','+g[10][2].replace('-','')+',sheep,'+g[11][1]+','+g[11][2].replace('-',''))
    logging.debug(all)
    olex.append(g[1][2].replace(',','')+',80-94lbs,'+g[35][1]+','+g[35][2].replace('-','')+',95-109lbs,'+g[36][1]+','+g[36][2].replace('-','')+',110+lbs,'+g[37][1]+','+g[37][2].replace('-','')+',sheep,'+g[38][1]+','+g[38][2].replace('-',''))
    logging.debug(olex)
    osi.append(g[1][2].replace(',','')+',80-94lbs,'+g[35][4]+','+g[35][5].replace('-','')+',95-109lbs,'+g[36][4]+','+g[36][5].replace('-','')+',110+lbs,'+g[37][4]+','+g[37][5].replace('-','')+',sheep,'+g[38][4]+','+g[38][5].replace('-',''))
    logging.debug(osi)
    
