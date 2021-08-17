#!/usr/bin/python2
# -*- coding: UTF-8 -*-
#import cgi
print "Content-type: text/html\n"
import sys
#sys.path.append('/share/pkg.7/python2/2.7.16/install/')
import random
import cgi
import sqlite3
import numpy as np
#sys.path.append('/share/pkg.7/python2/2.7.16/install/')
#print("Content-type: text/html\n")
print sys.version
#print(sys.prefix)
print np.arange(5)
#print("hello world")
#print("")
#print("test")
connection = sqlite3.connect("/restricted/projectnb/casa/_jychung/_gene2protein/db_g2p/gene2protein_v1.db")
cursor = connection.cursor()
query1 = """SELECT ENSG, symbol, chromosome, start_at, end_at, description,gene_type
            FROM Gene WHERE symbol="%s";""" % "TP53"
cursor.execute(query1)
rows=cursor.fetchall()
print rows
connection.close()
#print(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

#y =  2  * x +  5
#plt.plot(x,y) 
#plt.show()
#print("<img src='https://bioed.bu.edu/images/students_20/jh50/test.png' alt='test plot' width='600' height='345' />")
#print("<img src='/var/www/cgi-bin/students_20/jh50/others/test.png' alt='test plot' width='600' height='345' />")
#print("%s" %(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
