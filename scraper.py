#!/usr/bin/env/python
import json, math, sys, datetime

def getDistance(item, newItem):
	distance = 0.0
	print("\nFinding distance")
	print newItem
	print item
	# compare features originally present in the training set

	# keep first feature as day_of_the_week 
	# and second as hour_of_the_day to calculate weight
	# assume these are always present in newItem
	distance += pow((float(item["day_of_the_week"]) - float(newItem["day_of_the_week"])), 2)
	distance += pow((float(item["hour_of_the_day"]) - float(newItem["hour_of_the_day"])), 2)		
	
	properties = ["client_user", "client_host", "client_program", "service_name"]
	# if both have different lengths thus different features
	for prop in properties:
		if prop in item or prop in newItem:
				try:
					if item[prop] == newItem[prop]:
						pass
					else: 
						distance += 1.0
				
				except:
					distance += 1.0
					# print "Error calculating distance"
		else:
			pass
		pass
	if "client_user" in item:
		if "client_user" in newItem:
			if item["client_user"] != newItem["client_user"] \
			and distance <= 2.0:
				distance += 30.0

	finalDistance = math.sqrt(distance)
	print "Distance : ", finalDistance
	return finalDistance

def newConnection(items, newItem):
	for item in items:
		# match the ip address or the client user 
		# in case ip is absent
		if "client_user" in items[item]:
			if "client_user" in newItem:
				if items[item]["client_user"] == newItem["client_user"]:
					return False
		elif "client_ip" in items[item]:
			if "client_ip" in newItem:
				if items[item]["client_ip"] == newItem["client_ip"]:
					return False
		elif "client_host" in items[item]:
			if "client_host" in newItem:
				if items[item]["client_host"] == newItem["client_host"]:
					return False
	return True


if __name__ == '__main__':
	
	with open(sys.argv[1], 'r') as file:
		i = 0

		# TODO: change list-based stuff to dict
		data = {}
		anomalies = {}
		distanceVote = []

		# iterate over each logged line
		for line in file:
			newItem = {}
			#try:
			json_data = json.loads(line)

			if 'data' in json_data:
				timestamp = str(json_data['data']['event_timestamp'])
				hour_of_the_day = (float(timestamp[11:13]) + float(timestamp[14:16])/60)
				# 0 - Monday; 6 - Sunday
				day_of_the_week = datetime.datetime(int(timestamp[:4]), \
					int(timestamp[5:7]), int(timestamp[8:10]), int(timestamp[11:13]), \
					int(timestamp[14:16]), int(timestamp[17:19])).weekday()
				newItem["hour_of_the_day"] = hour_of_the_day
				newItem["day_of_the_week"] = day_of_the_week
				
				if 'client_ip' in json_data['data']:
					#print "\nclient_ip: ", json_data['data']['client_ip']
					client_ip = str(json_data['data']['client_ip'])
					newItem["client_ip"] = client_ip

				if 'client_user' in json_data['data']:
					#print "\nclient_user: ", json_data['data']['client_user']
					client_user = str(json_data['data']['client_user'])
					newItem["client_user"] = client_user
				
				if 'client_host' in json_data['data']:
					#print "\nclient_host: ", json_data['data']['client_host']
					client_host = str(json_data['data']['client_host'])
					newItem["client_host"] = client_host

				if 'client_program' in json_data['data']:
					#print "\nclient_program: ", json_data['data']['client_program']
					client_program = str(json_data['data']['client_program'])
					newItem["client_program"] = client_program

				if 'service_name' in json_data['data']:
					#print "\nservice_name: ", json_data['data']['service_name']
					service_name = str(json_data['data']['service_name'])
					newItem["service_name"] = service_name
			
			# print "\nNew Data :", newItem
			
			# ignore cases where data is incomplete
			if len(newItem) <= 2:
				continue

			# for a new connection, blindly trust it
			if newConnection(data, newItem):
				print "\nNew item found"
			
			# voting for distance to all previously stored nodes	
			for item in data:
				distance = getDistance(data[item], newItem)
				distanceVote.append(distance)
				if distance == 0.0:
					print "*" * 20
			# print "\nDistance Vote: ", distanceVote
			distanceVote.sort()

			if len(distanceVote) == 0:
				print "\nNo votes for closest neighbour"
				data[i] = newItem

			elif distanceVote[0] <= 3.0:
				# print(distanceVote)
				print "\nMinimum distance: ", distanceVote[0]
				data[i] = newItem

			elif distanceVote[0] > 3.0:
				print "\nAnomalous connection at: ", newItem
				anomalies[i] = newItem
			else:
				print "\nError"
				data[i] = newItem

			#except:
			#	print "\nError at line : ", i
			
			i += 1
		print "\nAnomalies: ", anomalies
