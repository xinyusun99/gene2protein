#!/usr/bin/python3
#import cgi
print ("Content-type: text/html\n")
import sys
import random
import cgi
import sqlite3
import numpy as np
print (sys.version)
print (np.arange(5))
connection = sqlite3.connect("/restricted/projectnb/casa/_jychung/_gene2protein/db_g2p/gene2protein_v1.db")
cursor = connection.cursor()
query1 = """SELECT ENSG, symbol, chromosome, start_at, end_at, description,gene_type
            FROM Gene WHERE symbol="%s";""" % "TP53"
cursor.execute(query1)
rows=cursor.fetchall()
print (rows)
connection.close()

