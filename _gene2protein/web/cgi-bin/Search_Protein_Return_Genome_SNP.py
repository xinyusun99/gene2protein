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
                PDB = form.getvalue("PDB")
                #PDB = '2wxw'
                if PDB:
                        print("Content-type: text/html\n")
                        PDB = PDB.upper()
                        query0 = '''select chr,min(position),max(position) from Protein
                                    where PDBID="%s"''' % PDB
                        cursor.execute(query0)
                        result0 = cursor.fetchall()[0]
                        if result0[0] != None:
                            query1 = '''select distinct snp,chr,position from Genome_SNP
                                        where chr="%s" and position>=%d and position<=%d;''' % (result0[0],result0[1],result0[2])
                            cursor.execute(query1)
                            result1 = cursor.fetchall()
                            for x in result1:
                                if x:
                                    queryx = '''select distinct Chain_number,AA_number,PDBID from Protein
                                                where chr="%s" and position=%d;''' % (x[1],x[2])
                                    cursor.execute(queryx)
                                    resultx = cursor.fetchall()
                                    for y in resultx:
                                        if y and y[2] == PDB:
                                            print(x[0]+"\t"+x[1]+"\t"+str(x[2])+"\t"+y[0]+"\t"+str(y[1])+"\t"+y[2])

        cursor.close()
        connection.close()

else:
        print("Content-type: text/html\n")
