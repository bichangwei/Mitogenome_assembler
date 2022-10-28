# @Author: Changwei Bi
# @E-mail: bichwei@163.com
# @Function: Draw coverage distribution graph of assembly

library(ggplot2)

Cov_data <- read.table("Species.csv")
names(Cov_data)<-c("No","Name","Length","Depth")
sort(Cov_data[,4],T)

bp = ggplot(Cov_data,aes(x=Length,y=Depth,color=cyl),options(scipen = 200))+
  geom_point(col="blue")+scale_y_continuous(limits = c(0,500),breaks=seq(0,500,20))+
  scale_x_continuous(breaks=seq(0,300000,10000))+xlim(0,300000)+theme_classic()+
  scale_color_manual(values = c("#002060", "#E477AA", "#D11617"))
bp + theme(axis.text.x = element_text(angle=0, hjust=0.5, vjust=.5),panel.border = element_rect(color = 'black', fill = NA))
