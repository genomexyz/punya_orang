#!/usr/bin/python3

from sklearn.cluster import DBSCAN
from sklearn import metrics
import numpy as np
import pymongo
import sys
import matplotlib.pyplot as plt

#setting
tahun = 2019
bulan = 6
hari = 5
jam = 3
menit = 0 

if len(sys.argv) > 5:
	tahun = int(sys.argv[1])
	bulan = int(sys.argv[2])
	hari = int(sys.argv[3])
	jam = int(sys.argv[4])
	menit = int(sys.argv[5])

client = pymongo.MongoClient()
collection = client['geof_achieve']['petir']

documents = list(collection.find({'tahun' : tahun, 'bulan' : bulan, 'hari' : hari, 'jam' : jam, 'menit' : menit}))
latlon = []
for i in range(len(documents)):
	lat = documents[i]['latitude']
	lon = documents[i]['longitude']
	latlon.append([lat, lon])
latlon = np.asarray(latlon)
db = DBSCAN(eps=0.3, min_samples=10).fit(latlon)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)
# #############################################################################
# Plot result
# Black removed and is used for noise instead.

unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
		  for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
	if k == -1:
		# Black used for noise.
		col = [0, 0, 0, 1]

	class_member_mask = (labels == k)

	xy = latlon[class_member_mask & core_samples_mask]
	plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
			 markeredgecolor='k', markersize=14)

	xy = latlon[class_member_mask & ~core_samples_mask]
	plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
			 markeredgecolor='k', markersize=6)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()
