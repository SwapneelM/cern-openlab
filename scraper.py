#!/usr/bin/env/python
import json, math, sys, datetime

def getDistance(item, newData):
	distance = 0.0
	print("\nFinding distance")
	print newData
	print item
	# compare features originally present in the training set
	for feature in range(len(max(item, newData, key=len))):
		# keep first feature as day_of_the_week 
		# and second as hour_of_the_day to calculate weight
		# assume these are always present in newData
		if feature <= 1:
			distance += pow((float(item[feature]) - float(newData[feature])), 2)
		else:
			# if both have different lengths thus different features 
			if len(item) != len(newData):
				distance += 1.0
			# if both have the same value for a feature
			elif newData[feature] == item[feature]:
				pass
			# both are the same length but different value of features
			else:
				distance += 1.0
	finalDistance = math.sqrt(distance)
	print "Distance : ", finalDistance
	return finalDistance

def newConnection(items, newItem):
	for item in items:
		# match the ip address or the client user 
		# in case ip is absent
		if item[2] == newItem[2]:
			return False
	return True


if __name__ == '__main__':
	
	with open(sys.argv[1], 'r') as file:
		i = 0

		# TODO: change list-based stuff to dict
		data = []
		anomalies = []
		distanceVote = []

		# iterate over each logged line
		for line in file:
			newData = []
			#try:
			json_data = json.loads(line)

			if 'data' in json_data:
				timestamp = str(json_data['data']['event_timestamp'])
				hour_of_the_day = (float(timestamp[11:13]) + float(timestamp[14:16])/60)
				# 0 - Monday; 6 - Sunday
				day_of_the_week = datetime.datetime(int(timestamp[:4]), \
					int(timestamp[5:7]), int(timestamp[8:10]), int(timestamp[11:13]), \
					int(timestamp[14:16]), int(timestamp[17:19])).weekday()
				newData.append(hour_of_the_day)
				newData.append(day_of_the_week)
				
				if 'client_ip' in json_data['data']:
					#print "\nclient_ip: ", json_data['data']['client_ip']
					client_ip = str(json_data['data']['client_ip'])
					newData.append(client_ip)

				if 'client_user' in json_data['data']:
					#print "\nclient_user: ", json_data['data']['client_user']
					client_user = str(json_data['data']['client_user'])
					newData.append(client_user)
				
				if 'client_host' in json_data['data']:
					#print "\nclient_host: ", json_data['data']['client_host']
					client_host = str(json_data['data']['client_host'])
					newData.append(client_host)

				if 'client_program' in json_data['data']:
					#print "\nclient_program: ", json_data['data']['client_program']
					client_program = str(json_data['data']['client_program'])
					newData.append(client_program)

				if 'service_name' in json_data['data']:
					#print "\nservice_name: ", json_data['data']['service_name']
					service_name = str(json_data['data']['service_name'])
					newData.append(service_name)
			
			# print "\nNew Data :", newData
			
			# ignore cases where data is incomplete
			if len(newData) <= 2:
				continue

			# for a new connection, blindly trust it
			if newConnection(data, newData):
				print "\nNew item found"
			
			# voting for distance to all previously stored nodes	
			for item in data:
				distanceVote.append(getDistance(item, newData))
			# print "\nDistance Vote: ", distanceVote
			distanceVote.sort()

			if len(distanceVote) == 0:
				print "\nNo votes for closest neighbour"
				data.append(newData)

			elif distanceVote[0] <= 10.0:
				# print(distanceVote)
				print "\nMinimum distance: ", distanceVote[0]
				data.append(newData)

			elif distanceVote[0] > 10.0:
				print "\nAnomalous connection at: ", newData
				anomalies.append(newData)
			else:
				print "\nError"
				data.append(newData)

			#except:
			#	print "\nError at line : ", i
			
			i += 1
		print "\nAnomalies: ", anomalies
