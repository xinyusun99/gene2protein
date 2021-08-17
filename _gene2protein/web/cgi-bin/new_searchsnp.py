#!/share/pkg.7/python3/3.6.10/install/bin/python3
import sys
import os
import sqlite3
import cgi
import cgitb
cgitb.enable()

form = cgi.FieldStorage()
#form = "y"
if form:
        # Connect to the database.
        connection = sqlite3.connect("/restricted/projectnb/casa/_jychung/_gene2protein/db_g2p/gene2protein_v1.db") 
        cursor = connection.cursor()
        submit = form.getvalue("submit")
        #submit = "y"
        if submit:
                symbol = form.getvalue("symbol")
                ENSG = form.getvalue("ENSG")
                #symbol = 'TP53'
                #ENSG = None
                if symbol and ENSG:
                        query = """select distinct * from Exon_SNP
                                    where chr=(select chromosome from Gene where ENSG="%s" and symbol="%s")
                                    and position>(select start_at from Gene where ENSG="%s" and symbol="%s")
                                    and position<(select end_at from Gene where ENSG="%s" and symbol="%s"); """%(ENSG,symbol,ENSG,symbol,ENSG,symbol)
                        cursor.execute(query)
                        rows=cursor.fetchall()
                        print("Content-type: text/html\n")
                        for row in rows:
                                print(row[1]+"\t"+row[2]+"\t"+str(row[3])+"\t"+row[4]+"\t"+row[5]+"\t"+row[6]+"\t"+row[7])

                elif symbol:
                        symbol = symbol.upper()
                        query = """select distinct * from Exon_SNP
                                    where chr=(select chromosome from Gene where symbol="%s")
                                    and position>(select start_at from Gene where symbol="%s")
                                    and position<(select end_at from Gene where symbol="%s"); """%(symbol,symbol,symbol)
                        cursor.execute(query)
                        rows=cursor.fetchall()
                        print("Content-type: text/html\n")
                        for row in rows:
                                print(row[1]+"\t"+row[2]+"\t"+str(row[3])+"\t"+row[4]+"\t"+row[5]+"\t"+row[6]+"\t"+row[7])
                elif ENSG:
                        ENSG = ENSG.upper()
                        query = """select distinct * from Exon_SNP
                                    where chr=(select chromosome from Gene where ENSG="%s")
                                    and position>(select start_at from Gene where ENSG="%s")
                                    and position<(select end_at from Gene where ENSG="%s"); """%(ENSG,ENSG,ENSG)

                        cursor.execute(query)
                        rows=cursor.fetchall()
                        print("Content-type: text/html\n")
                        for row in rows:
                                print(row[1]+"\t"+row[2]+"\t"+str(row[3])+"\t"+row[4]+"\t"+row[5]+"\t"+row[6]+"\t"+row[7])

        cursor.close()
        connection.close()
else:
        print("Content-type: text/html\n")

'''
import pymysql
gene = "TP53"
conn = sqlite3.connect("/restricted/projectnb/casa/_jychung/_gene2protein/db_g2p/gene2protein_v1.db")
c = conn.cursor()
query0 = """select distinct chromosome,start_at,end_at from Gene
            where symbol = '%s' """ % gene
c.execute(query0)
result0 = c.fetchall()[0]
chromosome = result0[0]
start = int(result0[1])
end = int(result0[2])
connection = pymysql.connect(host="ensembldb.ensembl.org", user="anonymous", db="homo_sapiens_variation_99_37",password="",port=3337)
cursor = connection.cursor()
query1 = """select distinct seq_region_id from seq_region
            where name='%s' """ % chromosome
cursor.execute(query1)
result1 = cursor.fetchall()[0]
region_id = result1[0]
query2 = """select variation.name,transcript_variation.allele_string,transcript_variation.somatic,seq_region_id,
            seq_region_start,seq_region_end,variation_feature.minor_allele_freq,transcript_variation.consequence_types,
            variation_feature.clinical_significance
            from variation join variation_feature using(variation_id)
            join transcript_variation using(variation_feature_id)
            where seq_region_id=%d and seq_region_start<=%d and seq_region_end>=%d;""" % (region_id, end, start)
cursor.execute(query2)
rows = cursor.fetchall()
for x in rows:
    x = list(x)
    x[3] = chromosome.copy()
    print(x)
print(row)
c.close()
conn.close()
cursor.close()
connection.close()
'''
