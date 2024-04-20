import unittest
from Tram import TramNetwork, readTramNetwork

class TestTramNetwork(unittest.TestCase):

    def setUp(self):
        self.tram_network = readTramNetwork()

    def test_stop_position(self):
        # Test that stop_position method returns correct positions
        expected_position = (57.7399617, 12.0286261)  
        actual_position = self.tram_network.stop_position("Beväringsgatan")
        self.assertEqual(expected_position, actual_position)

    def test_transition_time(self):
        expected_time = 11  
        actual_time = self.tram_network.transition_time("SKF", "Valand")
        self.assertEqual(expected_time, actual_time)

    def test_geographical_distance(self):
        # Test the geographical distance function
        expected_distance = 2.0 
        actual_distance = self.tram_network.geographical_distance("SKF", "Valand")
        self.assertAlmostEqual(expected_distance, actual_distance, places=1)

    def test_lines_through_stop(self):
        # Test to check if correct lines are returned for a given stop
        expected_lines = ["11", "7"]  
        actual_lines = self.tram_network.lines_through_stop("SKF")
        self.assertListEqual(expected_lines, sorted(actual_lines))

    def test_stops_along_line(self):
        # Test to check if correct stops are returned for a given line
        expected_stops = ["Stop1", "Stop2", "Stop3"]
        actual_stops = self.tram_network.stops_along_line("Line1")
        self.assertListEqual(expected_stops, actual_stops)

    def test_all_stops(self):
        # Test to check if all stops are listed
        expected_stops = ["Stop1", "Stop2", "Stop3", "Stop4"]
        actual_stops = self.tram_network.all_stops()
        self.assertCountEqual(expected_stops, actual_stops)

    def test_all_lines(self):
        # Test to check if all lines are listed
        expected_lines = ["Line1", "Line2"]
        actual_lines = self.tram_network.all_lines()
        self.assertCountEqual(expected_lines, actual_lines)
    
    
    def BFS(self, G, start_node):
        # Perform BFS and return a list of nodes in the order they were explored.
        Q = deque([start_node])
        explored = set([start_node])
        
        while Q:
            v = Q.popleft()
            for w in G.neighbours(v):
                if w not in explored:
                    explored.add(w)
                    Q.append(w)
        return list(explored)

    def test_breath_search(self):
        # Test to check if the graph is fully connected.
        all_nodes = set(self.tn.vertices())
        for start_node in all_nodes:
            explored_nodes = set(self.BFS(self.tn, start_node))
            self.assertEqual(all_nodes, explored_nodes, f"Graph not connected at node {start_node}")

# Run the tests
if __name__ == '__main__':
    unittest.main()

