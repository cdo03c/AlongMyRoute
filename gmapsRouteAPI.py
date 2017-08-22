#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 16:19:51 2017

@author: cdo03c
"""

#Import python libraries
from googlemaps import directions, Client
from datetime import timedelta


def findStep(route, time = 7200):
    '''The findStep function takes a google maps route and a time as inputs
    and returns a tuple containing the step of the route plus the beginning and
    end time of the step in which the time falls within the overall route.'''
    step = 0
    cumTime = 0
    while True:
        try:
            duration = route[0]['legs'][0]['steps'][step]['duration']['value']
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
    '''The findStepsWindow takes a googlemaps route, start time, time window,
    and possibly and end time and returns the location of the waypoint(s) along
    the route that falls within time parameters.'''
    
    #Sets the start time window (sTW) variable parameter by subtracting the 
    #time window from the startTime parameter
    sTW = startTime-twindow
    
    #Sets endTime to startTime if endTime is null
    if(not endTime):
        endTime = startTime
        
    #Sets the end time window (eTW) variable parameter by subtracting the 
    #time window from the endTime parameter
    eTW = startTime + twindow
    
    #Calls the findSteps function which returns a 
    steps = findSteps(route, sTW, eTW)
    
    #Tests if the start time does not fall within the time window
    if(not((steps[0][1]>sTW) & (steps[0][1]<startTime))):
        #Tests if the end time does not fall within the time window
        if(not((steps[1][1]>endTime) & (steps[1][1]<eTW))):
            #If both start time and end time fail, recursive call the function
            #with closest steps for start and end locations
            #Start Location (sL): start location of the step containing the start time
            #End Location (eL): start location of the step containing the end time
            sL = route[0]['legs'][0]['steps'][steps[0][0]]['start_location']
            eL = route[0]['legs'][0]['steps'][steps[1][0]]['start_location']
            return(findStepsWindow(gmaps.directions(origin = '{},{}'.format(sL['lat'],sL['lng']),
                                             destination ='{},{}'.format(eL['lat'],sL['lng'])),
                            startTime = startTime-steps[0][1],
                            endTime = eTW-steps[1][1]))
        else:
            return(findStepsWindow(gmaps.directions(origin = '{},{}'.format(sL['lat'],sL['lng']),
                                             destination ='{},{}'.format(eL['lat'],eL['lng'])),
                            startTime = startTime-steps[0][1],
                            endTime = eTW-steps[0][1]))
    else:
        if(not((steps[1][1]>endTime) & (steps[1][1]<eTW))):
            return(findStepsWindow(gmaps.directions(origin = '{},{}'.format(sL['lat'],sL['lng']),
                                             destination ='{},{}'.format(eL['lat'],sL['lng'])),
                            startTime = startTime-steps[0][1],
                            endTime = eTW-steps[0][1]))
        else:
            return(steps)

if(__name__ == "__main__"):

    #Sets up the client for google maps
    gmaps = Client(key='Add Your Key here')

    #Sets variables for directions
    origin = 'Lexington+MA'
    destination = 'Chicago+IL'
    startTime = timedelta(hours=2, minutes = 30)
    timeWindow = timedelta(minutes = 10)

    #Retrieves the route between an origin and destination using the directions
    #function from the googlemaps library
    route = gmaps.directions(origin, destination)
    window = findStepsWindow(route,
                             startTime = startTime.seconds,
                             endTime = None,
                             twindow = timeWindow.seconds)



# =============================================================================
# Tests to figure out how data is returned from Google Maps API Queries 
#
#
# #The route call to gmap has a json function that returns a dictionary with the
# #following keys.
# route.json().keys()
# #dict_keys(['routes', 'status', 'geocoded_waypoints'])
# 
# #The routes key contains a one element list which contains a dictionary.
# route.json()['routes'][0]
# 
# route.json()['routes'][0].keys()
# #dict_keys(['copyrights', 'warnings', 'waypoint_order', 'summary', 'bounds', 'overview_polyline', 'legs'])
# 
# #Geospatial extent of the route.
# route.json()['routes'][0]['bounds']
# #{'northeast': {'lat': 41.8781139, 'lng': -77.14263059999999}, 'southwest': {'lat': 38.7586761, 'lng': -87.630549}}
# 
# #Legs contains the location data for the journey.
# route.json()['routes'][0]['legs']
# 
# #The legs list contains one elements, a dictionary with the following keys.
# route.json()['routes'][0]['legs'][0].keys()
# #dict_keys(['start_address', 'end_address', 'start_location', 'traffic_speed_entry', 'distance', 'steps', 'duration', 'end_location', 'via_waypoint'])
# 
# #The steps key in the legs dictionary contains a list of dictionaries for each 
# #of the steps in a particular leg and each step dictionary with the element call
# route.json()['routes'][0]['legs'][0]['steps']
# 
# #The API call returns the Google geocodes of the origin and destination.
# route.json()['geocoded_waypoints']
# #[{'place_id': 'ChIJvUBPCmutt4kRxiQmNB4jueA', 'types': ['street_address'], 'geocoder_status': 'OK'}, {'place_id': 'ChIJ7cv00DwsDogRAMDACa2m4K8', 'types': ['locality', 'political'], 'geocoder_status': 'OK'}]
# 
# 
# =============================================================================
#print()
#print(response.content)