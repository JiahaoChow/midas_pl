This demo dataset is named TEADOG because it contains data from both TEA-seq (GSE158013) and DOGMA-seq (GSE166188) datasets. 
Each of these datasets includes RNA, ADT, and ATAC data.

We selected two batches from each dataset to create a combined dataset with four batches:
 - w1 and w6 from TEA-seq
 - lll_ctrl and dig_stim from DOGMA-seq

Next, we selected 1,000 samples (cells) from each batch, 
resulting in a total of 4,000 samples. 
To construct a mosaic dataset, we intentionally dropped some modalities.