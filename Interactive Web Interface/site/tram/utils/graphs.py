import networkx as nx
import graphviz


class Graph(nx.Graph):
    def __init__(self, start=None):
        super().__init__(start)

    def vertices(self):
        # Return a list of vertices in the graph
        return list(self.nodes())
    
    def neighbours(self, v):
        # Return a list of neighbors for a given vertex
        return list(self.neighbors(v))

    def add_vertex(self, a):
        # Add a vertex to the graph
        self.add_node(a)

    def is_directed(self):
        # Check if the graph is directed
        return self.is_directed()

    def get_vertex_value(self, v):
        # Get the value associated with a vertex
        # Returns None if the vertex does not exist or if no value is set
        return self.nodes[v].get('value', None) if v in self.nodes else None

    def set_vertex_value(self, v, x):
        # Set the value for a vertex
        if v in self.nodes:
            self.nodes[v]['value'] = x







##################################################################################################
# class WeightedGraph is inherited from class Graph
class WeightedGraph(Graph):
    def __init__(self, start=None):
        super().__init__(start)
        
        
    def get_weight(self, a, b):
        if (a, b) in self.edges:
            return self[a][b].get('weight')
        return None  # or handle error
    
    def set_weight(self, a, b, w):
    # Check if edge exists
        if (a, b) in self.edges:
            self.edges[a, b]['weight'] = w
        else:
        # Handle the case where the edge doesn't exist
        # For example, you could add the edge with the weight
            self.add_edge(a, b)
            self.edges[a, b]['weight'] = w
        # Or, raise an error or log a message




############################################################################################
def costs2attributes(G, cost, attr='weight'):
    for a, b in G.edges():
        G[a][b][attr] = cost(a, b)

def dijkstra(graph, source, cost=lambda u, v: 1):
    # Convert cost function to weight attributes on the edges
    costs2attributes(graph, cost)

    # Use NetworkX's shortest_path function
    shortest_paths = nx.shortest_path(graph, source=source, weight='weight',method='dijkstra')

    return shortest_paths

############################################################################################




def visualize(graph, view='dot', name='mygraph', nodecolors={}, engine = 'dot'):
# create an instance of graphviz.Graph,
  dot = graphviz.Graph()
# loop over the vertices of graph applying node() to them,
  for i in graph.vertices():
    dot.node(str(i))
# loop over the edges of graph applying edge() to them, 
  for i,j in graph.edges():
    dot.edge(str(i),str(j))
  dot.render(view=True)
  
def view_shortest(G, source, target, cost=lambda u,v: 1):
    path = dijkstra(G, source, cost)[target]['path']
    print(path)
    colormap = {str(v): 'orange' for v in path}
    print(colormap)
    visualize(G, view='view', nodecolors=colormap)

def demo():
    G = Graph([(1,2),(1,3),(1,4),(3,4),(3,5),(3,6), (3,7), (6,7)])
    view_shortest(G, 2, 6)

if __name__ == '__main__':
        demo()