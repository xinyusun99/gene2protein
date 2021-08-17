#!/share/pkg.7/python3/3.6.10/install/bin/python3
import sys
import os
#import random
import sqlite3
import cgi
import cgitb
cgitb.enable()
form = cgi.FieldStorage()
#form = "y"
if form:
        # Connect to the database.
        connection = sqlite3.connect("/restricted/projectnb/casa/_jychung/_gene2protein/db_g2p/gene2protein_v1.db")
        cursor = connection.cursor()
        submit = form.getvalue("submit")
        #submit = "y"
        if submit:
            plot_file1 = form.getvalue("plot_file1")
            plot_file2 = form.getvalue("plot_file2")
            if plot_file1 and plot_file2:
                print('Content-type: text/html\n')
                os.system("rm -f %s" % plot_file1)
                os.system("rm -f %s" % plot_file2)

else:
        print('Content-type: text/html\n')
