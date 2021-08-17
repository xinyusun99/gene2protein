#!/share/pkg.7/python3/3.6.10/install/bin/python3
#import sqlite3
import sys
import os
import cgi
import cgitb
import random

#gene = "tp53"
#string = ''.join(random.sample("abcdefghijklmnopqrstuvwxyz1234567890",8))
#os.system("/share/pkg.7/r/3.6.2/install/bin/Rscript gene_browser.R -s %s -r %s" %(gene,string))
cgitb.enable()
form = cgi.FieldStorage()
if form:
        #connection = sqlite3.connect("/restricted/projectnb/casa/_jychung/_gene2protein/db_g2p/gene2protein_v1.db")
        #cursor = connection.cursor()
        submit = form.getvalue("submit")
        if submit:
                chromosome = form.getvalue("Chr")
                if chromosome:
                    #print('Content-type: text/html\n')
                    start = form.getvalue('Start')
                    end = form.getvalue('End')
                    if start and end:
                        print('Content-type: text/html\n')
                        #symbol = symbol.upper()
                        string = ''.join(random.sample("abcdefghijklmnopqrstuvwxyz1234567890",8))
                        print(string)
                        os.system("/share/pkg.7/r/3.6.2/install/bin/Rscript range_browser.R -c %s -s %d -e %d -r %s" % \
                        (str(chromosome),int(start),int(end),string))
else:
        print('Content-type: text/html\n')
