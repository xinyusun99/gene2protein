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
                        query = """select distinct * from Genome_SNP
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
                        query = """select distinct * from Genome_SNP
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
                        query = """select distinct * from Genome_SNP
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
