# Team8: PhaseSpecific Chromatin Changes

## 🎯Project Objectives

Chromatin undergoes dynamic structural changes throughout the cell cycle to regulate DNA accessibility, replication, and segregation. These transformations ensure that the genome remains transcriptionally active when required, is accurately replicated, and properly segregated during cell division. While the general principles of chromatin conformation changes are gradually being uncovered, much less is known about the specific structural transitions that may drive chromatin organization throughout the cell cycle.

Our project aims to comprehensively integrate multi-omics datasets—including gene expression, chromatin accessibility, and contact maps—to advance the understanding of cell cycle phase-specific chromatin dynamics. Coupled with 3D genome modeling, our approach seeks to uncover novel and distinct chromatin conformational changes along the trajectory of cell cycle progression and other genomic processes such as cellular maturation. We employ state-of-the-art 3D modeling techniques that incorporate temporal information from the cell cycle, alongside cutting-edge methods for multi-omics integration, clustering, and pattern recognition. This combined strategy is designed to reveal common principles and patterns underlying chromatin structural organization within the cell nucleus.

## 📦 Dataset

The method was primarily tested on the ChAIR data set from (Chai et al. 2025) which combines contacts from ChIA-PET methodology, scRNA-seq and scATAC-seq obtained simultaneously for thousands of cells along the cell cycle trajectory. Our algorithms are also compatible with other similar multi-omics data sets. Similarily the 3D modeling strategy ChromMovie is applicable to different types of single cell contact data.

## 🛠 Tools & Dependencies

```
ArchR
scHiCyclePred
CIRCLET
ChromMovie
```

## 🧠 Methodology

#### Aggregation of average gene expresion per Phase and Pseudotime of K562 data (Agregation.ipynb)

1. Load statistics file after Seurat – only filtered cells left, which have both the ATAC and RNAseq signal. Infor,mation about Phase of the cells and Pseudotime.
2. Loading EnsemblID 2 Gene Name mapping – Gene names downloaded friom Ensembl Biomart.
3. Getting gene counts per cell from cellranger BAM file – parsing CB and GX fields (from uniq UMIs)
4. Creating expression matrix for filtered cells – Merge metadata with expression matrix.
5. Normalization per read counts per cell – Normalize gene counts per cell to 10,000 (Counts per 10k).
6. Aggregation by Phase and Pseudotime – Compute average gene expression per cell cycle phase.
7. Working on graphs.

## 📉 Hackathon work flowchart

```mermaid
graph TD;
    RNA(scRNA-seq)-->|Seurat, Scanpy|T(multidimentional tensor);
    ATAC(scATAC-seq)-->|ArchR|T;
    HiC(sc contacts)-->|scHiCyclePred, CIRCLET|T;
    HiC(sc contacts)-->|ChromMovie|3D(3D models);
    3D-->STdata(spatiotemporal data);
    T-->STdata;
    T-->classification(Classification);
    STdata-->Cluster(clusterization, AE, etc.);
    Cluster-->FDA(FDA);
```

## 🧬 Output

The output to our methods consists of a number of structures representing typical chromatin conformational changes detected in the studied case. The files are saved in the `.cif` format with additional `.gif` visualization files.

| Cluster 1  |  Cluster 2 | Cluster 3 | ... |
:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:
![centroid_0](https://github.com/user-attachments/assets/9f0382cb-8d35-4f7c-99ba-b37baa780f28) | ![centroid_5](https://github.com/user-attachments/assets/6b7f7820-4574-4df7-9057-84c867c3c355) | ![centroid_3](https://github.com/user-attachments/assets/ec3728d2-bd32-43f5-a6ee-427f9923727d) | ...



## 🏗 Future steps

1. Parameter tuning
2. Better integration of the multi-omics data (scRNA-seq, scATAC-seq, scChIA-PET,...)
3. Explore better characterizations of chromatin conformational changes
4. Explore better clustering algorithms
5. Explore the algorithms for determining representative structures via Functional Data Analysis (FDA) and other methods

## 🧾 Contributions

Krzysztof Banecki - team lead, 3D modeling, chromatin structure analysis

Rafał Wóycicki - RNA-seq analysis

Alicja M. Olszewska - RNA-seq analysis

Konrad Dębski - ATAC-seq analysis

Jatin Shrinet - scChIA-PET analysis

## 📌 References

1. Haoxi Chai, Xingyu Huang, Guangzhou Xiong, Jiaxiang Huang, Katarzyna Karolina Pels, Lingyun Meng, Jin Han, Dongmei Tang, Guanjing Pan, Liang Deng, Qin Xiao, Xiaotao Wang, Meng Zhang, Krzysztof Banecki, Dariusz Plewczynski, Chia-Lin Wei, Yijun Ruan, Tri-omic mapping revealed concerted dynamics of 3D epigenome and transcriptome in brain cells, Nature Methods (2025). https://doi.org/10.1038/s41592-025-02658-7

