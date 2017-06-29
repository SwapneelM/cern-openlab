#!/usr/bin/env/python
'''
arguments : [path_to_stored_json][csv_storage_filename]
'''
import json, csv, sys, datetime

def newConnection(items, newItem):
	for item in items:
		# match the ip address or the client user 
		# in case ip is absent
		if "client_user" in items[item] and "client_user" in newItem:
				if items[item]["client_user"] == newItem["client_user"]:
					return False
		'''
		elif "client_ip" in items[item] and "client_ip" in newItem:
				if items[item]["client_ip"] == newItem["client_ip"]:
					return False
		elif "client_host" in items[item] and "client_host" in newItem:
				if items[item]["client_host"] == newItem["client_host"]:
					return False
		'''
	return True

def extract(filename):

	with open(filename, 'r') as file:
		i = 0
		j = 0
		# TODO: change list-based stuff to dict
		data = {}

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
				
				if 'client_ip' in jsonData['data']:
					#print "\nclient_ip: ", jsonData['data']['client_ip']
					client_ip = str(jsonData['data']['client_ip'])
					newItem["client_ip"] = client_ip

				if 'client_user' in jsonData['data']:
					#print "\nclient_user: ", jsonData['data']['client_user']
					client_user = str(jsonData['data']['client_user'])
					newItem["client_user"] = client_user
				
				if 'client_host' in jsonData['data']:
					#print "\nclient_host: ", jsonData['data']['client_host']
					client_host = str(jsonData['data']['client_host'])
					newItem["client_host"] = client_host

				if 'client_program' in jsonData['data']:
					#print "\nclient_program: ", jsonData['data']['client_program']
					client_program = str(jsonData['data']['client_program'])
					newItem["client_program"] = client_program

				if 'service_name' in jsonData['data']:
					#print "\nservice_name: ", jsonData['data']['service_name']
					newItem["service_name"] = str(jsonData['data']['service_name'])
					
			
			# print "\nNew Data :", newItem
			
			# ignore cases where data is incomplete/very little to analyse
			if len(newItem) <= 2:
				continue

			else:
				data[i] = newItem

			# increment item number within the data
			i += 1
	return data

def writeToFile(filename, data):

	fieldNames = ['hour_of_the_day', 'day_of_the_week', 'client_user', 'client_host', 'client_ip', 'client_program', 'service_name']
	
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
	print "Could not store {0} lines due to invalid format".format(j)
