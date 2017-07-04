#!/usr/bin/env python
'''
arguments : [path_to_stored_json]
'''
import json, csv, sys, datetime

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
	if j > 0:
		print "Could not store {0} lines due to invalid format".format(j)
	return data

def writeToFile(filename, data):

	fieldNames = ['hour_of_the_day', 'day_of_the_week', 'client_user', 'client_host', 'client_ip', 'client_program', 'service_name']
	
	with open(filename, 'w') as csvFile:
		writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
		writer.writeheader()
		
		for item in data:
			writer.writerow(data[item])
	pass

def preprocess(sourceFile):
	# initialize each dictionary which will store values \
	# of the values of features already seen before
	clientUserDict = {}
	clientHostDict = {}
	clientIpDict = {}
	clientProgramDict = {}
	serviceNameDict = {}

	# assign a numeric value to each feature 
	userVal = 1
	hostVal = 1
	ipVal = 1
	programVal = 1
	serviceVal = 1
	# open the source file with the extracted json attributes
	with open(sourceFile, 'r') as sourceFile, open('../dataset/preprocessed.csv', 'w') as destFile:
		# open the destination file for the numeric data to be stored
		i = 0
		fieldNames = ['hour_of_the_day', 'day_of_the_week', 'client_user', 'client_host', 'client_ip', 'client_program', 'service_name']
		try:
			sourceReader = csv.DictReader(sourceFile)
			destWriter = csv.DictWriter(destFile, fieldnames=fieldNames)
			destWriter.writeheader()
		except:
			print "Failed to write to file"
		
		for line in sourceReader:
			if i == 0:
				i += 1
				continue
			client_user = ''
			client_host = ''
			client_ip = ''
			client_program = ''
			service_name = ''

			# if the item client_user matches a previous user \
			# assign its value to the current client_user else \
			# add a new client_user and increment the value

			if line['client_user'] == '':
				pass
			if line['client_user'] in clientUserDict:
				client_user = clientUserDict[line['client_user']]
			else:
				clientUserDict[line['client_user']] = userVal
				userVal += 1

			if line['client_host'] == '':
				pass
			if line['client_host'] in clientHostDict:
				client_host = clientHostDict[line['client_host']]
			else:
				clientHostDict[line['client_host']] = hostVal
				hostVal += 1

			if line['client_ip'] == '':
				pass
			elif line['client_ip'] in clientIpDict:
				client_ip = clientIpDict[line['client_ip']]
			else:
				clientIpDict[line['client_ip']] = ipVal
				ipVal += 1

			if line['client_program'] == '':
				pass
			elif line['client_program'] in clientProgramDict:
				client_program = clientProgramDict[line['client_program']]
			else:
				clientProgramDict[line['client_program']] = programVal
				programVal += 1

			if line['service_name'] == '':
				pass
			elif line['service_name'] in serviceNameDict:
				service_name = serviceNameDict[line['service_name']]
			else:	
				serviceNameDict[line['service_name']] = serviceVal
				serviceVal += 1

			newRow = {'hour_of_the_day' : line['hour_of_the_day'], \
				'day_of_the_week' : line['day_of_the_week'], \
				'client_user' : client_user, \
				'client_host' : client_host, \
				'client_ip' : client_ip, \
				'client_program' : client_program, \
				'service_name' : service_name}
			#print newRow
			# write the newly created row to the file
			destWriter.writerow(newRow)
			i += 1

	print "client_users : ", len(clientUserDict)
	print "client_hosts : ", len(clientHostDict)
	print "client_ips : ", len(clientIpDict)
	print "client_programs : ", len(clientProgramDict)
	print "service_names : ", len(serviceNameDict)
	pass

if __name__ == '__main__':
	
	data = extract(sys.argv[1])
	filename = '../dataset/extracted.csv'
	writeToFile(filename, data)
	print "Data stored in file"
	preprocess(filename)
	