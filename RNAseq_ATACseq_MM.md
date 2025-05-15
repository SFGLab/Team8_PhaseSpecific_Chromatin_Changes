# Materials and Methods

## Cell Metadata and Quality Control

Single-cell RNA-seq and ATAC-seq data were analyzed for *K562* cells. Metadata including cell barcodes, RNA library size (`nCount_RNA`), cell cycle phase (G1, S, G2/M), and metacell identity were derived from a Seurat object (`k562.dis.stat.txt`). Only cells present in both RNA and ATAC datasets were retained for downstream analysis.

## Gene Annotation and Promoter Region Definition

Gene annotations were obtained from Ensembl (release 114, GRCh38). Gene coordinates were extracted from the corresponding GTF file using custom parsing of entries with `feature type = gene`. Promoter regions were defined as ±500 base pairs from the transcription start site (TSS), adjusted based on gene strand orientation. These regions were saved in BED format for downstream intersection.

## scATAC-seq Processing and Promoter Accessibility Quantification

ATAC-seq fragments were provided in BED format, including chromosome, start, end, cell barcode, and count fields. Only fragments corresponding to the filtered cell barcodes were retained. Promoter accessibility was determined by intersecting filtered ATAC fragments with the promoter BED file using `bedtools intersect`. This resulted in a mapping of accessible regions to associated genes.

A gene-by-cell matrix of ATAC accessibility was constructed by counting the number of promoter-overlapping fragments per gene per cell. The resulting counts were normalized per cell by total fragment count and scaled to 10,000 to produce counts-per-10k (CP10K) values, analogous to RNA normalization. The normalized ATAC matrix was saved as both TSV and Parquet files for integration.

## scRNA-seq Processing and Expression Matrix Generation

Aligned single-cell RNA-seq reads were processed from a BAM file (`k562.allele.flt.M.bam_filterd.sam.bam`) using the `pysam` Python package. Cell barcodes (`CB`) and gene annotations (`GX`) were extracted from alignment tags to build a raw count matrix of genes × cells. Only reads associated with the filtered cell barcodes were included.

The resulting count matrix was normalized per cell by library size and scaled to CP10K. Gene names were mapped from Ensembl IDs using a lookup table generated via BioMart (`features_mapped.tsv`).

## Aggregation by Cell Cycle Phase and Pseudotime (Metacell)

Normalized RNA expression values were aggregated:

- **By cell cycle phase**, by averaging gene expression across all cells within each phase.
- **By pseudotime (metacell)**, using the average of each gene across all cells within each metacell.

A similar aggregation was performed on the ATAC-seq matrix, computing mean accessibility per gene across cells within the same metacell. For downstream integration, both RNA and ATAC matrices were subset to common genes and joined by metacell identity.

## Integration of RNA and ATAC Profiles

The final integrated matrix included normalized gene expression and chromatin accessibility for matched genes across metacells. This matrix enabled joint visualization and correlation analysis of promoter accessibility and gene expression along the pseudotemporal trajectory. The merged dataset was saved in TSV format (`k562.allele.flt.M_atacrnamerged.tsv`) for downstream analyses.
