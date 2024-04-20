# visualization of shortest path in Lab 3, modified to work with Django




# from trams import readTramNetwork
# from graphs import dijkstra
# from color_tram_svg import color_svg_network


from . import color_tram_svg
from . import graphs
from . import trams

import os
import graphviz
from django.conf import settings
import urllib.parse



SHORTEST_PATH_SVG = os.path.join(settings.BASE_DIR,
                        'tram/templates/tram/images/shortest_path.svg')

# SHORTEST_PATH_SVG = os.path.join(settings.BASE_DIR,
#                         'tram/templates/tram/images/gbg_tramnet.svg')

# Define colors for tram lines in Gothenburg
tram_line_colors = {
    1: 'gray', 2: 'yellow', 3: 'blue', 4: 'green', 5: 'red',
    6: 'orange', 7: 'brown', 8: 'purple', 9: 'blue',
    10: 'lightgreen', 11: 'black', 13: 'pink'}

# Function to adjust positions of tram stops on the map
def adjust_map_scale(tram_network):
    # Extract the extreme positions
    min_lat, min_lon, max_lat, max_lon = tram_network.extreme_positions()

    # Convert to float if they are strings
    min_lat, min_lon, max_lat, max_lon = map(float, [min_lat, min_lon, max_lat, max_lon])

    # Calculate map dimensions
    map_width = max_lon - min_lon
    map_height = max_lat - min_lat
    scale_factor = len(tram_network) / 4  # Heuristic scale factor

    # Calculate scale factors for x and y axes
    x_scale = scale_factor / map_width
    y_scale = scale_factor / map_height
    
    # Return a function to scale stop positions
    return lambda position: (x_scale * (float(position[0]) - min_lon), y_scale * (float(position[1]) - min_lat))


# Function to create a URL for Google Search of a tram stop
def generate_stop_search_url(stop_name):
    google_base_url = 'https://www.google.com/search'
    search_params = urllib.parse.urlencode({'q': 'Gothenburg ' + stop_name})
    return google_base_url + '?' + search_params

# Function to generate a graphviz representation of the tram network
def generate_network_visualization(tram_network, output_file, color_mapping=None, position_mapping=adjust_map_scale):
    graph_viz = graphviz.Graph(engine='fdp', graph_attr={'size': '12,12'})

    # Iterate over all stops to add them as nodes
    for stop in tram_network.all_stops():
        stop_position = tram_network.stop_position(stop)
        if position_mapping:
            stop_position = position_mapping(tram_network)(stop_position)
        pos_x, pos_y = str(stop_position[0]), str(stop_position[1])
        
        node_color = color_mapping.get(stop, 'white') if color_mapping else 'white'

            
        graph_viz.node(stop, label=stop, shape='rectangle', pos=pos_x + ',' + pos_y + '!',
                       fontsize='8pt', width='0.4', height='0.05',
                       URL=generate_stop_search_url(stop),
                       fillcolor=node_color, style='filled')
        
    # Add edges representing tram lines
    for line in tram_network.all_lines():
        stops_on_line = tram_network.line_stops(line)
        for i in range(len(stops_on_line) - 1):
            graph_viz.edge(stops_on_line[i], stops_on_line[i + 1],
                           color=tram_line_colors[int(line)], penwidth='2')

    graph_viz.format = 'svg'
    svg_output = graph_viz.pipe().decode('utf-8')
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(svg_output)








def show_shortest(departure, destination):
    # Load the tram network data
    tram_network = trams.readTramNetwork()

    # Determine the fastest route based on transit time and the shortest route by geographical distance
    time_based_route = graphs.dijkstra(tram_network, departure, cost=lambda node1, node2: tram_network.get_weight(node1, node2))
    distance_based_route = graphs.dijkstra(tram_network, departure, cost=lambda node1, node2: tram_network.geo_distance(node1, node2))
    
    # Prepare color codes for visualization of the routes
    route_colors = {}
    if destination in time_based_route:
        for stop in time_based_route[destination]:
            route_colors[str(stop)] = 'orange'
    if destination in distance_based_route:
        for stop in distance_based_route[destination]:
            route_colors[str(stop)] = 'green' if str(stop) not in route_colors else 'cyan'

    # Formulate the descriptions of the calculated routes
    timepath = 'Fastest route from {} to {}: '.format(departure, destination) + " -> ".join(time_based_route[destination])
    geopath = 'Geographically shortest route from {} to {}: '.format(departure, destination) + " -> ".join(distance_based_route[destination])

    # Updating the tram network visualization with the paths
    generate_network_visualization(tram_network, SHORTEST_PATH_SVG, route_colors)

    return timepath , geopath


