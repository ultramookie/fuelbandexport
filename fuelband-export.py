#!/usr/bin/python

import json
import urllib
import urllib2
import time

ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
 
base_url = 'https://api.nike.com'
url = '/me/sport/activities/FUELBAND?access_token=%s&experienceType=FUELBAND' % ACCESS_TOKEN
headers = {'appid':'fuelband', 'Accept':'application/json'} # weird required headers, blah.
current_month = None
emotion = ''
note = ''

file = open('fuelband.txt','w+')

while url:
 
	req = urllib2.Request('%s%s' % (base_url, url), None, headers)
	r = urllib2.urlopen(req)
	resp = json.loads(r.read())
	r.close()
 
	if resp.get('data'):
 
		for activity in resp.get('data'):
 
			# 2013-05-26T14:48:42Z
			start_time = time.strptime(activity.get('startTime'), '%Y-%m-%dT%H:%M:%SZ')
			date = time.strftime('%a %m/%d/%y', start_time)
 
			month = time.strftime('%B', start_time)
			if month != current_month:
				current_month = month
				#print ''
				file.write('\n')
				#print '--', current_month, '--'
				file.write('--' + current_month + '--\n')
			
			metrics = activity.get('metricSummary')

			calories = metrics.get('calories')
			fuel = metrics.get('fuel')
			steps = metrics.get('steps')

			for tag in activity.get('tags'):
				if tag.get('tagType') == "EMOTION":
					emotion = tag.get('tagValue').replace('_','-').title()
				if (tag.get('tagType') == "NOTE") and (tag.get('tagValue') != "NOTE"):
					note = tag.get('tagValue')

			# remove milliseconds
			duration = metrics.get('duration').partition('.')[0]

			if activity.get('activityType') == "ALL_DAY": 
				file.write(date + ' : fuel: ' + str(fuel).ljust(6) + '\tcalories: ' +  str(calories).ljust(6) + '\tactive: '  + duration.ljust(8) + '\t' + emotion.ljust(12) + '\t' + note + ' ' + '\n')
				emotion = '' 
				note = ''
	# pagination
	url = None
	if resp.get('paging') and resp.get('paging').get('next'):
		url = resp.get('paging').get('next') 

file.close()
