#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 16:19:51 2017

@author: obrien
"""

#Import python libraries
import requests

#Creates a function called getGMapRoute that takes as input the output format,
#origin, destination, and google maps API key, and returns data from the Google
#maps API in the specified format.
def getGMapRoute(output = 'json',
                 origin = '7341+Crestleigh+Circle+Alexandria+VA',
                 destination = 'Chicago+IL',
                 mode = '',
                 arrival_time = '',
                 departure_time = '',
                 key = ''):
    gmapscall = 'https://maps.googleapis.com/maps/api/directions/{}?'.format(output)
    if(origin):
        gmapscall += 'origin={}&'.format(origin)
    if(destination):
        gmapscall += 'destination={}&'.format(destination)
    if(mode):
        gmapscall += 'mode={}&'.format(mode)
    if(arrival_time):
        gmapscall += 'arrival_time={}&'.format(arrival_time)
    if(departure_time):
        gmapscall += 'departure_time={}&'.format(departure_time)
    gmapscall += 'key={}'.format(key)
    return(requests.get(gmapscall))


def findStep(route, time = 7200):
    step = 0
    cumTime = 0
    while True:
        try:
            duration = route.json()['routes'][0]['legs'][0]['steps'][step]['duration']['value']
            cumTime += duration
        except IndexError:
            print("The time you searched for is longer than the length of this leg of your journey.")
            return(step)
        if cumTime >= time:
            return(step, cumTime-duration, cumTime)
            break
        step += 1

def findSteps(route, startTime = 7600, endTime = 9600):
    return(findStep(route, startTime), findStep(route, endTime))

def findStepsWindow(route, startTime = 7200, endTime = None, twindow = 600):
    if(endTime):
        return(findSteps(route, startTime-twindow, endTime + twindow))
    return(findSteps(route, startTime-twindow, startTime+twindow))
        

route = getGMapRoute()
print(route.status_code)
#route.json()

#The route call to gmap has a json function that returns a dictionary with the
#following keys.
route.json().keys()
#dict_keys(['routes', 'status', 'geocoded_waypoints'])

#The routes key contains a one element list which contains a dictionary.
route.json()['routes'][0]

route.json()['routes'][0].keys()
#dict_keys(['copyrights', 'warnings', 'waypoint_order', 'summary', 'bounds', 'overview_polyline', 'legs'])

#Geospatial extent of the route.
route.json()['routes'][0]['bounds']
#{'northeast': {'lat': 41.8781139, 'lng': -77.14263059999999}, 'southwest': {'lat': 38.7586761, 'lng': -87.630549}}

#Legs contains the location data for the journey.
route.json()['routes'][0]['legs']

#The legs list contains one elements, a dictionary with the following keys.
route.json()['routes'][0]['legs'][0].keys()
#dict_keys(['start_address', 'end_address', 'start_location', 'traffic_speed_entry', 'distance', 'steps', 'duration', 'end_location', 'via_waypoint'])

#The steps key in the legs dictionary contains a list of dictionaries for each 
#of the steps in a particular leg and each step dictionary with the element call
route.json()['routes'][0]['legs'][0]['steps']

#The API call returns the Google geocodes of the origin and destination.
route.json()['geocoded_waypoints']
#[{'place_id': 'ChIJvUBPCmutt4kRxiQmNB4jueA', 'types': ['street_address'], 'geocoder_status': 'OK'}, {'place_id': 'ChIJ7cv00DwsDogRAMDACa2m4K8', 'types': ['locality', 'political'], 'geocoder_status': 'OK'}]


#print()
#print(response.content)