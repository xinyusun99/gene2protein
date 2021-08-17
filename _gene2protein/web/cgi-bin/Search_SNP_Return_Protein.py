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
                snp = form.getvalue("SNP")
                #snp = 'rs144102157'
                if snp:
                        print("Content-type: text/html\n")
                        query1 = '''select distinct snp,chr,position from Exon_SNP
                                    where snp="%s";''' % snp
                        cursor.execute(query1)
                        result1 = cursor.fetchall()
                        if not result1:
                            query1 = '''select distinct snp,chr,position from Genome_SNP
                                        where snp="%s";''' % snp
                            cursor.execute(query1)
                            result1 = cursor.fetchall()
                            if not result1:
                                query1 = '''select distinct snp,chr,start_at from VEP
                                            where snp="%s";''' % snp
                                cursor.execute(query1)
                                result1 = cursor.fetchall()
                        for x in result1:
                            queryx = '''select distinct Chain_number,AA_number,PDBID from Protein
                                        where chr="%s" and position=%d;''' % (x[1],x[2])
                            cursor.execute(queryx)
                            resultx = cursor.fetchall()
                            for y in resultx:
                                if y:
                                    print(x[0]+"\t"+x[1]+"\t"+str(x[2])+"\t"+y[0]+"\t"+str(y[1])+"\t"+y[2])

        cursor.close()
        connection.close()

else:
        print("Content-type: text/html\n")
