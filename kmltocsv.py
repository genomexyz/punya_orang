#!/usr/bin/python3

from bs4 import BeautifulSoup
import csv
import pandas as pd
import sys
import glob

#setting
input_dir = 'data_Juni_2019/banjarnegara-kml'
outname_suffix = 'banjarnegara'
outdir = 'allcsv'

if len(sys.argv) > 2:
	input_dir = sys.argv[1]
	outname_suffix = sys.argv[2]


def process_coordinate_string(str):
    space_splits = str.split(",")
    ret = []
    ret.append(space_splits[1])    # lat
    ret.append(space_splits[0])    # lng
    
    return ret

def main():
	"""
	Open the KML. Read the KML. Open a CSV file. Process a coordinate string to be a CSV row.
	"""
	waktu = "azz"
	jenis = "aaaa"

	all_kml = glob.glob(input_dir+'/*.kml')
	for i in range(len(all_kml)):
		lat = []
		lon = []
		time = []
		jenispetir = []
		waktu_data = all_kml[i].split('/')[-1][:-4]
		filename_output =  '%s-%s.csv'%(outname_suffix, waktu_data)
		print('processing %s...'%(all_kml[i]))
		with open(all_kml[i], 'r') as f:
			s = BeautifulSoup(f, 'xml')
			for coords in s.find_all(['coordinates', 'name', 'styleUrl']):
				umpan = coords.name
				if umpan[0:2]=="na":
					waktu=coords.string
				elif umpan[0:3]=="sty":
					jenis=coords.string
				elif umpan[0:2]=="co":
					jadi = process_coordinate_string(coords.string)
					lat.append(jadi[0])
					lon.append(jadi[1])
					time.append(waktu)
					jenispetir.append(jenis)
			lat = pd.DataFrame(lat)
			lon = pd.DataFrame(lon)
			time = pd.DataFrame(time)
			jenis = pd.DataFrame(jenispetir)
			nah = pd.concat([lat, lon, time, jenis], axis=1)
			nah.to_csv(outdir+'/'+filename_output, sep=',', index=False)   


if __name__ == "__main__":
    main()
