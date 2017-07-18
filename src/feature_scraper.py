#!/usr/bin/env python
'''
arguments : [path_to_stored_json][csv_storage_filename]
'''
import json, csv, sys, datetime

def extract(filename):

	with open(filename, 'r') as file:
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
				day_of_the_week = datetime.datetime(int(timestamp[:4]), \
					int(timestamp[5:7]), int(timestamp[8:10]), int(timestamp[11:13]), \
					int(timestamp[14:16]), int(timestamp[17:19])).weekday()
				newItem["hour_of_the_day"] = hour_of_the_day
				newItem["day_of_the_week"] = day_of_the_week
			
				featuresFromData = ["client_user", "client_host", "client_ip", "CONNECT_DATA_SERVICE_NAME", "client_program", "CONNECT_DATA_INSTANCE_NAME", "service_name"]
				for feature in featuresFromData:
					if feature in jsonData['data']:
						newItem[feature] = str(jsonData['data'][feature])
					else:
						newItem[feature] = ""

			if 'metadata' in jsonData:
				featuresFromMetadata = ["oracle_sid", "hostname", "type"]
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
	return data

def writeToFile(filename, data):

	fieldNames = ['hour_of_the_day', 'day_of_the_week', 'client_user', 'client_host', 'client_ip', 'CONNECT_DATA_SERVICE_NAME', 'client_program', 'CONNECT_DATA_INSTANCE_NAME', 'service_name', 'oracle_sid', 'hostname', 'type']
	
	with open(filename, 'w') as csvFile:
		writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
		writer.writeheader()
		
		for item in data:
			writer.writerow(data[item])
	pass

if __name__ == '__main__':
	
	data = extract(sys.argv[1])
	writeToFile(sys.argv[2], data)
	print "Data stored in file"
