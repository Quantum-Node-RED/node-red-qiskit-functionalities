import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import base64
import io
import os
from PIL import Image, ImageDraw, ImageFont

def visualize_graph(w, folder=".", filename="graph.png"):
    """Visualizes a graph given its adjacency matrix and saves it in the specified folder."""
    G = nx.from_numpy_array(w)
    layout = nx.random_layout(G, seed=10)
    
    # Ensure colors list matches the number of nodes
    num_nodes = len(G.nodes)
    colors = plt.cm.rainbow(np.linspace(0, 1, num_nodes))
    
    nx.draw(G, layout, node_color=colors)
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels)
    
    # Ensure the folder exists
    os.makedirs(folder, exist_ok=True)
    
    # Save the plot as an image in the specified folder
    filepath = os.path.join(folder, filename)
    plt.savefig(filepath)
    plt.close()
    return filepath

def save_circuit_image(qc, filename):
    """Saves a QuantumCircuit as an image."""
    fig = qc.draw(output='mpl')
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    with open(filename, 'wb') as f:
        f.write(base64.b64decode(img_str))
    buf.close()
    return filename

def encode_image_to_base64(filename):
    """Encodes an image file to base64."""
    with open(filename, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def combine_images(image_filenames, output_filename, columns=None):
    """Combines multiple images into a single image."""
    images = [Image.open(f) for f in image_filenames]
    widths, heights = zip(*(i.size for i in images))

    # Determine the number of columns
    if columns is None:
        columns = int(np.sqrt(len(images)))  # Default to a square grid

    # Determine the number of rows
    rows = (len(images) + columns - 1) // columns

    # Calculate the width and height of the combined image
    max_width = max(widths)
    max_height = max(heights)
    total_width = columns * max_width
    total_height = rows * max_height

    # Create a new blank image with white background
    combined_image = Image.new('RGB', (total_width, total_height), color='white')

    # Load a font
    font = ImageFont.load_default()

    # Paste each image onto the blank canvas and annotate
    for index, img in enumerate(images):
        row = index // columns
        col = index % columns
        x_offset = col * max_width
        y_offset = row * max_height
        combined_image.paste(img, (x_offset, y_offset))

        # Annotate the image with its sequence number
        draw = ImageDraw.Draw(combined_image)
        text = str(index + 1)
        text_position = (x_offset + 10, y_offset + 10)  # Position the text with some padding
        draw.text(text_position, text, fill="black", font=font)

    # Save the combined image
    combined_image.save(output_filename)
    return output_filename
