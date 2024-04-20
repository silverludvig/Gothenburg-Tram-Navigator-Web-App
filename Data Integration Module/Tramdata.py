import sys
import json
import re
import math





# files given
STOP_FILE = "data/tramstops.json"
LINE_FILE = "data/tramlines.txt"


# file to give
TRAM_FILE ="./tramnetwork.json" 


#####################################################################################################################################################################
def build_tram_stops(jsonobject): 
# Read the JSON file
    with open(jsonobject, 'r', encoding='utf-8') as file:
        json_data = file.read()
# Parse the JSON data into a dictionary
    dictionary_data = json.loads(json_data)
# print(dictionary_data)

# Create an empty dictionary to hold the new data
    new_dict = {}
   
# This is a for loop that iterates over each key-value pair in dictionary_data.
    for key, value in dictionary_data.items():
        lat = dictionary_data[key]['position'][0]
        lon = dictionary_data[key]['position'][1]
        new_dict[key] = {
            'lat': lat,
            'lon': lon
        }
   
      

    return new_dict
    

    

jsonobject= STOP_FILE 
tram_stop = build_tram_stops(jsonobject)
# print(tram_stop)   


# Test
# lat = dictionary_data['Östra Sjukhuset']['position'][0]
# lon = dictionary_data['Östra Sjukhuset']['position'][1]
# print (dictionary_data['Östra Sjukhuset']['position'])



###########################################################################################################



def build_tram_lines(lines):
    with open(lines, 'r', encoding='utf-8') as file:
        data = file.read()
        
# line numbers are followed by a colon and then a newline
    # line_numbers = re.findall(r'(\d+):\n', lines_data)
# split the data into lines
    each_line = data.split('\n\n')
    each_line = each_line[:-1]
    tram_data = {} 
    for block in each_line:
    # Split each block by newline to get individual lines
         lines = block.split('\n')
    
    # For each line (skipping the line number), extract the stop name
         tram_number = lines[0].rstrip(":")
    
    # All subsequent lines are tram stops
         tram_stops = [line[:-5].strip() for line in lines[1:]]
    
    # Assign the tram stops to the tram number in the dictionary
         tram_data[tram_number] = tram_stops
         
         
         
    blocks = data.split("\n\n")  # Split data by tram lines

    time_dict = {}

    for block in blocks:
        lines = block.split("\n")[1:]  # Split each block by newline and skip the tram number

        for i in range(len(lines) - 1):
            stop_name, stop_time = lines[i].rsplit(maxsplit=1)
            stop_hour, stop_minute = map(int, stop_time.split(":"))
            next_stop_name, next_stop_time = lines[i+1].rsplit(maxsplit=1)
            next_stop_hour, next_stop_minute = map(int, next_stop_time.split(":"))

            # Calculate time difference, adjusting for hour changes
            time_difference = (next_stop_hour * 60 + next_stop_minute) - (stop_hour * 60 + stop_minute)
            if time_difference < 0:
                time_difference += 24 * 60  # Adjust for midnight crossing

            # Update the time_dict
            if stop_name not in time_dict:
                time_dict[stop_name] = {}
            if next_stop_name not in time_dict[stop_name]:
                time_dict[stop_name][next_stop_name] = time_difference

    return tram_data, time_dict

    

lines = LINE_FILE
tram_lines, tram_time = build_tram_lines(lines)
# print(tram_lines)






###############################################################################################################






    
    









#####################################################################################################################################################################
def build_tram_network(stopfile, linefile):
    
    tram_stop = build_tram_stops(stopfile)
    tram_lines, tram_time = build_tram_lines(linefile)
    tram_network = {"stops": tram_stop  , "lines": tram_lines, "times": tram_time}
    
    return tram_network
    
    
    






#####################################################################################################################################################################
    
        
    
#####################################################################################################################################################################
def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of Earth in kilometers. Use 3956 for miles
    r = 6371

    # Calculate the result
    return c * r






#####################################################################################################################################################################
# Query functions

def lines_via_stop(linedict, stop):
    lines=[]
    for line in linedict:
        for stop_name in linedict[line]:
            if stop_name == stop: 
                lines.append(line)
    lines.sort(key=int)
    return lines

# print('line_via_stop: ',lines_via_stop(build_tram_lines(LINE_FILE)[0], 'Centralstationen'))

def lines_between_stops(linedict, stop1, stop2): 
    lines1 = lines_via_stop(linedict, stop1)        
    lines2 = lines_via_stop(linedict, stop2)
    res = list(set.intersection(*map(set, [lines1, lines2])))
    res.sort(key=int)
    return res

# print ('lines_between_stops:', lines_between_stops(build_tram_lines(LINE_FILE)[0],'Centralstationen', 'SKF'))

def time_between_stops(linedict, timedict, line, stop1, stop2):
    # Check if both stops are on the line
    if stop1 not in linedict[line] or stop2 not in linedict[line]:
        return None  # One or both stops are not on this line

    # Get the indices of the stops
    index1, index2 = linedict[line].index(stop1), linedict[line].index(stop2)

    # Ensure index1 is less than index2
    if index1 > index2:
        index1, index2 = index2, index1  # Swap the indices if out of order

    # Calculate the time
    total_time = 0
    for i in range(index1, index2):
        stop_a = linedict[line][i]
        stop_b = linedict[line][i + 1]
        total_time += timedict[stop_a][stop_b]

    return total_time

            
# print ('time_between_stops:', time_between_stops(tram_lines, tram_time, '11', 'Centralstationen', 'SKF'))

def distance_between_stops(stopdict, stop1, stop2): 
    a = (float(stopdict[stop1]['lat']), float(stopdict[stop1]['lon']))
    b = (float(stopdict[stop2]['lat']), float(stopdict[stop2]['lon']))
    
    return haversine(a[0],a[1], b[0],b[1])
    
# print('distance_between_stops:', distance_between_stops(tram_stop, 'Centralstationen', 'SKF'))
    
    
    
    
    
#####################################################################################################################################################################
def answer_query(tramdict, query):
    if query[:3] == 'via':
        try:
            return lines_via_stop(tramdict['lines'], query[3:].strip())
        except: 
            print('unknown arguments')
    
    elif query[:7].strip() == 'between': 
        # Remove 'between ' prefix
        query_without_prefix = query[len('between'):]

        # Split the string at ' and '
        parts = query_without_prefix.split(' and', 1)

        if len(parts) == 2:
            stop1, stop2 = parts[0].strip(), parts[1].strip()

            try:
                return lines_between_stops(tramdict['lines'], stop1, stop2)
            except:
                print('unknown arguments')
        else:
            print('Query format incorrect.')
            
    elif query[:10].strip() == 'time with':
        query = query.split()
        line = query[2].strip()
        from_index = query.index('from')
        to_index = query.index('to')
        stop1 = " ".join(query[from_index+1: to_index]).strip()
        stop2 = " ".join(query[to_index + 1:]).strip()
        try: 
            return time_between_stops(tramdict['lines'], tramdict['times'], line, stop1, stop2)
        except: 
            print('unknown arguments')      
            
    elif query[:8] == 'distance':
        query = query.split()
        from_index = query.index('from')
        to_index = query.index('to')
        stop1 = " ".join(query[from_index+1: to_index]).strip()
        stop2 = " ".join(query[to_index+1:]).strip()
        try:
            return distance_between_stops(tramdict['stops'], stop1, stop2)
        except: 
            print('unknown arguments')
    
    else: 
        print('sorry, try again')
        return False
        

# print(answer_query(TRAM_FILE , 'via Centralstationen'))



#####################################################################################################################################################################
def dialogue(tramfile): 
    with open(TRAM_FILE, encoding='utf-8') as net:
        tramdict = json.loads(net.read())
        query = input('Write your query > ')
        while query != 'quit': 
            print(answer_query(tramdict, query))
            query = input('Write your query > ')
        sys.exit()








#####################################################################################################################################################################
if __name__ == '__main__':
    if sys.argv[1:] == ['init']:
        build_tram_network(STOP_FILE,LINE_FILE)
    else:
        dialogue(TRAM_FILE)
        

