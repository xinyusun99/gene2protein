#!/share/pkg.7/python3/3.6.10/install/bin/python3
import sqlite3
import sys
import os
import cgi
import cgitb
import random
cgitb.enable()
form = cgi.FieldStorage()
#isoform = "ENST00000269305"
if form:
        connection = sqlite3.connect("/restricted/projectnb/casa/_jychung/_gene2protein/db_g2p/gene2protein_v1.db")
        cursor = connection.cursor()
        submit = form.getvalue("submit")
        if submit:
                isoform = form.getvalue("ENST")
                if isoform:
                        #isoform = isoform.upper()
                        print('Content-type: text/html\n')
                        string = ''.join(random.sample("abcdefghijklmnopqrstuvwxyz1234567890",8))
                        print(string)
                        os.system("/share/pkg.7/r/3.6.2/install/bin/Rscript isoform_browser.R -t %s -r %s" %(isoform,string))
        cursor.close()
        connection.close()
else:
        print('Content-type: text/html\n')
