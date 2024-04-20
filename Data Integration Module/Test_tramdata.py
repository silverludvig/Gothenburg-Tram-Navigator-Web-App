# The file test_tramdata-py already tests if all stops associated with lines in linedict also exist in stopdict. You should add at least the following tests:

# that all tram lines listed in the original text file tramlines.txt are included in linedict,
# that the list of stops for each tramline is the same in tramlines.txt and linedict,
# that all distances are "feasible", meaning less than 20 km (test this test with a smaller number to see it fail!),
# that the time from a to b is always the same as the time from b to a along the same line.




import unittest
from tramdata import *
import csv


TRAM_FILE = "./tramnetwork.json"
LINE_FILE = "data/tramlines.txt"


class TestTramData(unittest.TestCase):

    def setUp(self):
        with open(TRAM_FILE) as trams:
            tramdict = json.loads(trams.read())
            self.stopdict = tramdict['stops']
            self.linedict = tramdict['lines']
            self.timedict = tramdict['times']

    def test_stops_exist(self):
        stopset = {stop for line in self.linedict for stop in self.linedict[line]}
        for stop in stopset:
            self.assertIn(stop, self.stopdict, msg = stop + ' not in stopdict')
    
    def test_all_lines_exist(self): 
        with open('tramlines.txt','r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if (row == []):
                    continue
                current_str = row[0]
                tramLine = current_str[:len(current_str) - 1]
                if (tramLine.isnumeric()):
                    self.assertIn(tramLine, self.linedict, msg= tramLine + ' not in linedict')
    
    def test_all_stops_in_tramline(self): 
        with open('tramlines.txt','r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if (row == []):
                    continue
                current_str = row[0]
                tramLine = current_str[:len(current_str) - 1]
                if (tramLine.isnumeric()):
                    tram = tramLine
                else: 
                    stop = current_str[:-5].strip()
                    self.assertIn(stop, self.linedict[tram], msg = stop + ' not in line ' + tram)

    def test_all_distance_feasible(self):
        for stop1 in self.stopdict: 
            for stop2 in self.stopdict: 
                d = distance_between_stops(self.stopdict, stop1, stop2)
                #print(d)
                self.assertGreater(20, d, msg = stop1 + ' to ' + stop2 + ' not feasible')
    
    def test_time_equal_both_way(self): 
        for stop_a in self.timedict: 
             for stop_b in self.timedict[stop_a]:
            # Check if both stops exist in timedict
                if stop_b in self.timedict and stop_a in self.timedict.get(stop_b, {}):
                    time1 = self.timedict[stop_a][stop_b]
                    time2 = self.timedict[stop_b][stop_a]
                    self.assertEqual(time1, time2, msg=f'Time between {stop_a} and {stop_b} not the same for both ways')
                else:
                # If either stop doesn't exist in timedict for the reverse route
                    self.assertTrue(stop_b not in self.timedict or stop_a not in self.timedict.get(stop_b, {}), 
                                msg=f'Reverse route from {stop_b} to {stop_a} does not exist or is not recorded')


        
    

if __name__ == '__main__':
    unittest.main()




   
