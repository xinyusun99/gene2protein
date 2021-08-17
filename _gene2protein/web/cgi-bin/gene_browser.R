#!/share/pkg.7/r/3.6.2/install/bin/R
library(ggplot2)
library(gggenes)
library(cowplot)
library(getopt)
library(RSQLite)

spec <- matrix(
  c("symbol",  "s", 1, "character", "Gene symbol",
    "ENSG", "e", 1, "character",  "ENSG ID",
    "random_string","r",2,"character","random string for file name"),
  byrow=TRUE, ncol=5)
opt <- getopt(spec=spec)

symbol <- opt$symbol
ENSG <- opt$ENSG
rs <- opt$random_string

#symbol <- 'TP53'
create_table <- function(gene){
  con<-dbConnect(SQLite(),"/restricted/projectnb/casa/_jychung/_gene2protein/db_g2p/gene2protein_v1.db")
  query1 <- sprintf('select distinct Gene.ENSG,Gene.symbol,ENST,ENSE,
  Gene.start_at as G_start,Gene.end_at as G_end,
  Exon.start_at as E_start,Exon.end_at as E_end,strand
  from Exon join Gene using(ENSG)
  where Gene.chromosome = (select distinct chromosome from Gene
  where symbol="%s")
  and Gene.end_at>=(select distinct start_at-25000 from Gene where symbol="%s")
  and Gene.start_at<=(select distinct end_at+25000 from Gene where symbol="%s")
  order by Gene.ENSG, Gene.start_at, Exon.start_at;',gene,gene,gene)
  res<-dbSendQuery(con,query1)
  gene_table <- dbFetch(res)

  query1p5 <- sprintf('select chr,pos,trait,snp from GWAS_catalog
            where chr=(select distinct Gene.chromosome from Gene
                       where symbol="%s")
            and pos>=(select distinct start_at-25000 from Gene where symbol="%s")
            and pos<=(select distinct end_at+25000 from Gene where symbol="%s")
            order by chr,pos;',gene,gene,gene)
  res1p5 <- dbSendQuery(con,query1p5)
  GWAS_temp <- dbFetch(res1p5)
  if (nrow(GWAS_temp)!=0) {
    minp <- min(gene_table$G_start,GWAS_temp$pos)
    maxp <- max(gene_table$G_end,GWAS_temp$pos)
  } else {
    minp <- min(gene_table$G_start)
    maxp <- max(gene_table$G_end)
  }

  query2 <- sprintf('select chr,pos,recomb_rate from Recomb_rate
                    where chr = (select distinct Gene.chromosome from Gene
                    where symbol="%s")
                    and pos>=%d
                    and pos<=%d
                    order by chr,pos;',gene,minp,maxp)
  res2 <- dbSendQuery(con,query2)
  Recomb_rate <- dbFetch(res2)
  query3 = sprintf('select chr,pos,trait,snp from GWAS_catalog
            where chr = (select distinct Gene.chromosome from Gene
            where symbol="%s")
            and pos>=%d
            and pos<=%d
            order by chr,pos;',gene,minp,maxp)
  res3 <- dbSendQuery(con,query3)
  GWAS_cat <- dbFetch(res3)
  dbDisconnect(con)
  return(list(gene_table,Recomb_rate,GWAS_cat,minp,maxp))
}

if(length(symbol)!=0){
  symbol <- toupper(symbol)
  dtable <- create_table(symbol)
  gene_table <- dtable[[1]]
  Recomb_rate <- dtable[[2]]
  GWAS_cat <- dtable[[3]]
  minp <- dtable[[4]]
  maxp <- dtable[[5]]
} else if (!is.null(ENSG)){
  ENSG <- toupper(ENSG)
  con<-dbConnect(SQLite(),"/restricted/projectnb/casa/_jychung/_gene2protein/db_g2p/gene2protein_v1.db")
  query <- sprintf('select distinct symbol from Gene
                    where ENSG = "%s";',ENSG)
  res <- dbSendQuery(con,query)
  symbol <- dbFetch(res)[1,1]
  dbDisconnect(con)
  symbol <- toupper(symbol)
  dtable <- create_table(symbol)
  gene_table <- dtable[[1]]
  Recomb_rate <- dtable[[2]]
  GWAS_cat <- dtable[[3]]
  minp <- dtable[[4]]
  maxp <- dtable[[5]]
}

if(nrow(GWAS_cat)==0){
  GWAS_cat <- data.frame(pos=0,trait=NA,snp=NA)
}

if(nrow(Recomb_rate)==0){
  Recomb_rate <- data.frame(pos=0,recomb_rate=0)
}

gene_table$strand <- as.numeric(gene_table$strand)
rename <- function(x){
  if(x==1){
    s <- "(+)"
    return(s)
  }else if(x==-1){
    s <- "(-)"
    return(s)
  }
}
sname <- sapply(gene_table$strand,rename)
sname <- paste0(gene_table$symbol,sname)
gene_table$symbol2 <- sname
gene_structure.plot <- ggplot(gene_table, aes(xmin = G_start, xmax = G_end, y = symbol2,
                                              fill = "Introns")) +
  xlab("Position") +
  ylab("Gene") +
  xlim(minp,maxp)+
  #xlim(min(gene_table$G_start),max(gene_table$G_end))+
  geom_gene_arrow(arrowhead_width = unit(0, "mm"),
                  arrow_body_height = grid::unit(5, "mm")) +
  theme_genes() +
  geom_subgene_arrow(
    data = gene_table,
    aes(xsubmin = E_start, xsubmax = E_end,fill="Exons"),
    arrowhead_width = unit(0, "mm"),
    arrow_body_height = grid::unit(5, "mm")
  ) +
  theme(legend.title = element_blank())
  #annotate("segment", x=gene_table$G_start, xend=gene_table$G_end,y=-0.7,yend =-0.7,colour="white")
  #annotate(geom = "text", x=GWAS_cat$pos,y=0,colour="black",label=GWAS_cat$snp,angle=-90,size=3.2)
#gene_structure.plot

GWAS_anno <- ggplot()+xlim(minp,maxp)+
  xlab("Position")+
  ylab("GWAS catalog")+
  annotate(geom = "text", x=GWAS_cat$pos,y=0,colour="black",label=GWAS_cat$snp,angle=-90,size=3.2) +
  theme(panel.border = element_blank(), panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(), axis.line = element_blank(),
        axis.text.y = element_blank(),axis.ticks.y = element_blank())

recomb_plot <- ggplot()+xlim(minp,maxp)+
  geom_line(data = Recomb_rate,aes(x=pos,y=recomb_rate),color="navy")+
  theme_bw() +
  xlab("Position")+
  ylab("Recombination rate")+
  theme(panel.border = element_blank(), panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"))
#recomb_plot
Plot1 <- plot_grid(gene_structure.plot, GWAS_anno, recomb_plot, ncol = 1, align = "v",
                    axis="lr",rel_heights=c(4,1,1))

#Plot1
ggsave(sprintf("../htdocs/Gene_Browser1_%s.png",rs),plot=Plot1, width = 14, height = 9, dpi = 200)

isoform_table <- gene_table[gene_table$symbol==symbol,]
gene_structure.plot2 <- ggplot(isoform_table, aes(xmin = G_start, xmax = G_end, y = symbol2,
                                                 fill = "Introns")) +
  xlab("Position") +
  ylab("Gene") +
  xlim(min(isoform_table$G_start),max(isoform_table$G_end))+
  geom_gene_arrow(arrowhead_width = unit(0, "mm"),
                  arrow_body_height = grid::unit(5, "mm")) +
  theme_genes() +
  theme(legend.title = element_blank())+
  geom_subgene_arrow(
    data = isoform_table,
    aes(xsubmin = E_start, xsubmax = E_end,fill="Exons"),
    arrowhead_width = unit(0, "mm"),
    arrow_body_height = grid::unit(5, "mm")) +
  theme(plot.title = element_text(hjust = 0.5)) +
  annotate("segment", x=isoform_table$G_start, xend=isoform_table$G_end,y=0,yend=0,colour="black")
  #annotate(geom = "text", x=GWAS_cat$pos,y=0.5,colour="black",label=GWAS_cat$snp,angle=-90,size=3.5)
#gene_structure.plot

GWAS_anno2 <- ggplot()+xlim(min(isoform_table$G_start),max(isoform_table$G_end))+
  xlab("Position")+
  ylab("GWAS catalog")+
  annotate(geom = "text", x=GWAS_cat$pos,y=0,colour="black",label=GWAS_cat$snp,angle=-90,size=3.2) +
  theme(panel.border = element_blank(), panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(), axis.line = element_blank(),
        axis.text.y = element_blank(),axis.ticks.y = element_blank())

##isoform plot for gene
isoform.plot <- ggplot(isoform_table, aes(xmin = E_start, xmax = E_end, y = ENST,
                                          fill = "Exons")) +
  xlab("Position") +
  ylab("Isoform") +
  xlim(min(isoform_table$G_start),max(isoform_table$G_end))+
  geom_gene_arrow(arrowhead_width = unit(0, "mm"),
                  arrow_body_height = grid::unit(5, "mm")) +
  theme_genes() +
  theme(legend.title = element_blank())
#isoform.plot

Plot2 <- plot_grid(gene_structure.plot2, GWAS_anno2, isoform.plot,
                    ncol = 1, align = "v",
                    axis="lr",rel_heights=c(5,2,5))
#Plot2
ggsave(sprintf("../htdocs/Gene_Browser2_%s.png",rs), plot=Plot2, width=14, height=10, dpi=200)

