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
                protein = form.getvalue("PDB")
                #protein = '2HEY'
                if protein:
                        protein = protein.upper()
                        query = """SELECT distinct ENSG, symbol, chromosome, start_at, end_at, description,gene_type
                                    FROM Gene
                                    WHERE ENSG in (SELECT distinct ENSG FROM Isoform WHERE PDBID="%s");""" % protein
                        cursor.execute(query)
                        rows=cursor.fetchall()
                        print("Content-type: text/html\n")
                        for row in rows:
                                temp = []
                                for x in row:
                                        temp.append(str(x))
                                line = "\t".join(temp)
                                print(line)
        cursor.close()
        connection.close()
else:
        print("Content-type: text/html\n")
