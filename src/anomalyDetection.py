# coding: utf-8

# # Anomaly Detection Models

# In[1]:


get_ipython().magic(u'matplotlib inline')
import json, csv, sys, datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD, PCA
from sklearn import preprocessing
from sklearn.feature_extraction import DictVectorizer
from mpl_toolkits.mplot3d import Axes3D
from sklearn.neighbors import NearestNeighbors


# This function extracts the features specified in the array from the json file provided to it and stores it in a csv file at the location provided to it. 
# 
# Edit the file locations (source json; destination csv) and run the code to generate the requisite datasets.

# In[2]:



with open('../dataset/sample_first_50000.json', 'r') as file:
	i = 0
	j = 0
	# TODO: change list-based stuff to dict
	data = {}
	ipList = []
	# iterate over each logged line
	for line in file:
		newItem = {}
		try:
			jsonData = json.loads(line)
		except:
			print "\nLine {0} is not in JSON format".format(i)
			i += 1
			j += 1
			continue

		if 'data' in jsonData:
			timestamp = str(jsonData['data']['event_timestamp'])
			hour_of_the_day = (float(timestamp[11:13]) + float(timestamp[14:16])/60 + float(timestamp[17:19])/3600)
			# 0 - Monday; 6 - Sunday
			day_of_the_week = datetime.datetime(int(timestamp[:4]), 				int(timestamp[5:7]), int(timestamp[8:10]), int(timestamp[11:13]), 				int(timestamp[14:16]), int(timestamp[17:19])).weekday()
			newItem["hour_of_the_day"] = hour_of_the_day
			newItem["day_of_the_week"] = day_of_the_week
		
			featuresFromData = ["client_user", "client_host", "client_ip", "client_program", "CONNECT_DATA_INSTANCE_NAME", "service_name"]
			for feature in featuresFromData:
				if feature in jsonData['data']:
					newItem[feature] = str(jsonData['data'][feature])
				else:
					newItem[feature] = ""

		if 'metadata' in jsonData:
			featuresFromMetadata = ["oracle_sid", "hostname"]
			for feature in featuresFromMetadata:
				if feature in jsonData['metadata']:
					newItem[feature] = str(jsonData['metadata'][feature])
				else:
					newItem[feature] = ""

		# ignore cases where data is incomplete/very little to analyse
		if len(newItem) <= 2:
			continue

		else:
			data[i] = newItem
			ipList.append(newItem["client_ip"])
		# increment item number within the data
		i += 1

if j > 0:
	print "Could not store {0} lines due to invalid format".format(j)


# Write the data extracted from the json file into a csv file

# In[3]:


fieldNames = ['hour_of_the_day', 'day_of_the_week', 'client_user', 'client_host', 'client_ip', 'client_program', 'CONNECT_DATA_INSTANCE_NAME', 'service_name', 'oracle_sid', 'hostname']

with open('../dataset/preprocessed_first_50000.csv', 'w') as csvFile:
	writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
	writer.writeheader()
	
	for item in data:
		writer.writerow(data[item])
print"Data written to file."


# Read in the data and store it in a dataframe

# In[4]:


data = pd.read_csv('../dataset/preprocessed_first_50000.csv').fillna('0')
data = data.to_dict(orient='records')


# DictVectorizer allows us to transform categorical data into numerical format

# In[5]:


vec = DictVectorizer()
X = np.array(vec.fit_transform(data).toarray())


# Robust Scaling works better for large sparse matrices (?)

# In[6]:


X = preprocessing.robust_scale(X)
print "\nDimensions of feature matrix: ", X.shape
np.savetxt('../dataset/matX.txt', X)


# TruncatedSVD works better than PCA for our use-case

# In[7]:


svd = TruncatedSVD(n_components=2)
X_svd = svd.fit_transform(X)


# In[8]:


svd_3 = TruncatedSVD(n_components=3)
X_svd_3 = svd_3.fit_transform(X)


# Outcome of PCA similar to SVD, just to verify

# In[9]:


pca = PCA(n_components=2)
pca.fit(X)
X_pca = pca.transform(X)


# In[10]:


pca_3 = PCA(n_components=3)
pca_3.fit(X)
X_pca_3 = pca.transform(X)


# Visualisation of the data

# In[11]:


plt.scatter(X_pca[:, 0], X[:, 1])


# In[12]:


plt.scatter(X_svd[:, 0], X[:, 1])


# The following code attempts to perform K-Means Clustering on the data.

# In[17]:


from sklearn import cluster

k_means = cluster.MiniBatchKMeans(n_clusters=50)
k_means.fit_transform(X_svd)
labels = k_means.labels_
centroids = k_means.cluster_centers_

plt.scatter(X[:,0],X[:,1],c=k_means.labels_)


# In[ ]:


# Prepare sample data - normally distributed
vmin, vmax = -2, 2

# Create figure, add subplot with 3d projection
fig = plt.figure(figsize=(18, 18))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_xlim(vmin, vmax)
ax.set_ylim(vmin, vmax)
ax.set_zlim(vmin, vmax)

# Plot the data cloud
ax.scatter(X_svd_3[:, 0], X_svd_3[:, 1], X_svd_3[:, 2], s=.3, alpha=.1, edgecolor='b', facecolor='w', color='k')


# Let us now fit a KNN based model to our data

# In[ ]:


nbrs = NearestNeighbors(n_neighbors=50, algorithm='ball_tree').fit(X_svd)
distances, indices = nbrs.kneighbors(X_svd)
for i in xrange(5):
    print indices[i]
    print distances[i]


# In[ ]:


from sklearn import svm
from sklearn.model_selection import train_test_split

print "Started"


y = range(len(X_svd[:,0]))
X_svd_train, X_svd_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
print "Running"


# fit the model
clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
clf.fit(X_svd_train)
y_pred_train = clf.predict(X_svd_train)
y_pred_test = clf.predict(X_svd_test)
n_error_train = y_pred_train[y_pred_train == -1].size
n_error_test = y_pred_test[y_pred_test == -1].size
print "Running"
# plot the line, the points, and the nearest vectors to the plane
Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.title("Novelty Detection")
plt.contourf(xx, yy, Z, levels=np.linspace(Z.min(), 0, 7), cmap=plt.cm.PuBu)
a = plt.contour(xx, yy, Z, levels=[0], linewidths=2, colors='darkred')
plt.contourf(xx, yy, Z, levels=[0, Z.max()], colors='palevioletred')

s = 40
b1 = plt.scatter(X_svd_test[:, 0], X_svd_test[:, 1], c='white', s=s)
b2 = plt.scatter(X_svd_test[:, 0], X_svd_test[:, 1], c='blueviolet', s=s)
plt.axis('tight')
plt.xlim((-5, 5))
plt.ylim((-5, 5))
plt.legend([a.collections[0], b1, b2],
           ["learned frontier", "training observations",
            "new regular observations"],
           loc="upper left",
           prop=matplotlib.font_manager.FontProperties(size=11))
plt.xlabel(
    "error train: %d/200 ; errors novel regular: %d/40 ; "
    "errors novel abnormal: calculateOutliers/40"
    % (n_error_train, n_error_test))
plt.show()


# In[ ]:




