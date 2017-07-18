import pandas as pd 
import os, sys
import json, csv
from sklearn.feature_extraction import DictVectorizer
from sklearn import preprocessing
import numpy as np

"""
argument [path_to_csv]
"""

if __name__ == '__main__':
	# data = np.genfromtxt(sys.argv[1], delimiter=',')
	data = pd.read_csv(sys.argv[1]).fillna('0')
	data.drop('type', axis=1)
	data = data.to_dict(orient='records')

	vec = DictVectorizer()
	featureMatrix = np.array(vec.fit_transform(data).toarray())

	X_scaled = preprocessing.robust_scale(featureMatrix)
	print "\nDimensions of feature matrix: ", X_scaled.shape

	for i in X_scaled:
		print i 
		print "\n"

	try:
		knn(X_scaled)
		# ocsvm(X_scaled)
	except:
		print "\nCould not complete running models on data"