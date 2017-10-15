#!/usr/bin/env python

import sys, csv, pandas

if __name__ == '__main__':
	# read the csv data
	dataFrame = pandas.read_csv(sys.argv[1], delimiter=',').fillna(value=0.0)
	#print dataFrame
	columns = list(dataFrame)
	anomalies = {}
	# iterate over the entire data
	for i in xrange(len(dataFrame)-1):
		df = dataFrame[i:i+1]

		tmp_df = abs(dataFrame - df.iloc[0])
		tmp_df = tmp_df.drop(dataFrame.index[i])
		min_weight = tmp_df.sum(axis=1).min()

		# detect anomalies
		if min_weight >= 15.0:
			print "Anomaly found at index ", i
			anomalies[i] = min_weight

	for index in anomalies:
		print "\n\nAnomaly at : ", dataFrame.iloc[index]