#!/usr/bin/python3

from bs4 import BeautifulSoup
import csv
import pandas as pd
import sys
import glob
import pymongo

#setting
input_dir = 'data_Juni_2019/banjarnegara-kml'
outname_suffix = 'banjarnegara'

if len(sys.argv) > 2:
	input_dir = sys.argv[1]
	outname_suffix = sys.argv[2]

all_kml = glob.glob(input_dir+'/*.kml')
print(all_kml)
for i in range(len(all_kml)):
	waktu_data = all_kml[i].split('/')[-1][:-4]
	filename_output =  '%s-%s.csv'%(outname_suffix, waktu_data)
	print(filename_output)

client = pymongo.MongoClient()
collection = client['geod_achieve']['petir']
