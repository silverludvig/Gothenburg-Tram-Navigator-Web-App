
# uses randomly geneated data, covering a large number of test cases. 
# It is made available by the hypothesis library,

from hypothesis import given, strategies as st
import hypothesis
import unittest
import graph



# generate small integers, 0...10
smallints = st.integers(min_value=0, max_value=10)
# generate pairs of small integers
twoints = st.tuples(smallints, smallints)
# generate lists of pairs of small integers
# where x != y for each pair (x, y)
st_edge_list = st.lists(twoints, unique_by=(lambda x: x[0], lambda x: x[1]))
# generate list of random weights
weights_random = st.floats(min_value=1, max_value=100)
# generate edges with weights
edges_with_weight = st.tuples(twoints, weights_random)

# Define an **equality relation** between lists of edges that represent undirected graphs.
def equal(edges1, edges2):
  set1 = set([frozenset(edge) for edge in edges1])
  set2 = set([frozenset(edge) for edge in edges2])
  return set1 == set2

class TestPublicMethods(unittest.TestCase):

# Testing __len__() compare self-define graph.WeightedGraph with original graphs.WeightedGraph 
  @given(st_edge_list_with_weight)
  def test_len(self):
    self.assertEqual(len(graph.WeightedGraph())  , len(graphs.WeightedGraph()) ) #edges_with_weight


# Testing vertices()
  @given(st_edge_list_with_weight)
  def test_vertices(self):
    A = graph.WeightedGraph()
    B = graphs.WeightedGraph()
    self.assertEqual( A.nodes(), B.nodes())
       


  
# Testing neighbours()
  @given(st_edge_list_with_weight)
  def test_neighbours(self):
    A = graph.WeightedGraph()
    B = graphs.WeightedGraph()
    for i in A.nodes():
      self.assertEqual( A.neighbours(i), B.neighbours(i))


# Testing edges()
  @given(st_edge_list_with_weight)
  def test_edges(self):
    A = graph.WeightedGraph()
    B = graphs.WeightedGraph()
    self.assertEqual( A.edges(), B.edges())


# if (a, b) is in edges(), both a and b are in vertices()
  @given(st_edge_list_with_weight)






# if a has b as its neighbour, then b has a as its neighbour
  @given(st_edge_list_with_weight)






  @given(st_edge_list_with_weight)
  
  
  
  



