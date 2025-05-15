# Team8: PhaseSpecific Chromatin Changes

## Hackathon work flowchart

```mermaid
graph TD;
    RNA(scRNA-seq)-->|Seurat, Scanpy|T(multidomentional tensor);
    ATAC(scATAC-seq)-->|ArchR|T;
    HiC(sc contacts)-->|scHiCyclePred, CIRCLET|T;
    HiC(sc contacts)-->|ChromMovie|3D(3D models);
    3D-->STdata(spatiotemporal data);
    T-->STdata;
    T-->classification(Classification);
    STdata-->Cluster(clusterization, AE, etc.);
    Cluster-->FDA(FDA);
```

#### Aggregation of average gene expresion per Phase and Pseudotime of K562 data (Agregation.ipynb)

1. Load statistics file after Seurat – only filtered cells left, which have both the ATAC and RNAseq signal. Infor,mation about Phase of the cells and Pseudotime.
2. Loading EnsemblID 2 Gene Name mapping – Gene names downloaded friom Ensembl Biomart.
3. Getting gene counts per cell from cellranger BAM file – parsing CB and GX fields (from uniq UMIs)
4. Creating expression matrix for filtered cells – Merge metadata with expression matrix.
5. Normalization per read counts per cell – Normalize gene counts per cell to 10,000 (Counts per 10k).
6. Aggregation by Phase and Pseudotime – Compute average gene expression per cell cycle phase.

#### Adding ATACseq data to K562:
1. ATACseq script first takes ATAC seq signal file and annotate it with gene regions +- 500 bp from gene TSS.
2. The ATAC singals as 1/0 are normalized per cell and scaled by 10K factor, same as in scRNAseq analysis.
3. The ATAC signal data are filtered to contain only the cells same as in the Seurat stat file, so have same cells as in RNAseq analysis.
4. The ATAC signal data ate aggregated by Metacell (the mean signal per Metacell, so Pseudotime).,
5. The ATAC-seq and RNA-seq data are combined together for common genes.
