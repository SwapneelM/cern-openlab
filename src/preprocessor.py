#!/usr/bin/env python
'''
arguments : [path_to_extracted_csv][numeric_csv_storage_filename]
'''
import sys, csv

'''
def convertNumeric(item, users, hosts, ips, programs, services):
	row = {}
	if item['client_user'] in users:
		pass
	return
'''
# TODO: change csv to pandas
if __name__ == '__main__':

	# initialize each dictionary which will store values \
	# of the values of features already seen before
	clientUserDict = {}
	clientHostDict = {}
	clientIpDict = {}
	clientProgramDict = {}
	serviceNameDict = {}

	# assign a numeric value to each feature 
	userVal = 0
	hostVal = 0
	ipVal = 0
	programVal = 0
	serviceVal = 0
	# open the source file with the extracted json attributes
	with open(sys.argv[1], 'r') as sourceFile, open(sys.argv[2], 'w') as destFile:
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
			print newRow
			# write the newly created row to the file
			destWriter.writerow(newRow)
			i += 1

	print "client_users : ", len(clientUserDict)
	print "client_hosts : ", len(clientHostDict)
	print "client_ips : ", len(clientIpDict)
	print "client_programs : ", len(clientProgramDict)
	print "service_names : ", len(serviceNameDict)
	