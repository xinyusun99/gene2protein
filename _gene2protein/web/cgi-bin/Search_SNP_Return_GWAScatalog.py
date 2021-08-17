#!/share/pkg.7/python3/3.6.10/install/bin/python3
import sys
import os
#import pymysql
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
        #submit = 'y'
        if submit:
                snp = form.getvalue("SNP")
                #snp = 'rs35850753'
                if snp:
                        query = """select distinct chr,pos,trait,snp from GWAS_catalog
                                   where snp='%s'""" % snp
                        cursor.execute(query)
                        rows=cursor.fetchall()
                        print("Content-type: text/html\n")
                        for row in rows:
                                print(row[0]+"\t"+str(row[1])+"\t"+row[2]+"\t"+row[3])
        cursor.close()
        connection.close()
else:
        print("Content-type: text/html\n")
