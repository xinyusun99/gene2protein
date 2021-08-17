#!/share/pkg.7/r/3.6.2/install/bin/R
#warnings('off')
library(ggplot2)
library(gggenes)
library(cowplot)
library(getopt)
library(RSQLite)
library(grid)

spec <- matrix(
  c("snp", "s", 1, "character", "SNPID",
    "random_string","r",2,"character","random string for file name"),
  byrow=TRUE, ncol=5)
opt <- getopt(spec=spec)

snp <- opt$snp
rs <- opt$random_string
#variant <- "rs1000000342"
#snp <- "rs699"
create_table <- function(variant) {
  con<-dbConnect(SQLite(),"/restricted/projectnb/casa/_jychung/_gene2protein/db_g2p/gene2protein_v1.db")
  query0 <- sprintf('select distinct snp,chr,position from Exon_SNP
                    where snp="%s";',variant)
  res0<-dbSendQuery(con,query0)
  snp_table <- dbFetch(res0)
  if (nrow(snp_table)!=0) {
    chromosome <- snp_table$chr
    query1 <- sprintf('select distinct Gene.ENSG,Gene.symbol,ENST,ENSE,
    Gene.start_at as G_start,Gene.end_at as G_end,Exon.start_at as E_start,
    Exon.end_at as E_end,strand
    from Exon join Gene using(ENSG)
    where Gene.chromosome = (select distinct chr from Exon_SNP where snp="%s")
    and Gene.end_at>(select distinct position-25000 from Exon_SNP where snp="%s")
    and Gene.start_at<(select distinct position+25000 from Exon_SNP where snp="%s")
    order by Gene.ENSG, Gene.start_at, Exon.start_at;',variant,variant,variant)
    res1<-dbSendQuery(con,query1)
    gene_table <- dbFetch(res1)
    minp <- min(gene_table$G_start)
    maxp <- max(gene_table$G_end)
    query2 <- sprintf('select chr,pos,recomb_rate from Recomb_rate
                    where chr = "%s"
                    and pos>%d
                    and pos<%d
                    order by chr,pos;',chromosome,minp,maxp)
    res2 <- dbSendQuery(con,query2)
    Recomb_rate <- dbFetch(res2)
    query3 = sprintf('select chr,pos,trait,snp from GWAS_catalog
              where chr ="%s"
              and pos>%d
              and pos<%d
              order by chr,pos;',chromosome,minp,maxp)
    res3 <- dbSendQuery(con,query3)
    GWAS_cat <- dbFetch(res3)
    dbDisconnect(con)
    return(list(snp_table,gene_table,Recomb_rate,GWAS_cat))
    } else {
    query0 <- sprintf('select distinct snp,chr,position from Genome_SNP
                    where snp="%s";',variant)
    res0<-dbSendQuery(con,query0)
    snp_table <- dbFetch(res0)
    if (nrow(snp_table)!=0) {
      chromosome <- snp_table$chr
      query1 <- sprintf('select distinct Gene.ENSG,Gene.symbol,ENST,ENSE,
      Gene.start_at as G_start,Gene.end_at as G_end,Exon.start_at as E_start,
      Exon.end_at as E_end,strand
      from Exon join Gene using(ENSG)
      where Gene.chromosome = (select distinct chr from Genome_SNP where snp="%s")
      and Gene.end_at>(select distinct position-25000 from Genome_SNP where snp="%s")
      and Gene.start_at<(select distinct position+25000 from Genome_SNP where snp="%s")
      order by Gene.ENSG, Gene.start_at, Exon.start_at;',variant,variant,variant)
      res1<-dbSendQuery(con,query1)
      gene_table <- dbFetch(res1)
      minp <- min(gene_table$G_start)
      maxp <- max(gene_table$G_end)
      query2 <- sprintf('select chr,pos,recomb_rate from Recomb_rate
                      where chr = "%s"
                      and pos>%d
                      and pos<%d
                      order by chr,pos;',chromosome,minp,maxp)
      res2 <- dbSendQuery(con,query2)
      Recomb_rate <- dbFetch(res2)
      query3 = sprintf('select chr,pos,trait,snp from GWAS_catalog
                where chr ="%s"
                and pos>%d
                and pos<%d
                order by chr,pos;',chromosome,minp,maxp)
      res3 <- dbSendQuery(con,query3)
      GWAS_cat <- dbFetch(res3)
      dbDisconnect(con)
      return(list(snp_table,gene_table,Recomb_rate,GWAS_cat))
    } else {
      query0 <- sprintf('select distinct snp,chr,start_at as position from VEP
                    where snp="%s";',variant)
      res0<-dbSendQuery(con,query0)
      snp_table <- dbFetch(res0)
      if (nrow(snp_table)!=0) {
        chromosome <- snp_table$chr
        query1 <- sprintf('select distinct Gene.ENSG,Gene.symbol,ENST,ENSE,
      Gene.start_at as G_start,Gene.end_at as G_end,Exon.start_at as E_start,
      Exon.end_at as E_end,strand
      from Exon join Gene using(ENSG)
      where Gene.chromosome = (select distinct chr from VEP where snp="%s")
      and Gene.end_at>(select distinct start_at-25000 from VEP where snp="%s")
      and Gene.start_at<(select distinct end_at+25000 from VEP where snp="%s")
      order by Gene.ENSG, Gene.start_at, Exon.start_at;',variant,variant,variant)
        res1<-dbSendQuery(con,query1)
        gene_table <- dbFetch(res1)
        minp <- min(gene_table$G_start)
        maxp <- max(gene_table$G_end)
        query2 <- sprintf('select chr,pos,recomb_rate from Recomb_rate
                      where chr = "%s"
                      and pos>%d
                      and pos<%d
                      order by chr,pos;',chromosome,minp,maxp)
        res2 <- dbSendQuery(con,query2)
        Recomb_rate <- dbFetch(res2)
        query3 = sprintf('select chr,pos,trait,snp from GWAS_catalog
                where chr ="%s"
                and pos>%d
                and pos<%d
                order by chr,pos;',chromosome,minp,maxp)
        res3 <- dbSendQuery(con,query3)
        GWAS_cat <- dbFetch(res3)
        dbDisconnect(con)
        return(list(snp_table,gene_table,Recomb_rate,GWAS_cat))
      }
    }
  }
}

if(!is.null(snp)){
  dtable <- create_table(snp)
  snp_table <- dtable[[1]]
  gene_table <- dtable[[2]]
  Recomb_rate <- dtable[[3]]
  GWAS_cat <- dtable[[4]]
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

#text_GWAS <- textGrob("GWAS catalog", gp = gpar(fontsize=13))

sname <- sapply(gene_table$strand,rename)
sname <- paste0(gene_table$symbol,sname)
gene_table$symbol2 <- sname
gene_structure.plot <- ggplot(gene_table, aes(xmin = G_start, xmax = G_end, y = symbol2,
                                              fill = "Introns")) +
  labs(title=paste0("SNP:",snp_table$snp[1])) +
  theme(plot.title = element_text(hjust = 0.5)) +
  xlab("Position") +
  ylab("Gene") +
  xlim(min(gene_table$G_start),max(gene_table$G_end))+
  #scale_x_continuous()+
  geom_gene_arrow(arrowhead_width = unit(0, "mm"),
                  arrow_body_height = grid::unit(5, "mm")) +
  theme_genes() +
  theme(legend.title = element_blank()) +
  geom_subgene_arrow(
    data = gene_table,
    aes(xsubmin = E_start, xsubmax = E_end,fill="Exons"),
    arrowhead_width = unit(0, "mm"),
    arrow_body_height = grid::unit(5, "mm")
  ) +
  annotate("segment", x=snp_table$position, xend=snp_table$position,y=0,yend =length(unique(gene_table$symbol))+0.2,colour="red")
  #annotate("segment", x=isoform_table$V5, xend=isoform_table$V6,y=0,yend=0,colour="black")+
  #annotate(geom = "text", x=GWAS_cat$pos,y=0,colour="black",label=GWAS_cat$snp,angle=-90,size=3.2)
  #annotation_custom(text_GWAS, xmin=min(gene_table$G_start)-5000, xmax=min(gene_table$G_start)-5000, ymin=0, ymax=0)

GWAS_anno <- ggplot()+xlim(min(gene_table$G_start),max(gene_table$G_end))+
  xlab("Position")+
  ylab("GWAS catalog")+
  annotate(geom = "text", x=GWAS_cat$pos,y=0,colour="black",label=GWAS_cat$snp,angle=-90,size=3.2) +
  theme(panel.border = element_blank(), panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(), axis.line = element_blank(),
        axis.text.y = element_blank(),axis.ticks.y = element_blank())

#gene_structure.plot
recomb_plot <- ggplot()+geom_line(data = Recomb_rate,aes(x=pos,y=recomb_rate),color="navy") +
  theme_bw() +
  xlim(min(gene_table$G_start),max(gene_table$G_end))+
  xlab("Position")+
  ylab("Recombination rate")+
  theme(panel.border = element_blank(), panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"))
#recomb_plot
Plot1 <- plot_grid(gene_structure.plot,GWAS_anno,recomb_plot, ncol = 1, align = "v",
                    axis="lr",rel_heights=c(4,1,1))

#Plot1
ggsave(sprintf("../htdocs/SNP_Browser1_%s.png",rs), plot=Plot1, width = 14, height = 9, dpi = 200)

###Isoform plot
snp.position <- unique(snp_table$position)
isoform_table <- gene_table[gene_table$G_start<=snp.position&gene_table$G_end>=snp.position,]
maxp <- max(isoform_table$G_end)
minp <- min(isoform_table$G_start)
GWAS_cat2 <- GWAS_cat[GWAS_cat$pos<=maxp&GWAS_cat$pos>=minp,]

if(nrow(GWAS_cat2)==0){
  GWAS_cat2 <- data.frame(pos=0,trait=NA,snp=NA)
}

gene_structure.plot <- ggplot(isoform_table, aes(xmin = G_start, xmax = G_end, y = symbol2,
                                                 fill = "Introns")) +
  labs(title=paste0("SNP:",snp_table$snp[1])) +
  theme(plot.title = element_text(hjust = 0.5)) +
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
  annotate("segment", x=snp_table$position, xend=snp_table$position,y=0,yend =length(unique(isoform_table$symbol))+0.1,colour="red")
  #annotate(geom = "text", x=GWAS_cat2$pos,y=0,colour="black",label=GWAS_cat2$snp,angle=-90,size=3.2)

#gene_structure.plot

GWAS_anno2 <- ggplot()+xlim(min(isoform_table$G_start),max(isoform_table$G_end))+
  xlab("Position")+
  ylab("GWAS catalog")+
  annotate(geom = "text", x=GWAS_cat2$pos,y=0,colour="black",label=GWAS_cat2$snp,angle=-90,size=3.2) +
  theme(panel.border = element_blank(), panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(), axis.line = element_blank(),
        axis.text.y = element_blank(),axis.ticks.y = element_blank())

##isoform plot for gene
isoform.plot <- ggplot(isoform_table, aes(xmin = E_start, xmax = E_end, y = ENST,
                                          fill = symbol)) +
  scale_fill_manual(values=c("#FFA500","#FF4500","#6495ED")) +
  xlab("Position") +
  ylab("Isoform") +
  xlim(min(isoform_table$G_start),max(isoform_table$G_end))+
  geom_gene_arrow(arrowhead_width = unit(0, "mm"),
                  arrow_body_height = grid::unit(5, "mm")) +
  annotate("segment", x=snp_table$position, xend=snp_table$position,y=0.4,
           yend =length(unique(isoform_table$ENST))+0.2,colour="red") +
  theme_genes()+
  theme(legend.title = element_blank())
#isoform.plot

Plot2 <- plot_grid(gene_structure.plot, GWAS_anno2, isoform.plot,
                    ncol = 1, align = "v",
                    axis="lr",rel_heights=c(5,2,5))
Plot2
ggsave(sprintf("../htdocs/SNP_Browser2_%s.png",rs), plot=Plot2, width = 14, height = 10, dpi = 200)
#ggsave("images/image5.png",plot=myPlot, width = 14, height = 12, dpi = 200)
