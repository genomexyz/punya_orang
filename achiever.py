#!/usr/bin/python3

from bs4 import BeautifulSoup
import csv
import sys
import glob
import pymongo
import pandas as pd
import numpy as np

#setting
input_dir = 'allcsv'

client = pymongo.MongoClient()
collection = client['geof_achieve']['petir']

all_csv = glob.glob(input_dir+'/*.csv')
for i in range(len(all_csv)):
	lokasitanggal = all_csv[i].split('/')[-1][:-4]
	lokasitanggal = lokasitanggal.split('-')

	lokasi = lokasitanggal[0]
	tanggal = lokasitanggal[1]

	tahun = int(tanggal[:4])
	bulan = int(tanggal[4:6])
	hari = int(tanggal[6:8])

	dataset_open = open(all_csv[i])
	dataset_array = dataset_open.read().split('\n')[1:]
	if dataset_array[-1] == '':
		dataset_array = dataset_array[:-1]
	for j in range(len(dataset_array)):
		dataset_array[j] = dataset_array[j].split(',')

	for j in range(len(dataset_array)):
		data_row = dataset_array[j]
		jammenit = data_row[2].split('-')[-1].strip()
		jammenit = jammenit.split(':')
		try:
			jam = int(jammenit[0])
			menit = int(jammenit[1][:2])
		except ValueError:
			print(jammenit)
			print('data waktu error, lanjutkan...')
			continue
		ampm = jammenit[1][-2:]
		if ampm.upper() == 'AM':
			pass
		elif ampm.upper() == 'PM':
			jam += 12
		else:
			print('penanda waktu AM atau PM tidak valid, lanjutkan...')
			continue
		if jam > 24:
			print('perhitungan waktu error (jam=%i), lanjutkan...'%(jam))
			continue
		try:
			lat = float(data_row[0])
			lon = float(data_row[1])
		except ValueError:
			print('lat atau lon tidak valid, lanjutkan...')
			continue
		jenis_petir = data_row[-1]
		print(lokasi, tahun, bulan, hari, jam, menit, lat, lon, jenis_petir)
		collection.insert_one({'lokasi' : lokasi, 'tahun' : tahun, 'bulan' : bulan, 'hari' : hari, 'jam' : jam, 'menit' : menit,
		'latitude' : lat, 'longitude' : lon, 'jenis_petir' : jenis_petir})
