import graphs

colors = ['blue', 'purple', 'brown', 'red', 'black']

def simplyfy(graph, n=4):
    reduced_graph = {}
    for vtx in graph.vertices():
        if len(graph.neighbours(vtx)) < n:
            reduced_graph[vtx] = graph.neighbours(vtx)
    for vtx in reduced_graph:
        graph.remove_vertex(vtx)
    if not reduced_graph:
        raise ValueError(f"Input graph cannot be simplyfied with n = {n}")
    return list(reduced_graph.items())

def rebuild(graph, stack, colors):
    n = len(colors)
    colormap = {}
    for vtx, nbs in reversed(stack):
        graph.add_vertex(str(vtx))
        for nb in nbs:
            graph.add_edge(str(vtx), str(nb))
        available_colors = colors[:]
        for neighbour in graph.neighbours(str(vtx)):
            if neighbour in colormap:
                available_colors.remove(colormap[neighbour])
        colormap[str(vtx)] = available_colors[-1]
    return colormap

def viz_color_graph(graph, colors):
    n = len(colors)
    stack = simplyfy(graph, n)
    colormap = rebuild(graph, stack, colors)
    graphs.visualize(graph, nodecolors=colormap)

def demo():
    G = graphs.Graph([(1,2),(1,3),(1,4),(3,4),(3,5),(3,6), (3,7), (6,7)])
    viz_color_graph(G,['red', 'green', 'blue'])

if __name__ == '__main__':
    demo()
