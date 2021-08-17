#!/share/pkg.7/python3/3.6.10/install/bin/python3
import sys
import os
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
                SNP = form.getvalue("SNP")
                base = form.getvalue("base")
                if SNP and base:
                        SNP = SNP.lower()
                        query1 = """SELECT * FROM Exon_SNP WHERE snp='%s' and position=%d;"""%(SNP,base)
                        cursor.execute(query1)
                        rows=cursor.fetchall()
                        print("Content-type: text/html\n")
                        for row in rows:
                                print(row[0],row[1],row[2])

                        query2 = """SELECT * FROM Genome_SNP WHERE snp='%s' and position=%d;"""%(SNP,base)
                        cursor.execute(query2)
                        rows=cursor.fetchall()
                        for row in rows:
                                print(row[0],row[1],row[2])
                        query3 = """SELECT * FROM VEP WHERE snp='%s' and start_at=%d;"""%(SNP,base)
                        cursor.execute(query3)
                        rows=cursor.fetchall()
                        for row in rows:
                                print(row[0],row[1],row[2])

                elif SNP:
                        SNP = SNP.lower()
                        query1 = """SELECT * FROM Exon_SNP WHERE snp='%s';"""%(SNP)
                        cursor.execute(query1)
                        rows=cursor.fetchall()
                        print("Content-type: text/html\n")
                        for row in rows:
                                print(row[0],row[1],row[2])
            
                        query2 = """SELECT * FROM Genome_SNP WHERE snp='%s';"""%(SNP)
                        cursor.execute(query2)
                        rows=cursor.fetchall()
                        for row in rows:
                                print(row[0],row[1],row[2])

                        query3 = """SELECT * FROM VEP WHERE snp='%s';"""%(SNP)
                        cursor.execute(query3)
                        rows=cursor.fetchall()
                        for row in rows:
                                print(row[0],row[1],row[2])

                #elif base:
                #        query1 = """SELECT * FROM Exon_SNP WHERE position=%d;"""%(base)
                #        cursor.execute(query1)
                #        rows=cursor.fetchall()
                #        print("Content-type: text/html\n")
                #        for row in rows:
                #                print(row[0],row[1],row[2],row[3])
                #        query2 = """SELECT * FROM Genome_SNP WHERE position=%d;"""%(base)
                #        cursor.execute(query2)
                #        rows=cursor.fetchall()
                #        for row in rows:
                #                print(row[0],row[1],row[2],row[3])


        cursor.close()
        connection.close()
else:
        print("Content-type: text/html\n")


