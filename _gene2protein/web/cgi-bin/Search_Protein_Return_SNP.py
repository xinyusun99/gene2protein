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
                #PDB = '2hey'
                #PDB = '2wxw'
                if PDB:
                        print("Content-type: text/html\n")
                        PDB = PDB.upper()
                        query0 = '''select chr,min(position),max(position) from Protein
                                    where PDBID="%s"''' % PDB
                        cursor.execute(query0)
                        result0 = cursor.fetchall()[0]
                        if result0[0] != None:
                            query1 = '''select distinct snp,chr,position from Exon_SNP
                                        where chr="%s" and position>=%d and position<=%d;''' % (result0[0],result0[1],result0[2])
                            cursor.execute(query1)
                            result1 = cursor.fetchall()

                            query2 = '''select distinct snp,chr,position from Genome_SNP
                                        where chr="%s" and position>=%d and position<=%d;''' % (result0[0],result0[1],result0[2])
                            cursor.execute(query2)
                            while True:
                                record = cursor.fetchone()
                                if record:
                                    result1.append(record)
                                else:
                                    break

                            query3 = '''select distinct snp,chr,start_at from VEP
                                        where chr="%s" and start_at>=%d and start_at<=%d;''' % (result0[0],result0[1],result0[2])
                            cursor.execute(query3)
                            while True:
                                record = cursor.fetchone()
                                if record:
                                    result1.append(record)
                                else:
                                    break

                            result1 = set(result1)
                            for x in result1:
                                if x:
                                    queryx = '''select distinct Chain_number,AA_number,PDBID from Protein
                                                where chr="%s" and position=%d;''' % (x[1],x[2])
                                    cursor.execute(queryx)
                                    resultx = cursor.fetchall()
                                    queryz = '''select distinct ENST,consequence,sift_prediction,sift_score,polyphen_prediction,polyphen_score from VEP
                                                where snp="%s";''' % (x[0])
                                    cursor.execute(queryz) 
                                    resultz = cursor.fetchall()                 
                                    for y in resultx:
                                        if y and y[2] == PDB and resultz:
                                            for z in resultz:
                                                print(x[0]+"\t"+x[1]+"\t"+str(x[2])+"\t"+y[0]+"\t"+str(y[1])+"\t"+y[2]+"\t"+z[0]+"\t"+z[1]+"\t"+z[2]+"\t"+str(z[3])+"\t"+z[4]+"\t"+str(z[5]))
                                        elif y and y[2] == PDB and not resultz:
                                            print(x[0]+"\t"+x[1]+"\t"+str(x[2])+"\t"+y[0]+"\t"+str(y[1])+"\t"+y[2]+"\t"+"."+"\t"+"."+"\t"+"."+"\t"+"."+"\t"+"."+"\t"+".")
                        query_res = '''select chr,min(position),max(position),Chain_number,AA_number from Protein
                                       where PDBID="%s"
                                       group by Chain_number,AA_number''' % PDB
                        cursor.execute(query_res)
                        while True:
                            record = cursor.fetchone()
                            if record:
                                print("Residue:"+str(record[4])+"\t"+str(record[0])+"\t"+str(record[1])+"-"+str(record[2])+"\t"+str(record[3])+"\t"+str(record[4])+"\t"+PDB+"\t"+"."+"\t"+"."+"\t"+"."+"\t"+"."+"\t"+"."+"\t"+".")
                            else:
                                break
                        #results_res = cursor.fetchall()
                        #print(results_res)
                        #query_res =  '''select distinct Chain_number,AA_number from Protein
                                        #where PDBID="%s"''' % PDB
                        #cursor.execute(query_res)
                        #results_res = cursor.fetchall()
                        #for record in results_res:
                        #        query_pos = '''select chr,min(position),max(position) from Protein
                        #                       where PDBID="%s" and Chain_number="%s" and AA_number=%d''' % (PDB,record[0],record[1])
            
        
        cursor.close()
        connection.close()

else:
        print("Content-type: text/html\n")                    
                            
