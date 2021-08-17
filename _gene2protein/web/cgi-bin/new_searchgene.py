#!/share/pkg.7/python3/3.6.10/install/bin/python3
import sys
import random
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
		symbol = form.getvalue("symbol")
		ENSG = form.getvalue("ENSG")
		#ENSG = None
		#symbol = "TP53"
		if symbol and ENSG:
			query1 = """SELECT distinct ENSG, symbol, chromosome, start_at, end_at, description,gene_type 
                                 FROM Gene WHERE symbol="%s" AND ENSG="%s";"""%(symbol,ENSG)
			cursor.execute(query1)
			rows=cursor.fetchall()
			print("Content-type: text/html\n")
			for row in rows:
				print(row[0]+"\t"+row[1]+"\t"+row[2]+"\t"+str(row[3])+"\t"+str(row[4])+"\t"+row[5]+"\t"+row[6])                        
		elif symbol:
			symbol = symbol.upper()
			query1 = """SELECT distinct ENSG, symbol, chromosome, start_at, end_at, description,gene_type 
                                 FROM Gene WHERE symbol="%s";"""%symbol
			cursor.execute(query1)
			rows=cursor.fetchall()
			print("Content-type: text/html\n")
			for row in rows:
				print(row[0]+"\t"+row[1]+"\t"+row[2]+"\t"+str(row[3])+"\t"+str(row[4])+"\t"+row[5]+"\t"+row[6])
		elif ENSG:
			ENSG = ENSG.upper()
			query1 = """SELECT distinct ENSG, symbol, chromosome, start_at, end_at, description,gene_type 
                                 FROM Gene WHERE ENSG="%s";"""%ENSG
			cursor.execute(query1)
			rows=cursor.fetchall()
			print("Content-type: text/html\n")
			for row in rows:
				print(row[0]+"\t"+row[1]+"\t"+row[2]+"\t"+str(row[3])+"\t"+str(row[4])+"\t"+row[5]+"\t"+row[6])
	
	cursor.close()
	connection.close()
else:
	print("Content-type: text/html\n")
	
