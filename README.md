# Team8_PhaseSpecific_Chromatin_Changes

```mermaid
graph TD;
    RNA(scRNA-seq)-->|Seurat, Scanpy|T(multidomentional tensor);
    ATAC(scATAC-seq)-->T;
    HiC(sc contacts)-->|scHiCyclePred, CIRCLET|T;
    HiC(sc contacts)-->|ChromMovie|3D(3D models);
    3D-->STdata(spatiotemporal data);
    T-->STdata;
    T-->classification(Classification);
    STdata-->Cluster(clusterization, AE, etc.);
    Cluster-->FDA(FDA);
```
