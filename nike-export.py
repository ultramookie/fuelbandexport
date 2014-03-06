#!/usr/bin/python

import json
import urllib
import urllib2
import time
 
ACCESS_TOKEN = 'ACCESS_TOKEN'
 
base_url = 'https://api.nike.com'
url = '/me/sport/activities?access_token=%s' % ACCESS_TOKEN
headers = {'appid':'fuelband', 'Accept':'application/json'} # weird required headers, blah.
current_month = None
emotion = ''
note = ''
shoes = ''
weather = ''
terrain = ''

file = open('nike.txt','w+')

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
                        # convert from km to mi and round
                        miles = metrics.get('distance') * 0.621371
                        distance = '%.2f' % round(miles, 2)

                        # remove milliseconds
                        duration = metrics.get('duration').partition('.')[0]

                        pace = ''
                        sp = duration.split(':')
                        if (len(sp) == 3):
                                duration_seconds = int(sp[0]) * 60 * 60 + int(sp[1]) * 60 + int(sp[2])
                                if miles > 0:
                                        seconds_per_mile = duration_seconds / miles
                                else:
                                        seconds_per_mile = 0
                                hours, remainder = divmod(seconds_per_mile, 3600)
                                minutes, seconds = divmod(remainder, 60)
                                pace = '(%.0f\'%02.0f/mi)' % (minutes, seconds)

			for tag in activity.get('tags'):
				if tag.get('tagType') == "EMOTION":
					emotion = tag.get('tagValue').replace('_','-').title()
				if (tag.get('tagType') == "NOTE") and (tag.get('tagValue') != "NOTE"):
					note = tag.get('tagValue')
				if tag.get('tagType') == "SHOES":
					shoes = tag.get('tagValue')
				if tag.get('tagType') == "WEATHER":
					weather = tag.get('tagValue').replace('_','-').title()
				if tag.get('tagType') == "TERRAIN":
					terrain = tag.get('tagValue').title()

			# remove milliseconds
			duration = metrics.get('duration').partition('.')[0]

			if activity.get('activityType') == "RUN": 
				file.write(date + ' : ' + distance.ljust(5) + ' miles ' + pace.ljust(11) + ' fuel: ' + str(fuel).ljust(5) + ' calories: ' +  str(calories).ljust(4) + ' active: '  + duration.ljust(7) + ' | ' + emotion.ljust(12) + ' | ' + shoes.ljust(12) + ' | ' + weather.ljust(12) + ' | ' + terrain.ljust(9) + ' | ' + note + '\n')
				emotion = '' 
				note = ''
				shoes = ''
				weather = ''
				terrain = ''
	# pagination
	url = None
	if resp.get('paging') and resp.get('paging').get('next'):
		url = resp.get('paging').get('next') 

file.close()
