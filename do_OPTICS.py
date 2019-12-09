#!/usr/bin/python3

from sklearn.cluster import DBSCAN, OPTICS
from sklearn import metrics
#import tkinter as tk
import numpy as np
import pymongo
import sys
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import pandas as pd
import json

#setting
tahun = 2019
bulan = 6
hari = 5
jam = 3
menit = 0 
jenis_petir1 = 'CGPositive'
jenis_petir2 = '0'
#jenis petir
#0 = CGPositive
#1 = CGNegative
#2 = between cloud

def convert(o):
	if isinstance(o, np.int64): return int(o)  
	raise TypeError

if len(sys.argv) > 7:
	tahun = int(sys.argv[1])
	bulan = int(sys.argv[2])
	hari = int(sys.argv[3])
	jam = int(sys.argv[4])
	menit = int(sys.argv[5])
	jenis_petir1 = sys.argv[6]
	jenis_petir2 = sys.argv[7]
elif len(sys.argv) > 6:
	tahun = int(sys.argv[1])
	bulan = int(sys.argv[2])
	hari = int(sys.argv[3])
	jam = int(sys.argv[4])
	menit = int(sys.argv[5])
	jenis_petir1 = sys.argv[6]

client = pymongo.MongoClient()
collection = client['geof_achieve']['petir']

if len(sys.argv) > 7:
	documents = list(collection.find({'tahun' : tahun, 'bulan' : bulan, 'hari' : hari, 'jam' : jam, 'menit' : menit,
	'$or' : [{'jenis_petir' : jenis_petir1}, {'jenis_petir' : jenis_petir2}]}))
elif len(sys.argv) > 6:
	documents = list(collection.find({'tahun' : tahun, 'bulan' : bulan, 'hari' : hari, 'jam' : jam, 'menit' : menit,
	'jenis_petir' : jenis_petir1}))
else:
	documents = list(collection.find({'tahun' : tahun, 'bulan' : bulan, 'hari' : hari, 'jam' : jam, 'menit' : menit,
	'$or' : [{'jenis_petir' : jenis_petir1}, {'jenis_petir' : jenis_petir2}]}))
latlon = []
for i in range(len(documents)):
	lat = documents[i]['latitude']
	lon = documents[i]['longitude']
	latlon.append([lon, lat])
latlon = np.asarray(latlon)
clust = OPTICS(eps=0.5, min_samples=10).fit(latlon)

#plot
space = np.arange(len(latlon))
reachability = clust.reachability_[clust.ordering_]
labels = clust.labels_[clust.ordering_]
true_label = clust.labels_
print(true_label)

fig = plt.figure(figsize=(10, 10))
G = gridspec.GridSpec(2, 2)
ax1 = plt.subplot(G[0, :])
ax2 = plt.subplot(G[1, :])

# Reachability plot
colors = ['g.', 'r.', 'b.', 'y.', 'c.']
for klass, color in zip(range(0, 5), colors):
    Xk = space[labels == klass]
    Rk = reachability[labels == klass]
    ax1.plot(Xk, Rk, color, alpha=1)
ax1.plot(space[labels == -1], reachability[labels == -1], 'k.', alpha=0.3)
ax1.plot(space, np.full_like(space, 2., dtype=float), 'k-', alpha=0.5)
ax1.plot(space, np.full_like(space, 0.5, dtype=float), 'k-.', alpha=0.5)
ax1.set_ylabel('Reachability (epsilon distance)')
ax1.set_title('Reachability Plot')

if bulan < 10:
	bulan = '0'+str(bulan)

if hari < 10:
	hari = '0'+str(hari)

if jam < 10:
	jam = '0'+str(jam)

if menit < 10:
	menit = '0'+str(menit)

if jenis_petir1 == '2':
	jenis_petir1 = 'Clout-to-Cloud_In-Cloud'

# OPTICS
#colors = ['g.', 'r.', 'b.', 'y.', 'c.']
#for klass, color in zip(range(0, 5), colors):
#	Xk = latlon[clust.labels_ == klass]
#	ax2.plot(Xk[:, 0], Xk[:, 1], color, alpha=0.8)
#ax2.plot(latlon[clust.labels_ == -1, 0], latlon[clust.labels_ == -1, 1], 'k+', alpha=0.3)
#ax2.set_title('Automatic Clustering\nOPTICS')
#ax2.set_title('Clustering %s%s%s%s%s\n%s'%(tahun, bulan, hari, jam, menit, jenis_petir1))

#plt.tight_layout()
#fig.savefig('output/%s%s%s%s%s-%s.png'%(tahun, bulan, hari, jam, menit, jenis_petir1), bbox_inches='tight')


#save JSON
#total_cluster = np.max(clust.labels_)+1
#group_cluster = {}
#for i in range(len(latlon)):
#	group_cluster['%s,%s'%(latlon[i,1], latlon[i,0])] = clust.labels_[i]


#json_save = json.dumps(group_cluster, default=convert)
#data_save = open('output/%s%s%s%s%s-%s.json'%(tahun, bulan, hari, jam, menit, jenis_petir1), 'w')
#data_save.write(json_save)

#save to MongoDB
coll_save = client['geof_achieve']['cluster']
array_dict_save = []
for i in range(len(true_label)):
	data_save = {'tahun' : int(tahun), 'bulan' : int(bulan), 'hari' : int(hari), 'jam' : int(jam), 'menit' : int(menit), 
	'latitude' : float(latlon[i,1]), 'longitude' : float(latlon[i,0]), 'jenis_petir' : jenis_petir1, 'cluster_index' : int(true_label[i])}
	array_dict_save.append(data_save)

saved_data = coll_save.insert_many(array_dict_save)
print(saved_data)

