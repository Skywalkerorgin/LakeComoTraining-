setwd("C:/Users/Rohini/Box Sync/LakeComo/streamflow/data/sol308")
data=read.delim("drought_year.txt", header = FALSE, sep = "\t")
newdata <- data[order(data$V4),]

setwd("C:/Users/Rohini/Box Sync/LakeComo/streamflow/data/sol308/drought")
#reference=read.delim("HydroInfo_100_thinned.resultfile", header = FALSE, sep = " ")
#vector=seq(1,4745,13)
vector=seq(1,365,1)
for (i in vector){
  newdata=data[i,1:3]
  filename=paste("day",as.character(data[i,4]),".txt",sep="")
  write.table(newdata,file=filename,col.names = F, row.names = F)
}


setwd("C:/Users/Rohini/Box Sync/LakeComo/streamflow/data")
data=read.delim("Sol313_streamflow.txt", header = FALSE, sep = "\t")
newdata <- data[order(data$V4),]

setwd("C:/Users/Rohini/Box Sync/LakeComo/streamflow_precip/streamflow")
#reference=read.delim("HydroInfo_100_thinned.resultfile", header = FALSE, sep = " ")
vector=seq(1,4745,13)
for (i in vector){
  newdata=data[i:(i+12),1:3]
  filename=paste("day",as.character(data[i,4]),".txt",sep="")
  write.table(newdata,file=filename,col.names = F, row.names = F)
}
