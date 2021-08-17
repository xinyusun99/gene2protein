#!/share/pkg.7/r/3.6.2/install/bin/R
library(ggplot2)
library(gggenes)
library(cowplot)
library(getopt)
library(RSQLite)

spec <- matrix(
  c("ENST",  "t", 2, "character", "ENST ID",
    "random_string","r",2,"character","random string for file name"),
  byrow=TRUE, ncol=5)
opt <- getopt(spec=spec)

ENST <- opt$ENST
rs <- opt$random_string

create_table <- function(isoform){
  con<-dbConnect(SQLite(),"/restricted/projectnb/casa/_jychung/_gene2protein/db_g2p/gene2protein_v1.db")
  query1 <- sprintf('select distinct Gene.ENSG,Gene.symbol,ENST,ENSE,
  Gene.start_at as G_start,Gene.end_at as G_end,Exon.start_at as E_start,
  Exon.end_at as E_end,strand
  from Exon join Gene using(ENSG)
  where Gene.ENSG = (select distinct ENSG from Isoform where ENST="%s")
  order by Gene.ENSG,ENST,Gene.start_at, Exon.start_at;',isoform)
  res<-dbSendQuery(con,query1)
  isoform_table <- dbFetch(res)
  query2 <- sprintf('select distinct Gene.ENSG,Gene.symbol,ENST,ENSE,
  Gene.start_at as G_start,Gene.end_at as G_end,Exon.start_at as E_start,
  Exon.end_at as E_end,strand
  from Exon join Gene using(ENSG)
  where ENST="%s"
  order by Gene.ENSG,ENST,Gene.start_at, Exon.start_at;',isoform)
  res2<-dbSendQuery(con,query2)
  iso_table <- dbFetch(res2)
  minp <- iso_table$G_start[1]
  maxp <- iso_table$G_end[1]
  gene <- iso_table$symbol[1]
  query3 <- sprintf('select chr,pos,recomb_rate from Recomb_rate
                    where chr = (select distinct Gene.chromosome from Gene
                    where symbol="%s")
                    and pos>%d
                    and pos<%d
                    order by chr,pos;',gene,minp,maxp)
  res3 <- dbSendQuery(con,query3)
  Recomb_rate <- dbFetch(res3)
  query4 = sprintf('select chr,pos,trait,snp from GWAS_catalog
            where chr = (select distinct Gene.chromosome
            from Gene where symbol="%s")
            and pos>%d
            and pos<%d
            order by chr,pos;',gene,minp,maxp)
  res4 <- dbSendQuery(con,query4)
  GWAS_cat <- dbFetch(res4)
  dbDisconnect(con)
  return(list(isoform_table,iso_table,Recomb_rate,GWAS_cat))
}

if(length(ENST)!=0){
  ENST <- toupper(ENST)
  dtable <- create_table(ENST)
  isoform_table <- dtable[[1]]
  iso_table <- dtable[[2]]
  Recomb_rate <- dtable[[3]]
  GWAS_cat <- dtable[[4]]
}

if(nrow(GWAS_cat)==0){
  GWAS_cat <- data.frame(pos=0,trait=NA,snp=NA)
}

if(nrow(Recomb_rate)==0){
  Recomb_rate <- data.frame(pos=0,recomb_rate=0)
}
isoform_table$strand <- as.numeric(isoform_table$strand)
rename <- function(x){
  if(x==1){
    s <- "(+)"
    return(s)
  }else if(x==-1){
    s <- "(-)"
    return(s)
  }
}
sname <- sapply(isoform_table$strand,rename)
sname <- paste0(isoform_table$symbol,sname)
isoform_table$symbol2 <- sname
gene_structure.plot <- ggplot(isoform_table, aes(xmin = G_start, xmax = G_end, y = symbol2,
                                                 fill = "Introns")) +
  xlab("Position") +
  ylab("Gene") +
  theme(plot.title = element_text(hjust = 0.5)) +
  xlim(min(isoform_table$G_start),max(isoform_table$G_end))+
  geom_gene_arrow(arrowhead_width = unit(0, "mm"),
                  arrow_body_height = grid::unit(5, "mm")) +
  theme_genes() +
  geom_subgene_arrow(
    data = isoform_table,
    aes(xsubmin = E_start, xsubmax = E_end,fill="Exons"),
    arrowhead_width = unit(0, "mm"),
    arrow_body_height = grid::unit(5, "mm")
  ) +
  theme(legend.title = element_blank())+
  annotate("segment", x=isoform_table$G_start, xend=isoform_table$G_end,y=0,yend =0,colour="black")
  #annotate(geom = "text", x=GWAS_cat$pos,y=0.5,colour="black",label=GWAS_cat$snp,angle=-90,size=3.5)
#gene_structure.plot

GWAS_anno2 <- ggplot()+xlim(min(isoform_table$G_start),max(isoform_table$G_end))+
  xlab("Position")+
  ylab("GWAS catalog")+
  annotate(geom = "text", x=GWAS_cat$pos,y=0,colour="black",label=GWAS_cat$snp,angle=-90,size=3.2)+
  theme(panel.border = element_blank(), panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(), axis.line = element_blank(),
        axis.text.y = element_blank(),axis.ticks.y = element_blank())

##isoform plot for gene
isoform.plot <- ggplot(iso_table, aes(xmin = E_start, xmax = E_end, y = ENST,
                                    fill = "Exons")) +
  xlab("Position") +
  ylab("Isoform") +
  xlim(min(iso_table$G_start),max(iso_table$G_end))+
  geom_gene_arrow(arrowhead_width = unit(0, "mm"),
                  arrow_body_height = grid::unit(5, "mm")) +
  theme_genes()+
  theme(legend.title = element_blank())
#isoform.plot

##recombnation plot
recomb_plot <- ggplot()+geom_line(data = Recomb_rate,aes(x=pos,y=recomb_rate),
                                  color="navy")+ theme_bw() +
  xlim(min(isoform_table$G_start),max(isoform_table$G_end))+
  xlab("Position")+
  ylab("Recombination rate")+
  theme(panel.border = element_blank(), panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"))
#recomb_plot
myPlot <- plot_grid(gene_structure.plot, GWAS_anno2, isoform.plot, recomb_plot,
                    ncol = 1, align = "v",
                    axis="lr",rel_heights=c(5,2,2,2))
#myPlot
ggsave(sprintf("../htdocs/Isoform_Browser1_%s.png",rs), plot=myPlot, width = 14, height = 9, dpi = 200)
