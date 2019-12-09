#!/usr/bin/python3

from sklearn.cluster import OPTICS
from sklearn import metrics
import numpy as np
import pymongo
import sys
import matplotlib.pyplot as plt

#setting
tahun = 2019
bulan = 6
hari = 4
jam = 3
menit = 0
tipe_sambaran1 = 'CGPositive'
tipe_sambaran2 = '0'
#tipe_sambaran1 = 'CGNegative'
#tipe_sambaran2 = '1'

#catatan
#0 = CG+
#1 = CG-
#2 = intercloud or cloud to cloud

if len(sys.argv) > 7:
	tahun = int(sys.argv[1])
	bulan = int(sys.argv[2])
	hari = int(sys.argv[3])
	jam = int(sys.argv[4])
	menit = int(sys.argv[5])
	tipe_sambaran1 = sys.argv[6]
	tipe_sambaran2 = sys.argv[7]

client = pymongo.MongoClient()
collection = client['geof_achieve']['petir']

documents = list(collection.find({'tahun' : tahun, 'bulan' : bulan, 'hari' : hari, 'jam' : jam, 'menit' : menit, '$or' : [{'jenis_petir' : tipe_sambaran1}, {'jenis_petir' : tipe_sambaran2}]}))
latlon = []
for i in range(len(documents)):
	lat = documents[i]['latitude']
	lon = documents[i]['longitude']
	latlon.append([lat, lon])
latlon = np.asarray(latlon)
db = OPTICS(eps=0.3, min_samples=5).fit(latlon)

total_cluster = np.max(db.labels_)+1
group_cluster = {}
for i in range(total_cluster):
	group_cluster[i] = []
group_cluster[-1] = []

for i in range(len(db.labels_)):
	group = db.labels_[i]
	group_cluster[group].append(latlon[i])

for i in range(total_cluster):
	group_cluster[i] = np.asarray(group_cluster[i])
group_cluster[-1] = np.asarray(group_cluster[-1])

rata_koordinat = np.zeros((total_cluster, 2))
for i in range(len(rata_koordinat)):
	rata_koordinat[i,0] = np.mean(group_cluster[i][:,0])
	rata_koordinat[i,1] = np.mean(group_cluster[i][:,1])

print('RATA-RATA cluster')
print(rata_koordinat)
