import json

# imports added in Lab3 version
import math
import os
from . import graphs
from django.conf import settings


# path changed from Lab2 version
# TODO: copy your json file from Lab 1 here

TRAM_FILE = os.path.join(settings.BASE_DIR, 'C:/Users/hp/lab3/static/tramnetwork.json')
# 'static/tramnetwork.json'




class TramStop:
    def __init__(self, name, lat=None, lon=None, lines=None):
        self.name = name
        self.position = (lat, lon)
        self.lines_serve_stop = lines if lines else []

    # Getter for stop name
    def get_name(self):
        return self.name

    # Getter for stop position
    def get_position(self):
        return self.position

    # Setter for stop position
    def set_position(self, lat, lon):
        self.position = (lat, lon)

    # Getter for lines serving the stop
    def get_lines(self):
        return self.lines_serve_stop

    # Method to add a line to the stop
    def add_line(self, line):
        self.lines_serve_stop.append(line)




class TramLine:
    def __init__(self, name, stops):
        self.name = name  # Name of the tram line
        self.stops = stops  # List of stops in order

    # Getter for line name
    def get_name(self):
        return self.name

    # Getter for stops of the line
    def get_stops(self):
        return self.stops




class TramNetwork(graphs.WeightedGraph):
    def __init__(self, stops, lines, times):
        super().__init__()  
  
    
        # Initialize line dictionary
        self._linedict = {}
        if lines:
            for line, stops_list in lines.items():
                self._linedict[str(line)] = TramLine(line, stops_list)
        
     
        self._stopdict = {}
        if stops:
             for stop, stop_data in stops.items():
                lines_at_stop = [line for line in lines if stop in lines[line]]
                self._stopdict[str(stop)] = TramStop(stop, lat=stop_data['lat'], lon=stop_data['lon'], lines=lines_at_stop)


        # Initialize time dictionary
        self._timedict = times or {}

        # Adding vertices and edges
        for stop in self.all_stops():
            self.add_vertex(stop)
        for start_stop, destinations in self._timedict.items():
            for end_stop, time in destinations.items():
                self.add_edge(start_stop, end_stop)
                self.set_weight(start_stop, end_stop, time)

    def all_lines(self):
        return list(self._linedict)

    def all_stops(self):
        return list(self._stopdict)


    def geo_distance(self, a, b):
        a = str(a)
        b = str(b)

        if a not in self._stopdict or b not in self._stopdict:
            return "unknown arguments"
        if a == b:
            return "Please enter two different stops!"
        
        # Extract latitudes and longitudes for both stops and convert them to floats
        lat1, lon1 = map(float, self.stop_position(a))
        lat2, lon2 = map(float, self.stop_position(b))
        
        # Convert degrees to radians
        Earth_Radius = 6371.009
        degree_to_rad = math.pi / 180
        lat1_rad = lat1 * degree_to_rad
        lon1_rad = lon1 * degree_to_rad
        lat2_rad = lat2 * degree_to_rad
        lon2_rad = lon2 * degree_to_rad

        # Calculate the differences in coordinates
        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad
        lat_m = (lat1_rad + lat2_rad) / 2

        # Calculate the distance
        distance = Earth_Radius * math.sqrt(dlat**2 + (math.cos(lat_m) * dlon)**2)
        return round(distance, 3)




    def line_stops(self, line):
        line = str(line)
        if line in self._linedict:
            return self._linedict[line].get_stops()
        return f"The line {line} does not exist"
    def remove_lines(self, lines_to_remove):
        for line in lines_to_remove:
            line = str(line)
            stops_on_line = self.line_stops(line)
            
            # Update dictionaries
            if line in self._linedict:
                del self._linedict[line]

            for i, stop in enumerate(stops_on_line):
                if i == len(stops_on_line) - 1:
                    break  # Skip the last stop as it doesn't have a next stop

                next_stop = stops_on_line[i + 1]

                if line in self._stopdict[stop].get_lines():
                    self._stopdict[stop].remove_line(line)

                # Update time dictionary and remove edges
                if self._should_delete_edge(stop, next_stop, lines_to_remove):
                    self.remove_edge(stop, next_stop)
                    del self._timedict[stop][next_stop]

    def _should_delete_edge(self, stop, stops_on_line, lines_to_remove):
        # Helper method to decide if an edge should be deleted
        for i in range(len(stops_on_line) - 1):
            next_stop = stops_on_line[i + 1]
            for other_line in self.all_lines():
                if other_line in lines_to_remove:
                    continue
                if stop in self._linedict[other_line].get_stops() and next_stop in self._linedict[other_line].get_stops():
                    return False
        return True

    def stop_lines(self, stop):
        if stop in self._stopdict:
            return self._stopdict[stop].get_lines()

    def stop_position(self, stop):
        if stop in self._stopdict:
            position = self._stopdict[stop].get_position()
            print(f"Position of {stop}: {position}")  # Debugging line
            return position


    def transition_time(self, a, b):
        if a in self._timedict and b in self._timedict[a]:
            return self._timedict[a][b]
        return f"{a} and {b} are not adjacent or valid stops"


    def extreme_positions(self):
        stops = self._stopdict.values()

        # Extracting positions as floats
        minlat = min(float(stop.get_position()[0]) for stop in stops)
        maxlat = max(float(stop.get_position()[0]) for stop in stops)
        minlon = min(float(stop.get_position()[1]) for stop in stops)
        maxlon = max(float(stop.get_position()[1]) for stop in stops)

        return minlon, minlat, maxlon, maxlat






def readTramNetwork():
    with open(TRAM_FILE, encoding="utf-8") as tram_file:
        dict = json.load(tram_file)
    return TramNetwork(dict["stops"], dict["lines"], dict["times"])
    
    

    


# Bonus task 1: take changes into account and show used tram lines

def specialize_stops_to_lines(network):
    # TODO: write this function as specified
    return network


def specialized_transition_time(spec_network, a, b, changetime=10):
    # TODO: write this function as specified
    return changetime


def specialized_geo_distance(spec_network, a, b, changedistance=0.02):
    # TODO: write this function as specified
    return changedistance




