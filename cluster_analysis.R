#libraries
library(raster)
library(RColorBrewer)

get_dendro <- function(matrix){
  matrix[matrix=="NaN"] <- 0.0
  matrix[matrix==NaN] <- 0.0
  return(hclust(as.dist(1-matrix)))
}

analyse_clusters <- function(clust, labels, matrix, k){
  clusters_info <- NULL
  for (i in 1:k) {
    cluster <- row.names(matrix[clust==i,])
    cluster_info <- analyse_cluster(cluster, labels)
    cluster_name <- rep(paste("c", i, sep=""), 6)
    cluster_len <- rep(length(cluster), 6)
    cluster_info <- cbind(cluster_name, cluster_len, cluster_info)
    clusters_info <- rbind(clusters_info, cluster_info)
  }
  return(clusters_info)
}

analyse_cluster <- function(cluster, labels){
  clust_labels <- labels[labels$datasets %in% cluster,]
  top5_assay <- sort(table(clust_labels$assay), decreasing=T)[1:5]
  top5_celltype <- sort(table(clust_labels$cellType), decreasing=T)[1:5]
  top5_consortium <- sort(table(clust_labels$consortium), decreasing=T)[1:5]
  
  cluster_info<-NULL
  
  for (i in 1:5) {
    row <- rep(NA, 9)
    
    #assay
    count <- unname(top5_assay[i])
    label <- names(top5_assay[i])
    pct_cluster <- count/length(cluster)
    pct_label <- count/sum(labels$assay == label)
    
    row[1] <- label
    row[2] <- pct_cluster
    row[3] <- pct_label
    
    #celltype
    count <- unname(top5_celltype[i])
    label <- names(top5_celltype[i])
    pct_cluster <- count/length(cluster)
    pct_label <- count/sum(labels$cellType == label)
    
    row[4] <- label
    row[5] <- pct_cluster
    row[6] <- pct_label
    
    #consortium
    count <- unname(top5_consortium[i])
    label <- names(top5_consortium[i])
    pct_cluster <- count/length(cluster)
    pct_label <- count/sum(labels$consortium == label)
    
    row[7] <- label
    row[8] <- pct_cluster
    row[9] <- pct_label
    
    cluster_info <- rbind(cluster_info, row)
  }
  
  row <- rep(NA, 9)
  
  #top1 combinations
  #assay+celltype
  label1 <- names(top5_assay[1])
  label2 <- names(top5_celltype[1])
  count <- sum(clust_labels$assay == label1 & clust_labels$cellType == label2)
  pct_cluster <- count/length(cluster)
  pct_label <- count/sum(labels$assay == label1 & labels$cellType == label2)
  
  row[1] <- paste(label1,"+",label2,sep="")
  row[2] <- pct_cluster
  row[3] <- pct_label
  
  #assay + consortium
  label1 <- names(top5_assay[1])
  label2 <- names(top5_consortium[1])
  count <- sum(clust_labels$assay == label1 & clust_labels$consortium == label2)
  pct_cluster <- count/length(cluster)
  pct_label <- count/sum(labels$assay == label1 & labels$consortium == label2)
  
  row[4] <- paste(label1,"+",label2,sep="")
  row[5] <- pct_cluster
  row[6] <- pct_label
  
  #celltype+consortium
  label1 <- names(top5_celltype[1])
  label2 <- names(top5_consortium[1])
  count <- sum(clust_labels$cellType == label1 & clust_labels$consortium == label2)
  pct_cluster <- count/length(cluster)
  pct_label <- count/sum(labels$cellType == label1 & labels$consortium == label2)
  
  row[7] <- paste(label1,"+",label2,sep="")
  row[8] <- pct_cluster
  row[9] <- pct_label
  
  cluster_info <- rbind(cluster_info, row)
  row.names(cluster_info) <- NULL
  return(cluster_info)
}

main <- function(){
  args <- commandArgs(trailingOnly=T)
  matrixFile <- "/Users/Jon/Desktop/ARI/hg19.mat"
  labelFile <- "/Users/Jon/Desktop/ARI/all.csv"
  nb_clusters <- 6
  
  #read files
  matrix <- as.matrix(read.csv(matrixFile, header=T, sep='\t', row.names=1, as.is=T, check.names=F))
  labels <- read.csv(labelFile)
  
  #reorder alphabetically
  matrix <- matrix[order(row.names(matrix)), order(row.names(matrix))]
  
  #cluster
  dendro <- get_dendro(matrix)
  
  clust <- cutree(dendro, k=nb_clusters)
  clusters_info <- analyse_clusters(clust, labels, matrix, nb_clusters)
  write.table(clusters_info, file="/Users/Jon/Desktop/test.txt", sep="\t", row.names=F, col.names=F)
}

main()
