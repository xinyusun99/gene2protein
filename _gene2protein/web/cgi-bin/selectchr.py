#!/share/pkg.7/python3/3.6.10/install/bin/python3
#import pymysql
import sqlite3
import cgi
import cgitb
cgitb.enable()
form = cgi.FieldStorage()
if form:
        # Connect to the database.
        #connection = pymysql.connect(host='bioed.bu.edu',database='groupE',user='xdhan',password='xdhan',port=4253)
        #cursor = connection.cursor()
        connection = sqlite3.connect("/restricted/projectnb/casa/_jychung/_gene2protein/db_g2p/gene2protein_v1.db")
        cursor = connection.cursor()
        submit = form.getvalue("submit")
        if submit:
            print("Content-type: text/html\n")
            Chr = form.getvalue("Chr")
            query = """SELECT max(end_at) FROM Gene WHERE chromosome='%s';"""%(Chr)
            cursor.execute(query)
            rows=cursor.fetchall()
            print(rows[0][0])
else:
    print("Content-type: text/html\n")
