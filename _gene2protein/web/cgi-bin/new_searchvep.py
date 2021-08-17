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
                snp = form.getvalue("SNP")
                if snp:
                        query = """select distinct * from VEP where snp="%s";"""%snp
                        cursor.execute(query)
                        rows=cursor.fetchall()
                        print("Content-type: text/html\n")
                        for row in rows:
                                temp = []
                                for x in row:
                                        temp.append(str(x))  
                                line = "\t".join(temp)
                                print(line)
                                #print(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12])

        cursor.close()
        connection.close()
else:
        print("Content-type: text/html\n")

"""
import pymysql
connection = pymysql.connect(host="ensembldb.ensembl.org", user="anonymous", db="homo_sapiens_variation_99_37",password="",port=3337)
cursor = connection.cursor()
query = '''select variation.name,feature_stable_id,transcript_variation.allele_string,seq_region_id, seq_region_start,seq_region_end,
           transcript_variation.consequence_types,sift_prediction,
           sift_score,polyphen_prediction,polyphen_score
           from variation join variation_feature using(variation_id)
           join transcript_variation using(variation_feature_id)
           where variation.name="rs699";'''
cursor.execute(query)
row = cursor.fetchall()
for x in row:
    x = list(x)
    query2 = '''select distinct name from seq_region
                where seq_region_id=%d''' % x[3]
    cursor.execute(query2)
    x[3] = cursor.fetchall()[0][0]
    print(x)
#print(row)
cursor.close()
connection.close()
"""
