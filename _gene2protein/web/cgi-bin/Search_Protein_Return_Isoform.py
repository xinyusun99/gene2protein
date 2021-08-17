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
                #protein = '2hey'
                if protein:
                        protein = protein.upper()
                        query = """SELECT distinct ENST,chr,start_at,end_at,transcription_type,PDBID
                                   FROM Isoform
                                   WHERE PDBID="%s";"""%(protein)
                        cursor.execute(query)
                        rows=cursor.fetchall()
                        print("Content-type: text/html\n")
                        for row in rows:
                                print(row[0],row[1],row[2],row[3],row[4],row[5])
        cursor.close()
        connection.close()
else:
        print("Content-type: text/html\n")
