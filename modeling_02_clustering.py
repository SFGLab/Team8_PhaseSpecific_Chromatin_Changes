import numpy as np
import pandas as pd
import os
import argparse
from tqdm import tqdm
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import imageio
from PIL import Image
import matplotlib.pyplot as plt


def main(data_input, path_out, n_clusters=5, random_state=42, length=10, width=5):
    
    if not os.path.exists(path_out): os.makedirs(path_out)

    # Clustering
    data_input = np.load(data_input)
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
    labels = kmeans.fit_predict(data_input)
    centroids = kmeans.cluster_centers_
    
    # Extracting centroids and creating animations
    path_frames = os.path.join(path_out, "test")
    if not os.path.exists(path_frames): os.makedirs(path_frames)
            
    for i in range(len(centroids)):
        structures = []
        for w in range(width):
            structure = centroids[i][w*length*3 : (w+1)*length*3]
            structure = np.array(structure).reshape((length,3))
            structures.append(structure)
        directory = os.path.join(path_out, f"centroid_{i}")
        if not os.path.exists(directory): os.makedirs(directory)
            
        # List to store file paths of saved images
        filenames = []
        images = []
        # Generate multiple plots
        for j in range(len(structures)):
            fig, ax = plt.subplots(1, 1, figsize=(4, 4))
            ax.scatter(structures[j][:,0], structures[j][:,1], s=30)
            ax.plot(structures[j][:,0], structures[j][:,1], linewidth=3)
            ax.set_xticks([])
            ax.set_yticks([])
            
            filename = os.path.join(path_frames, f"frame{i}_{j}.png")
            plt.tight_layout()
            
            plt.savefig(filename)
            plt.close(fig)
            filenames.append(filename)
        
        # Create GIF
        images = [Image.open(os.path.join(path_frames, f"frame{i}_{j}.png")) for j in range(len(structures))]
        images[0].save(os.path.join(directory, f'centroid_{i}.gif'),
                       save_all=True,
                       append_images=images[1:],
                       duration=500,
                       loop=0)
        
    # Remove temporary image files
    for filename in os.listdir(path_frames):
        os.remove(os.path.join(path_frames, filename))
    os.rmdir(path_frames)


if __name__ == "__main__":
    """
    Clusters the motif files, extracts centroids and creates gif files.
    """

    parser = argparse.ArgumentParser(description="A script that clusters the motif files, extracts centroids and creates gif files.")
    parser.add_argument("--input", type=str, help="Input folder containing npy results of motif extraction.")
    parser.add_argument("--output", type=str, help="Output folder containing resulting gif files.")
    parser.add_argument("--nc", type=int, help="Number of clusters.")
    parser.add_argument("--seed", type=int, help="Random seed.")
    parser.add_argument("-l", type=int, help="Length of the studied sequences.")
    parser.add_argument("-w", type=int, help="Width of the studied time interval.")
    
    args = parser.parse_args()
    
    main(args.input, args.output, args.nc, args.seed, args.l, args.w)
    
    