import numpy as np
import pandas as pd
import os
import argparse
from tqdm import tqdm


def read_cif(path):
    df = pd.DataFrame(columns=["chr", "x", "y", "z"])
    with open(path, 'r') as f:
        for line in f:
            if line.startswith("ATOM"):
                line_split = line.split()
                chrom = line_split[6]
                x, y, z = line_split[-3:]
                df.loc[df.shape[0]] = [chrom, x, y, z]
    return df


def main(path_in):
    path_out = path_in[:-3]+"pd"
    if not os.path.exists(path_out): os.makedirs(path_out)
    files = os.listdir(path_in)

    for file in tqdm(files):
        if file.startswith("step099"):
            df = read_cif(os.path.join(path_in, file))
            df.to_csv(os.path.join(path_out, file.split(".")[0]+".csv"))

if __name__ == "__main__":
    """
    Converts cif files from the path into pandas DataFrames.
    """

    parser = argparse.ArgumentParser(description="A script that greets the user.")
    parser.add_argument("--input", type=str, help="Input folder containing cif files.")
    args = parser.parse_args()
    
    main(args.input)
    
    

