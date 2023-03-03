#%%

import pydot
import networkx as nx
import pandas as pd

#%%
#Transition probabilities
df = pd.read_csv('probabilities.csv', index_col=0)
df
#%%
#Possible states
states = ['checkout','dairy','drinks','entrance', 'fruit','spices']

# create a function that maps transition probability dataframe
# to markov edges and weights
def _get_markov_edges(Q):
    edges = {}
    for col in Q.columns:
        for idx in Q.index:
            edges[(idx,col)] = Q.loc[idx,col]
    return edges
edges_wts = _get_markov_edges(df)
#pprint(edges_wts)
# create graph object
G = nx.MultiDiGraph()
# nodes correspond to states
G.add_nodes_from(states)
print(f'Nodes:\n{G.nodes()}\n')
# edges represent transition probabilities
for k, v in edges_wts.items():
    if v > 0.0:
        tmp_origin, tmp_destination = k[0], k[1]
        G.add_edge(tmp_origin, tmp_destination, weight=[v], label=[v])

        #G.add_edge(tmp_origin, tmp_destination, weight=v, label=v)
pos = nx.drawing.nx_pydot.graphviz_layout(G, prog='dot')
nx.draw_networkx(G, pos)
# create edge labels for jupyter plot but is not necessary
edge_labels = {(n1,n2):d['label'] for n1,n2,d in G.edges(data=True)}

nx.draw_networkx_edge_labels(G , pos, edge_labels=edge_labels)
nx.drawing.nx_pydot.write_dot(G, 'markov.dot')
(graph,) = pydot.graph_from_dot_file('markov.dot')
graph.write_png('markov.png')


from PIL import Image
IN_PATH = "markov.png"
OUT_PATH = "resized_markov.png"
def white_square(source_image):
    size = tuple([2*i for i in source_image.size])
    layer = Image.new("RGB", size, (255, 255, 255))
    layer.paste(
        source_image,
        tuple(map(lambda x: int((x[0] - x[1]) / 2), zip(size, source_image.size))),
    )
    return layer
if __name__ == "__main__":
    img = Image.open(IN_PATH)
    framed_img = white_square(img)
    framed_img = framed_img.resize((100, 100), Image.ANTIALIAS)
    framed_img.save(OUT_PATH)