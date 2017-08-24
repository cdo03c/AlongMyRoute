import json
import googlemaps

class Route():
    def __init__(self, route):
        """
        This class only currently looks at a "primary" route/leg of a return. 
        Additional functionality can be added to accomodate additional routes
        and waypoints (legs).
    
        Args:
            route (dict): Route response from Google Maps API
        """
        self.routes = route
        self.primary_route = self.routes[0] #usually only one of these is returned
        self.primary_leg = self.primary_route['legs'][0]
        self.distance = self.primary_leg['distance']['value']
        self.duration = self.primary_leg['duration']['value']
        self.start_address = self.primary_leg['start_address']
        self.end_address = self.primary_leg['end_address']
        self.steps = self.primary_leg['steps']


    def find_step_by_time(self, desired_time):
        """
        For the primary leg of the route, finds the step which the user will
        be in during the desired_time specified.abs
        
        Args:
            desired_time (int): The desired time a step is to be found for

        Returns:
            step (dict): The step of the route traveled during the ``desired_time``
        """
        steps = self.steps
        trip_total_duration = self.duration
        cumulative_time = 0
        
        if trip_total_duration < desired_time:
            raise ValueError("Your desired time is longer than the length of this leg of your journey")

        for step in steps:
            try:
                duration = step['duration']['value']
                cumulative_time += duration
                if cumulative_time >= desired_time:
                    return step
            except:
                print("Something went wrong finding step")
    