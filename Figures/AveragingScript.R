setwd("C:/Users/Rohini/Box Sync/LakeComo/SST/compromise/")
data=read.delim("Sol5.txt", header = FALSE, sep = "\t")
new=aggregate(data[, 1:3], list(data$V4), mean)
write.table(new,file="Sol5_Average.txt",append=TRUE,col.names = F, row.names = F)
