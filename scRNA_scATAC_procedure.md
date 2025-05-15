# Integrated RNA + ATAC-seq Analysis by Cell Cycle Phase and Pseudotime

## Step 1: Load Seurat Statistics and Filtered Cell Metadata

**Input**: `seurat_stats.tsv` or `.rds`

- Retain only high-quality cells that are shared between RNA-seq and ATAC-seq datasets.
- Extract metadata:
  - Cell barcodes (CB)
  - Cell cycle Phase
  - Pseudotime or Metacell assignment

---

## Step 2: Load Gene Annotation Mapping

**Input**: Ensembl ID ↔ Gene Name table (from Ensembl BioMart)

- **Purpose**: Map raw gene IDs to human-readable names for interpretability and merging.

---

## Step 3: Create Raw Expression Matrix

**Input**: CellRanger BAM or UMI count matrix

- Extract unique gene counts per cell using BAM tags:
  - `CB` = cell barcode  
  - `GX` = gene ID (Ensembl)

- **Result**: Sparse matrix of shape (genes × cells)

---

## Step 4: Filter and Align Expression Data

- Keep only those cell barcodes present in filtered metadata.
- Merge gene expression matrix with metadata (Phase, Pseudotime).

---

## Step 5: Normalize RNA Expression

For each cell:
- Compute total UMI count
- Normalize each gene count as:

```text
Normalized count = (raw count / total per cell) × 10^4
