#!/share/pkg.7/python3/3.6.10/install/bin/python3
import sys
import os
#import pymysql
#import MySQLdb
#import mysql.connector
import sqlite3
import cgi
import cgitb
cgitb.enable()
form = cgi.FieldStorage()
#form = 'y'
if form:
        # Connect to the database.
        conn = sqlite3.connect("/restricted/projectnb/casa/_jychung/_gene2protein/db_g2p/gene2protein_v1.db")
        c = conn.cursor()
        #connection = pymysql.connect(host="ensembldb.ensembl.org", user="anonymous", db="homo_sapiens_variation_99_37",password="",port=3337)
        #cursor = connection.cursor()
        submit = form.getvalue("submit")
        #submit = 'y'
        if submit:
                snp = form.getvalue("SNP")
                #snp = 'rs1641549'
                if snp:
                        #query0 = '''select distinct seq_region_id,seq_region_start,seq_region_end
                        #           from variation join variation_feature using(variation_id)
                        #           where variation.name="%s";''' % snp
                        
                        #cursor.execute(query0)
                        #row = cursor.fetchall()[0]
                        #query1 = '''select distinct name from seq_region
                        #            where seq_region_id=%d''' % row[0]
                        #cursor.execute(query1)
                        #chromosome = cursor.fetchall()[0][0]
                        #start = row[1]
                        #end = row[2]

                        query1 = '''select distinct chr,position from Exon_SNP
                                    where snp="%s"''' % snp
                        c.execute(query1)
                        result1 = c.fetchall()
                        if result1:
                            chromosome = result1[0][0]
                            pos = result1[0][1]
                            #print(chromosome,pos)
                        else:
                            query1 = '''select distinct chr,position from Genome_SNP
                                        where snp="%s"''' % snp
                            c.execute(query1)
                            result1 = c.fetchall()
                            if result1:
                                chromosome = result1[0][0]
                                pos = result1[0][1]
                            else:
                                query1 = '''select distinct chr,start_at from VEP
                                            where snp="%s"''' % snp
                                c.execute(query1)
                                result1 = c.fetchall()[0]
                                chromosome = result1[0]
                                pos = result1[1]
                            #print(chromosome,pos)
                        query2 = """SELECT distinct ENSG, symbol, chromosome, start_at, end_at, description,gene_type
                                    FROM Gene
                                    WHERE chromosome="%s" and end_at>=%d and start_at<=%d;""" % (chromosome, pos, pos)
                        c.execute(query2)
                        rows=c.fetchall()
                        print("Content-type: text/html\n")
                        for r in rows:
                                temp = []
                                for x in r:
                                        temp.append(str(x))
                                line = "\t".join(temp)
                                print(line)
        #cursor.close()
        #connection.close()
        c.close()
        conn.close()
else:
       print("Content-type: text/html\n")
