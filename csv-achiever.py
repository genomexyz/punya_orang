#!/usr/bin/python3

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import csv
import sys
import glob
import pymongo
import pandas as pd
import numpy as np

#setting
input_dir = '/home/genomexyz/sulkhi/data_Juni_2019/Bandung-csv'
lokasi = 'bandung'

if len(sys.argv) > 2:
	input_dir = sys.argv[1]
	lokasi = sys.argv[2]

client = pymongo.MongoClient()
collection = client['geof_achieve']['petir']

all_csv = glob.glob(input_dir+'/*.csv')
for i in range(len(all_csv)):
	csv_open = open(all_csv[i])
	csv_array = csv_open.read().split('\n')[1:]
	if csv_array[-1] == '':
		csv_array = csv_array[:-1]
	for j in range(len(csv_array)):
		csv_array[j] = csv_array[j].split(',')
	for j in range(len(csv_array)):
		data_row =  csv_array[j]
		waktu = data_row[2].strip()
		waktu = waktu.split(' ')
		tanggal = waktu[0]
		jammenit = waktu[1]
		tanggal = tanggal.split('-')
		jammenit = jammenit.split(':')
		try:
			tahun = int(tanggal[0])
			bulan = int(tanggal[1])
			hari = int(tanggal[2])
			jam = int(jammenit[0])
			menit = int(jammenit[1])
		except ValueError:
			print('kesalahan pada format waktu, lanjutkan...')
			continue
		section_menit = menit // 15
		mod_section_menit = menit % 15
		if section_menit == 3 and (mod_section_menit > 7):
			waktu_baru = datetime(tahun, bulan, hari, jam, 0)
			waktu_baru = waktu_baru + timedelta(hours=1)
			tahun = waktu_baru.year
			bulan = waktu_baru.month
			hari = waktu_baru.day
			jam = waktu_baru.hour
			menit = waktu_baru.minute
		elif mod_section_menit > 7:
			section_menit += 1	
			menit = section_menit * 15
		else:
			menit = section_menit * 15
		try:
			lat = float(data_row[3])
			lon = float(data_row[4])
		except ValueError:
			print('kesalahan pada angka lintang dan bujur, lanjutkan...')
			continue
		jenis_petir = data_row[-1]
		print(lokasi, tahun, bulan, hari, jam, menit, lat, lon, jenis_petir)
		collection.insert_one({'lokasi' : lokasi, 'tahun' : tahun, 'bulan' : bulan, 'hari' : hari, 'jam' : jam, 'menit' : menit,
		'latitude' : lat, 'longitude' : lon, 'jenis_petir' : jenis_petir})
