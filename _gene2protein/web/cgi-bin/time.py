#!/share/pkg.7/python3/3.6.10/install/bin/python3
#-*- coding: UTF-8 -*-
print("Content-type: text/html\n")
import sys
#sys.path.append('/share/pkg.7/python2/2.7.16/install/')
import random
import cgi
import sqlite3 
#import numpy as np
#print("Content-type: text/html\n")
#print sys.version
#print(sys.prefix)
#print np.arange(5)
#print("hello world")
#print("")
#print("test")
connection = sqlite3.connect("/restricted/projectnb/casa/_jychung/_gene2protein/db_g2p/gene2protein_v1.db")
cursor = connection.cursor()
query1 = """SELECT ENSG, symbol, chromosome, start_at, end_at, description,gene_type
            FROM Gene WHERE symbol="%s";""" % "TP53"
cursor.execute(query1)
rows=cursor.fetchall()[0]
#rows = [str(x) for x in rows]
#rows = [x.encode('utf-8') for x in rows]
print(rows)
cursor.close()
connection.close()
