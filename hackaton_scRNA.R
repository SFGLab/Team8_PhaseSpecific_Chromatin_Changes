if (!require("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
BiocManager::install(version = "3.21")
install.packages('Seurat')
setRepositories(ind = 1:3, addURLs = c('https://satijalab.r-universe.dev', 'https://bnprks.r-universe.dev/'))
install.packages(c("BPCells", "presto", "glmGamPoi"))

library(Seurat)

devtools::install_github('satijalab/seurat-data')

library(SeuratData)
# install the dataset and load requirements

InstallData("pbmcMultiome")