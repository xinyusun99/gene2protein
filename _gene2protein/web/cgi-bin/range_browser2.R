.libPaths( c( .libPaths(), "/home/students_20/xinyusun/R/x86_64-redhat-linux-gnu-library/3.6") )
library(gggenes,lib.loc = "/home/students_20/xinyusun/R/x86_64-redhat-linux-gnu-library/3.6",quietly = T)
library(cowplot)
library("ggplot2",lib.loc = "/home/students_20/xinyusun/R/x86_64-redhat-linux-gnu-library/3.6",quietly = T)

#install.packages("cowplot")
coordinate <- read.csv("genome_browser/range_RangePart.csv",header = F)
try(gene_table <- read.csv("genome_browser/gene_table_RangePart.csv",header = F),silent = TRUE)
try(Recomb_rate <- read.csv("genome_browser/Recomb_rate_RangePart.csv",header = F),silent = TRUE)
try(GWAS_cat <- read.csv("genome_browser/GWAS_catalog_RangePart.csv",header = F),silent = TRUE)

if(!exists('gene_table')){
  gene_table <- data.frame(V1=NA,V2=NA,V3=NA,V4=0,V5=0,V6=0,V7=0)
  start_at <- coordinate$V1
  end_at <- coordinate$V2
}else{
  start_at <- min(coordinate$V1,min(gene_table$V4))
  end_at <- max(coordinate$V2,max(gene_table$V5))
}

if(!exists('GWAS_cat')){
  GWAS_cat <- data.frame(V2=0,V3=NA,V4=NA)
}

if(!exists('Recomb_rate')){
  Recomb_rate <- data.frame(V2=0,V3=0)
}

gene_structure.plot <- ggplot(gene_table, aes(xmin = V4, xmax = V5, y = V2,
                                              fill = "Introns")) +
  xlab("Position") +
  ylab("Gene") +
  xlim(start_at,end_at)+
  geom_gene_arrow(arrowhead_width = unit(0, "mm"),
                  arrow_body_height = grid::unit(5, "mm")) +
  theme_genes() +
  geom_subgene_arrow(
    data = gene_table,
    aes(xsubmin = V6, xsubmax = V7,fill="Exons"),
    arrowhead_width = unit(0, "mm"),
    arrow_body_height = grid::unit(5, "mm")
  ) +
  theme(legend.title = element_blank())+
  annotate("segment", x=gene_table$V4, xend=gene_table$V5,y=-0.7,yend =-0.7,colour="white") +
  annotate(geom = "text", x=GWAS_cat$V2,y=0,colour="black",label=GWAS_cat$V4,angle=-90,size=3.2)
#gene_structure.plot

recomb_plot <- ggplot()+xlim(start_at,end_at)+
  geom_line(data = Recomb_rate,aes(x=V2,y=V3),color="navy")+
  theme_bw() +
  xlab("Position")+
  ylab("Recombination rate")+
  theme(panel.border = element_blank(), panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"))
#recomb_plot
myPlot <- plot_grid(gene_structure.plot,recomb_plot, ncol = 1, align = "v",
                    axis="lr",rel_heights=c(4,1))

#myPlot
ggsave('/var/www/html/images/students_20/xinyusun/RangePart.png', plot=myPlot, width = 14, height = 9, dpi = 200)
#ggsave("images/image1.png",plot=myPlot, width = 14, height = 9, dpi = 200)

