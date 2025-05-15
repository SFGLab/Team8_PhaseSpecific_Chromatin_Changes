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
- This yields **Counts Per 10k (CP10K)**

---

## Step 6: Aggregate RNA Expression

Group by:
- **Cell Cycle Phase**
- and/or **Pseudotime bin / Metacell**

Compute mean normalized expression per gene for each group.

---

## Step 7: Process ATAC-seq Data

**Input**: Fragment positions or accessibility regions (±500 bp from gene TSS)

- Annotate each fragment to nearby gene TSS.
- For each cell:
  - Assign binary value per gene (accessible = 1, else 0)
  - Normalize binary matrix by total accessible signals per cell, scaled to 10,000

---

## Step 8: Filter and Align ATAC Data

- Retain only cells present in RNA metadata.
- Aggregate ATAC accessibility per gene and pseudotime/metacell, computing mean accessibility.

---

## Step 9: Merge RNA and ATAC Matrices

- Match genes present in both modalities.
- Create a **combined matrix** with:
  - **Rows** = genes
  - **Columns** = pseudotime/metacell
  - **Two values per gene**: RNA expression and ATAC accessibility

---

## Step 10: Downstream Analyses

Examples:
- Correlation between promoter accessibility and expression.
- Plot gene expression and accessibility dynamics over pseudotime.
- Cluster genes by concordant/inverse dynamics.

