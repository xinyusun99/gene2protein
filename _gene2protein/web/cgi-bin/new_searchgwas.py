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
        submit = form.getvalue("submit")
        #submit = 'y'
        if submit:
                symbol = form.getvalue("symbol")
                ENSG = form.getvalue("ENSG")
                #symbol = 'TP53'
                #ENSG = None
                if symbol and ENSG:
                        symbol = symbol.upper()
                        ENSG = ENSG.upper()
                        query = """select chr,pos,trait,snp from GWAS_catalog
                                   where chr = (select distinct Gene.chromosome from Gene where symbol="%s" and ENSG="%s")
                                   and pos>(select distinct Gene.start_at-25000 from Gene where symbol="%s" and ENSG="%s")
                                   and pos<(select distinct Gene.end_at+25000 from Gene where symbol="%s" and ENSG="%s")
                                   order by chr,pos;"""%(symbol,ENSG,symbol,ENSG,symbol,ENSG)
                        cursor.execute(query)
                        rows=cursor.fetchall()
                        print("Content-type: text/html\n")
                        for row in rows:
                                print(row[0]+"\t"+str(row[1])+"\t"+row[2]+"\t"+row[3])


                elif symbol:
                        symbol = symbol.upper()
                        query = """select chr,pos,trait,snp from GWAS_catalog
                                   where chr = (select distinct Gene.chromosome from Gene where symbol="%s")
                                   and pos>(select distinct Gene.start_at-25000 from Gene where symbol="%s") 
                                   and pos<(select distinct Gene.end_at+25000 from Gene where symbol="%s")
                                   order by chr,pos;"""%(symbol,symbol,symbol)
                        cursor.execute(query)
                        rows=cursor.fetchall()
                        print("Content-type: text/html\n")
                        for row in rows:
                                print(row[0]+"\t"+str(row[1])+"\t"+row[2]+"\t"+row[3])
                elif ENSG:
                        ENSG = ENSG.upper()
                        query ="""select chr,pos,trait,snp from GWAS_catalog
                                   where chr = (select distinct Gene.chromosome from Gene where ENSG="%s")
                                   and pos>(select distinct Gene.start_at-25000 from Gene where ENSG="%s")
                                   and pos<(select distinct Gene.end_at+25000 from Gene where ENSG="%s")
                                   order by chr,pos;"""%(ENSG,ENSG,ENSG)
                        cursor.execute(query)
                        rows=cursor.fetchall()
                        print("Content-type: text/html\n")
                        for row in rows:
                                print(row[0]+"\t"+str(row[1])+"\t"+row[2]+"\t"+row[3])

 
        cursor.close()
        connection.close()
else:
        print("Content-type: text/html\n")

