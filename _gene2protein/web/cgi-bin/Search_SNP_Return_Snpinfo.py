#!/share/pkg.7/python3/3.6.10/install/bin/python3
import sys
import os
#import pymysql
import sqlite3
import cgi
import cgitb
cgitb.enable()
form = cgi.FieldStorage()
#form = 'y'
if form:
        # Connect to the database.
        connection = sqlite3.connect("/restricted/projectnb/casa/_jychung/_gene2protein/db_g2p/gene2protein_v1.db")
        cursor = connection.cursor()
        #connection = pymysql.connect(host="ensembldb.ensembl.org", user="anonymous", db="homo_sapiens_variation_99_37",password="",port=3337)
        #cursor = connection.cursor()
        submit = form.getvalue("submit")
        #submit = 'y'
        if submit:
                snp = form.getvalue("SNP")
                #snp = 'rs1064795542'
                if snp:
                    #query2 = '''select variation.name,transcript_variation.allele_string,transcript_variation.somatic,seq_region_id, 
                    #            seq_region_start,seq_region_end,variation_feature.minor_allele_freq,transcript_variation.consequence_types,
                    #            variation_feature.clinical_significance
                    #            from variation join variation_feature using(variation_id)
                    #            join transcript_variation using(variation_feature_id)
                    #            where variation.name="%s";''' % snp
                    print("Content-type: text/html\n")
                    query1 = '''select distinct snp,chr,position,REF,ALT,variant_type,allele_type from Exon_SNP
                                where snp="%s"''' % snp
                    cursor.execute(query1)
                    result1 = cursor.fetchall()
                    if result1:
                        for r in result1:
                            print(r[0]+"\t"+r[1]+"\t"+str(r[2])+"\t"+r[3]+"\t"+r[4]+"\t"+r[5]+"\t"+r[6])
                           
                    else:
                        query1 = '''select distinct snp,chr,position,REF,ALT,variant_type,allele_type from Genome_SNP
                                    where snp="%s"''' % snp
                        cursor.execute(query1)
                        result1 = cursor.fetchall()
                        if result1:
                            for r in result1:
                                print(r[0]+"\t"+r[1]+"\t"+str(r[2])+"\t"+r[3]+"\t"+r[4]+"\t"+r[5]+"\t"+r[6])
                        else:
                            query1 = '''select distinct snp,chr,start_at,REF,ALT from VEP
                                        where snp="%s"''' % snp
                            cursor.execute(query1)
                            result1 = cursor.fetchall()
                            if result1:
                                for r in result1:
                                    print(r[0]+"\t"+r[1]+"\t"+str(r[2])+"\t"+r[3]+"\t"+r[4]+"\t"+"NA"+"\t"+"NA")
        
                        #x = list(x)
                        #query3 = '''select distinct name from seq_region
                        #            where seq_region_id=%d''' % x[3]
                        #cursor.execute(query3)
                        #x[3] = cursor.fetchall()[0][0]
                        #print(x)

        cursor.close()
        connection.close()

else:
        print("Content-type: text/html\n")
