#!/usr/bin/env/python
import json, math

def getDistance(item, new_item):
	distance = 0.0
	# compare features originally present in the training set
	for feature in xrange(len(item)):
		# keep first feature as day_of_the_week 
		# and second as hour_of_the_day to calculate weight
		if feature <= 1:
			distance += pow((float(item[feature]) - float(new_item[feature])), 2)
		else:
			if feature 
			if new_item[feature] == item[feature]:
				pass
			else:
				distance += 1.0
	return math.sqrt(distance)

def prediction(new_item, distance):




if __name__ == '__main__':
	
	with open(sys.argv[1], 'r') as file:
		'''
		# Extract useful features from the dataset
		i = 0
		training = []
		for line in file:
			if i < 1000000

				try:
					json_data = json.load(line)
					if json_data['data']['client_user']:

				except:
					pass
				i += 1
			else:
		'''
		i = 0
		data = {}
		newdata = []
		for line in file:
			try:
				json_data = json.load(line)
				if json_data:
					if json_data['data']['event_timestamp']:
						timestamp = json_data['data']['event_timestamp']
						hour_of_the_day = int(timestamp[11:13])
						# 0 - Monday; 6 - Sunday
						day_of_the_week = datetime.datetime(int(timestamp[:4]), \
							int(timestamp[5:7]), int(timestamp[8:10]), hour_of_the_day, \
							int(timestamp[14:16]), int(timestamp[17:19])).weekday()
					newdata.extend(hour_of_the_day, day_of_the_week)
					if json_data['data']['client_ip']:	
						client_ip = json_data['data']['client_ip']
						newdata.extend(client_ip)
					if json_data['data']['client_user']:
						client_user = json_data['data']['client_user']
						newdata.extend(client_user)
					if json_data['data']['client_program']:
						client_program = json_data['data']['client_program']
						newdata.extend(client_program)
					if json_data['data']['client_host']:
						client_host = json_data['data']['client_host']
						newdata.extend(client_host)
					if json_data['data']['service_name']:	
						service_name = json_data['data']['service_name']
						newdata.extend(service_name)
					if i == 1:
						data.append(newdata)
			except:
				print "Error at line : ", i
			i += 1

