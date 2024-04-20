import json
from haversine import haversine 
import graphs 
import sys


sys.path.append('/content/gdrive/MyDrive/lab1-Information-Extraction-main/tramdata.py')
import tramdata as td


class TramStop:
    def __init__(self, name, lat=None, lon=None, lines_serve_stop=None):
        self.name = name  # Name of the tram stop
        self.position = (lat, lon)  # Position as a tuple (latitude, longitude)
        self.lines_serve_stop = lines_serve_stop if lines_serve_stop else []  # List of lines serving the stop

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
        self.stops = {name: TramStop(name, *stops[name]) for name in stops}
        self.lines = {line: TramLine(line, lines[line]) for line in lines}

        # Adding vertices (stops) and edges (connections between stops) to the graph
        for stop_name in self.stops:
            self.add_vertex(stop_name)
        for line in self.lines.values():
            stops_in_line = line.get_stops()
            for i in range(len(stops_in_line) - 1):
                stop1, stop2 = stops_in_line[i], stops_in_line[i+1]
                self.add_edge(stop1, stop2)
                self.set_weight(stop1, stop2, times[stop1][stop2])


# read the tram network from a JSON file
def readTramNetwork(file='tramnetwork.json'):
    with open(file, 'r', encoding='utf-8') as f:
        tram_network_data = json.load(f)
    # Extracting stops, lines, and times data
    stops = tram_network_data["stops"]
    lines = tram_network_data["lines"]
    times = tram_network_data["times"]
    # Creating and returning a TramNetwork object
    return TramNetwork(stops, lines, times)


def demo():
    G = readTramNetwork()
    a, b = input('from,to ').split(',')  
    view_shortest(G, a, b)  


if __name__ == '__main__':
    demo()
