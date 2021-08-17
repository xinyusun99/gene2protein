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
                symbol = form.getvalue("symbol")
                ENSG = form.getvalue("ENSG")
                #symbol = None
                #ENSG = 'ENSG00000141510'
                
                if symbol:
                        symbol = symbol.upper()
                        #query = """select * from VEP
                        #           where chr = (select distinct Gene.chromosome from Gene where symbol='%s')
                        #           and end_at>(select distinct Gene.start_at from Gene where symbol='%s')
                        #           and start_at<(select distinct Gene.end_at from Gene where symbol='%s')
                        #           and (sift_prediction!='tolerated' or polyphen_prediction!='benign') 
                        #           order by chr,start_at;"""%(symbol,symbol,symbol)
                        query = """select * from VEP
                                   where chr = (select distinct Gene.chromosome from Gene where symbol='%s')
                                   and end_at>(select distinct Gene.start_at from Gene where symbol='%s')
                                   and start_at<(select distinct Gene.end_at from Gene where symbol='%s')
                                   order by chr,start_at;"""%(symbol,symbol,symbol)
                        cursor.execute(query)
                        rows=cursor.fetchall()
                        print("Content-type: text/html\n")
                        for row in rows:
                                temp = []
                                for x in row:
                                        temp.append(str(x))
                                line = "\t".join(temp)
                                print(line)
                elif ENSG:
                        ENSG = ENSG.upper()
                        #query ="""select * from VEP
                        #          where chr = (select distinct Gene.chromosome from Gene where ENSG='%s')
                        #          and end_at>(select distinct Gene.start_at from Gene where ENSG='%s')
                        #          and start_at<(select distinct Gene.end_at from Gene where ENSG='%s')
                        #          and (sift_prediction!='tolerated' and polyphen_prediction!='benign')
                        #          order by chr,pos;"""%(ENSG,ENSG,ENSG)
                        query ="""select * from VEP
                                  where chr = (select distinct Gene.chromosome from Gene where ENSG='%s')
                                  and end_at>(select distinct Gene.start_at from Gene where ENSG='%s')
                                  and start_at<(select distinct Gene.end_at from Gene where ENSG='%s')
                                  order by chr,start_at;"""%(ENSG,ENSG,ENSG)
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
