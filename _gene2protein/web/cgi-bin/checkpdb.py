#!/share/pkg.7/python3/3.6.10/install/bin/python3
import sys
import os
#import pymysql
import sqlite3
import cgi
import cgitb
cgitb.enable()
form = cgi.FieldStorage()
if form:
        # Connect to the database.
        connection = sqlite3.connect("/restricted/projectnb/casa/_jychung/_gene2protein/db_g2p/gene2protein_v1.db")
        cursor = connection.cursor()
        submit = form.getvalue("submit")
        if submit:
                PDB = form.getvalue("PDB")
                if PDB:
                        PDB = PDB.upper()
                        query1 = """SELECT * FROM Isoform WHERE PDBID = '%s';"""%(PDB)
                        cursor.execute(query1)
                        rows=cursor.fetchall()
                        print("Content-type: text/html\n")
                        for row in rows:
                                print(row[-1])

        cursor.close()
        connection.close()
else:
        print("Content-type: text/html\n")

