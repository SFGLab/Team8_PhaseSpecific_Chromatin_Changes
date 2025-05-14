import numpy as np
import pandas as pd
import os
import argparse
from tqdm import tqdm
from Bio.PDB import qcprot


def get_kmers(dfs, length=200, width=5):
    n = len(dfs)
    kmers = []
    reference_structure = np.array(dfs[0][['x', 'y', 'z']].iloc[0:length,:])
    
    for i in tqdm(range(dfs[0].shape[0]-length)):
        if i%length==0:
            chrom = dfs[0]["chr"].iloc[i]
            chrom_end = dfs[0]["chr"].iloc[i+length-1]
            if chrom == chrom_end:
                for df_id in range(n-width+1):
                    if df_id%width == 0:
                        sub_structures = []
                        for j in range(width):
                            structure_array = np.array(dfs[df_id+j][['x', 'y', 'z']].iloc[i:i+length,:])
                            # if j==0:
                            #     R, t = kabsch(structure_array, reference_structure)
                            # structure_array = apply_transformation(structure_array, R, t)
                                
                            structure_array = get_qcp_fit_model(reference_structure, structure_array)
                            flat_vector = structure_array.flatten()
                            flat_vector = flat_vector - flat_vector.mean()
                            sub_structures.append(flat_vector)
                        kmers.append( np.hstack(sub_structures) )
    return np.vstack(kmers)


def get_angle(A, B, C):
    BA = A - B
    BC = C - B
    cos_angle = np.dot(BA, BC) / (np.linalg.norm(BA) * np.linalg.norm(BC))
    cos_angle = np.clip(cos_angle, -1.0, 1.0)
    
    angle_rad = np.arccos(cos_angle)
    # angle_deg = np.degrees(angle_rad)
    return angle_rad


def get_kmers_angles(dfs, length=200, width=5):
    n = len(dfs)
    kmers = []
    reference_structure = np.array(dfs[0][['x', 'y', 'z']].iloc[0:length,:])
    
    for i in tqdm(range(dfs[0].shape[0]-length)):
        if i%length==0:
            chrom = dfs[0]["chr"].iloc[i]
            chrom_end = dfs[0]["chr"].iloc[i+length-1]
            if chrom == chrom_end:
                for df_id in range(n-width+1):
                    if df_id%width == 0:
                        sub_angles = []
                        for j in range(width):
                            structure_array = np.array(dfs[df_id+j][['x', 'y', 'z']].iloc[i:i+length,:])
                            for k in range(structure_array.shape[0] - 3 + 1):
                                sub_angles.append(get_angle(structure_array[k,:], structure_array[k+1,:], structure_array[k+2,:]))
                            
                        kmers.append( np.hstack(sub_angles) )
    return np.vstack(kmers)


def extrapolate_points(points, n):
    n1 = len(points)
    total_len = n1 - 1
    points_new = [points[0]]
    for i in range(1, n):
        curr_len = total_len * i / (n - 1)
        p1 = points[int(curr_len // 1)]
        if curr_len // 1 == n1 - 1:
            points_new.append(p1)
        else:
            p2 = points[int(curr_len // 1) + 1]
            alpha = curr_len % 1
            p = (p1[0] * (1 - alpha) + p2[0] * alpha, p1[1] * (1 - alpha) + p2[1] * alpha,
                 p1[2] * (1 - alpha) + p2[2] * alpha)
            points_new.append(p)
    return points_new


def get_qcp_fit_model(image_structure, gd_structure):
    """
    applying the QCP transformation to fit into the points of the image
    :param image_structure: list of points from the image to which other structure is to be transformed
    :param gd_structure: structure to transform
    :return: transformed structure
    """
    n = len(image_structure)
    gd_points = np.array(extrapolate_points(gd_structure, n))
    qcp_transformation = qcprot.QCPSuperimposer()
    qcp_transformation.set(reference_coords=np.array(image_structure), coords=gd_points)
    qcp_transformation.run()
    return qcp_transformation.get_transformed()


def kabsch(P, Q):
    """Aligns P onto Q using the Kabsch algorithm."""
    # Subtract centroids
    Pc = P - P.mean(axis=0)
    Qc = Q - Q.mean(axis=0)

    # Covariance matrix
    C = np.dot(Pc.T, Qc)

    # Singular value decomposition
    V, S, Wt = np.linalg.svd(C)
    d = np.sign(np.linalg.det(np.dot(V, Wt)))
    D = np.diag([1, 1, d])

    # Optimal rotation
    U = np.dot(np.dot(V, D), Wt)

    # Save the transformation
    rotation = U
    translation = Q.mean(axis=0) - np.dot(P.mean(axis=0), U)

    return rotation, translation


def apply_transformation(X, rotation, translation):
    """Apply saved transformation to structure X."""
    return np.dot(X, rotation) + translation
    

def main(path_in, path_out, length=10, width=5):
    
    if not os.path.exists(path_out): os.makedirs(path_out)
    files_df = os.listdir(path_in)
    files_df.sort()
    dfs = [pd.read_csv(os.path.join(path_in, file), index_col=0) for file in files_df]

    kmers = get_kmers(dfs, length=length, width=width)
    np.save(os.path.join(path_out, f"kmers_l{length}_w{width}.npy"), kmers)


if __name__ == "__main__":
    """
    Converts cif files from the path into pandas DataFrames.
    """
    
    parser = argparse.ArgumentParser(description="A script that greets the user.")
    parser.add_argument("--input", type=str, help="Input folder containing dataframe files.")
    parser.add_argument("--output", type=str, help="Out folder for storing resulting npy arrays.")
    parser.add_argument("-l", type=int, help="Length of the studied sequences.")
    parser.add_argument("-w", type=int, help="Width of the studied time interval.")
    
    args = parser.parse_args()
    
    main(args.input, args.output, args.l, args.w)



