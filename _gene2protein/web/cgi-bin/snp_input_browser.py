#!/share/pkg.7/python3/3.6.10/install/bin/python3
import sqlite3
import sys
import os
import cgi
import cgitb
import random

#snp = "rs699"
#string = ''.join(random.sample("abcdefghijklmnopqrstuvwxyz1234567890",8))
#os.system("/share/pkg.7/r/3.6.2/install/bin/Rscript snp_browser.R -s %s -r %s" %(gene,string))
cgitb.enable()
form = cgi.FieldStorage()
#form = 'y'
if form:
        connection = sqlite3.connect("/restricted/projectnb/casa/_jychung/_gene2protein/db_g2p/gene2protein_v1.db")
        cursor = connection.cursor()
        submit = form.getvalue("submit")
        #submit = 'y'
        if submit:
                snp = form.getvalue("SNP")
                #snp = 'rs699'
                if snp:
                        #snp = snp.lower()
                        print('Content-type: text/html\n')
                        string = ''.join(random.sample("abcdefghijklmnopqrstuvwxyz1234567890",8))
                        print(string)
                        os.system("/share/pkg.7/r/3.6.2/install/bin/Rscript snp_browser.R -s %s -r %s" %(snp,string))
        cursor.close()
        connection.close()

else:
        print('Content-type: text/html\n')
