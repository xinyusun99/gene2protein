#!/share/pkg.7/r/3.6.2/install/bin/R
library(ggplot2)
library(gggenes)
library(cowplot)
library(getopt)
library(RSQLite)

spec <- matrix(
    c("chr",  "c", 1, "character", "chromosome",
      "start_at", "s", 1, "integer",  "start at",
      "end_at", "e", 1, "integer", "end at",
      "random_string","r",1,"character","random string for file name"),
    byrow=TRUE, ncol=5)
opt <- getopt(spec=spec)

chr <- opt$chr
start_at <- opt$start_at
end_at <- opt$end_at
rs <- opt$random_string

#chr <- "17"
#start_at <- 7565000
#end_at <- 7900000  within 400000
#rs <- "jhjhjh"

create_table <- function(chr, start_at, end_at){
  con<-dbConnect(SQLite(),
                 "/restricted/projectnb/casa/_jychung/_gene2protein/db_g2p/gene2protein_v1.db")
  query1 <- sprintf('select distinct Gene.ENSG,Gene.symbol,ENSE,
                    Gene.start_at as G_start, Gene.end_at as G_end,
                    Exon.start_at as E_start, Exon.end_at as E_end,strand
                    from Exon join Gene using(ENSG)
                    where Gene.chromosome = "%s"
                    and Gene.end_at>%d
                    and Gene.start_at<%d
                    order by Gene.ENSG, Gene.start_at, Exon.start_at;',
                    chr,start_at,end_at)
  res<-dbSendQuery(con,query1)
  gene_table <- dbFetch(res)

  if (nrow(gene_table) != 0) {
    minp <- min(gene_table$G_start, start_at)
    maxp <- max(gene_table$G_end, end_at)
  } else {
    gene_table <- data.frame(ENSG=NA,symbol=NA,ENSE=NA,G_start=0,
                             G_end=0,E_start=0,E_end=0,strand="1")
    minp <- start_at
    maxp <- end_at
  }

  query2 <- sprintf('select chr,pos,recomb_rate from Recomb_rate
                    where chr="%s"
                    and pos>=%d
                    and pos<=%d
                    order by chr,pos;', chr, minp, maxp)
  res2 <- dbSendQuery(con,query2)
  Recomb_rate <- dbFetch(res2)
  query3 = sprintf('select chr,pos,trait,snp from GWAS_catalog
            where chr="%s"
            and pos>=%d
            and pos<=%d
            order by chr,pos;', chr, minp, maxp)
  res3 <- dbSendQuery(con,query3)
  GWAS_cat <- dbFetch(res3)
  dbDisconnect(con)
  return(list(gene_table,Recomb_rate,GWAS_cat,minp,maxp))
}

dtable <- create_table(chr, start_at, end_at)
gene_table <- dtable[[1]]
Recomb_rate <- dtable[[2]]
GWAS_cat <- dtable[[3]]
minp <- dtable[[4]]
maxp <- dtable[[5]]

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
#ggsave(sprintf("../htdocs/Range_Browser1_%s.png",rs),plot=Plot1)
ggsave(sprintf("../htdocs/Range_Browser1_%s.png",rs),plot=Plot1, width = 14, height = 9, dpi = 200)
