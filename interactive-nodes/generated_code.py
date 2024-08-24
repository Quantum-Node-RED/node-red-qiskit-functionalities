import base64
import io
import json
import warnings
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

def visualise_graph(matrix):
        
    # Suppress specific warnings
    warnings.filterwarnings('ignore', category=UserWarning)
        
    # Create graph from numpy matrix
    G = nx.from_numpy_array(matrix)
    layout = nx.random_layout(G, seed=10)
        
    # Generate node colors
    num_nodes = len(G.nodes)
    colors = plt.cm.rainbow(np.linspace(0, 1, num_nodes))
        
    # Draw graph
    nx.draw(G, layout, node_color=colors)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels)
        
    # Save graph to a buffer instead of a file
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
        
    # Encode buffer contents to base64
    buffer.seek(0)
    b64_str = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
        
    return b64_str

import traceback
try:
    weight_matrix = np.array(eval("[[0.0, 1.0, 1.0, 0.0], [1.0, 0.0, 1.0, 1.0], [1.0, 1.0, 0.0, 1.0], [0.0, 1.0, 1.0, 0.0]]"))
    graph = visualise_graph(weight_matrix)
    print(json.dumps(graph))
    
except Exception as e:
    print(f'An error occurred: {e}')
    print(traceback.format_exc())
