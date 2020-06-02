
import networkx as nx

names = dir( nx )
nx.__version__

if( 'Graph' in names ):
    print('EXISTS')

#CREATE GRAPH
G = nx.Graph()

#ADD NODE
G.add_node(1)
G.add_nodes_from([2, 3])

#ADD SPECIAL NODE
H = nx.path_graph(10)
G.add_nodes_from(H)
G.add_node(H)

#ADD EDGE
G.add_edge(1, 2)
e = (2, 3)
G.add_edge(*e)

G.add_edges_from([(1, 2), (1, 3)])
G.add_edges_from(H.edges)


#REMOVING EVERYTHING
G.clear()

#REWRITING G
G.add_edges_from([(1, 2), (1, 3)])
G.add_node(1)
G.add_edge(1, 2)
G.add_node("spam")        # adds node "spam"
G.add_nodes_from("spam")  # adds 4 nodes: 's', 'p', 'a', 'm'
G.add_edge(3, 'm')


#PRINT
print( G.number_of_nodes() )
print( G.number_of_edges() )
print( list(G.nodes) )
print( list(G.edges) )
print( list(G.adj[1]) )
print( G.degree[1] )
print( G.nodes.items())
print( G.edges.items())
#OTHER
G.edges([ 2 , 'm' ])
G.degree([2,3])

#CAN REMOVE THINGS
G.remove_node(2)
G.remove_nodes_from("spam")
list(G.nodes)
G.remove_edge(1, 3)
#USING GRAPH CLASS
G.add_edge(1, 2)
H = nx.DiGraph(G)   # create a DiGraph using the connections from G
list(H.edges())
edgelist = [(0, 1), (1, 2), (2, 3)]
H = nx.Graph(edgelist)
#ACCESSING DATA
G[1]  # same as G.adj[1]
G[1][2]
G.edges[1,2]
G.add_edge(1, 3)
G[1][3]['color'] = "blue"
G.edges[1, 2]['color'] = "red"
#REDO GRAPH
FG = nx.Graph()
FG.add_weighted_edges_from([(1, 2, 0.125), (1, 3, 0.75), (2, 4, 1.2), (3, 4, 0.375)])
for n, nbrs in FG.adj.items():
    for nbr, eattr in nbrs.items():
        wt = eattr['weight']
        if wt < 0.5: print('(%d, %d, %.3f)' % (n, nbr, wt))

for (u, v, wt) in FG.edges.data('weight'):
    if wt < 0.5: print('(%d, %d, %.3f)' % (u, v, wt))
#GRAPH ATTRIBUTE
G = nx.Graph(day="Friday")
G.graph
G.graph['day'] = "Monday"
G.graph
#NODe ATTRIBUTES
G.add_node(1, time='5pm')
G.add_nodes_from([3], time='2pm')
G.nodes[1]
G.nodes[1]['room'] = 714
G.nodes.data()
#EDGE ATTRIBUTES
G.add_edge(1, 2, weight=4.7 )
G.add_edges_from([(3, 4), (4, 5)], color='red')
G.add_edges_from([(1, 2, {'color': 'blue'}), (2, 3, {'weight': 8})])
G[1][2]['weight'] = 4.7
G.edges[3, 4]['weight'] = 4.2
#DIRECTED GRAPH
DG = nx.DiGraph()
DG.add_weighted_edges_from([(1, 2, 0.5), (3, 1, 0.75)])
DG.out_degree(1, weight='weight')
DG.degree(1, weight='weight')
list(DG.successors(1))
list(DG.neighbors(1))
H = nx.Graph(G)  # convert G to undirected graph
#MULTIGRAPHS
MG = nx.MultiGraph()
MG.add_weighted_edges_from([(1, 2, 0.5), (1, 2, 0.75), (2, 3, 0.5)])
dict(MG.degree(weight='weight'))
GG = nx.Graph()
for n, nbrs in MG.adjacency():
    for nbr, edict in nbrs.items():
        minvalue = min([d['weight'] for d in edict.values()])
        GG.add_edge(n, nbr, weight = minvalue)

nx.shortest_path(GG, 1, 3)

#SOME GRAPH OPERATION
'''
subgraph(G, nbunch)      - induced subgraph view of G on nodes in nbunch
union(G1,G2)             - graph union
disjoint_union(G1,G2)    - graph union assuming all nodes are different
cartesian_product(G1,G2) - return Cartesian product graph
compose(G1,G2)           - combine graphs identifying nodes common to both
complement(G)            - graph complement
create_empty_copy(G)     - return an empty copy of the same graph class
to_undirected(G) - return an undirected representation of G
to_directed(G)   - return a directed representation of G
'''
#SOME OTHER TYPE OF GRAPH
petersen = nx.petersen_graph()
tutte = nx.tutte_graph()
maze = nx.sedgewick_maze_graph()
tet = nx.tetrahedral_graph()
#GENERATOR FOR GRAPH CLASSE
K_5 = nx.complete_graph(5)
K_3_5 = nx.complete_bipartite_graph(3, 5)
barbell = nx.barbell_graph(10, 10)
lollipop = nx.lollipop_graph(10, 20)
#IDEM
er = nx.erdos_renyi_graph(100, 0.15)
ws = nx.watts_strogatz_graph(30, 3, 0.1)
ba = nx.barabasi_albert_graph(100, 5)
red = nx.random_lobster(100, 0.9, 0.9)
#READING A GRAPH FROM A FILE
nx.write_gml(red, "path.to.file")
mygraph = nx.read_gml("path.to.file")
#ANALYSING GRAPH
G = nx.Graph()
G.add_edges_from([(1, 2), (1, 3)])
G.add_node("spam")       # adds node "spam"
list(nx.connected_components(G))
sorted(d for n, d in G.degree())
nx.clustering(G)
sp = dict(nx.all_pairs_shortest_path(G))
sp[3]
#DRAWING A CLASS

import matplotlib.pyplot as plt





