#!/share/pkg.7/python3/3.6.10/install/bin/python3
import sys
import os
import sqlite3
import cgi
import cgitb
cgitb.enable()
form = cgi.FieldStorage()
if form:
	# Connect to the database.
	connection = sqlite3.connect("/restricted/projectnb/casa/_jychung/_gene2protein/db_g2p/gene2protein_v1.db")
	cursor = connection.cursor()
	submit = form.getvalue("submit")
	if submit:
		symbol = form.getvalue("symbol")
		ENSG = form.getvalue("ENSG")
		if symbol and ENSG:
			query2 = """SELECT Isoform.ENST, Isoform.chr, Isoform.start_at, Isoform.end_at,Isoform.transcription_type, Isoform.PDBID 
                    FROM Isoform JOIN Gene USING (ENSG)
                    WHERE Gene.symbol = "%s" AND Gene.ENSG="%s";"""%(symbol,ENSG)
			cursor.execute(query2)
			rows=cursor.fetchall()
			print("Content-type: text/html\n")
			for row in rows:
				print(row[0],row[1],row[2],row[3],row[4],row[5])

		elif symbol:
			symbol = symbol.upper()
			query2 = """SELECT Isoform.ENST, Isoform.chr, Isoform.start_at, Isoform.end_at,Isoform.transcription_type, Isoform.PDBID 
                    FROM Isoform JOIN Gene USING (ENSG)
                    WHERE Gene.symbol = "%s";"""%symbol
			cursor.execute(query2)
			rows=cursor.fetchall()
			print("Content-type: text/html\n")
			for row in rows:
				print(row[0],row[1],row[2],row[3],row[4],row[5])
		elif ENSG:
			ENSG = ENSG.upper()
			query2 = """SELECT Isoform.ENST, Isoform.chr, Isoform.start_at, Isoform.end_at,Isoform.transcription_type, Isoform.PDBID 
                    FROM Isoform JOIN Gene USING (ENSG)
                    WHERE Gene.ENSG = "%s";"""%ENSG
			cursor.execute(query2)
			rows=cursor.fetchall()
			print("Content-type: text/html\n")
			for row in rows:
				print(row[0],row[1],row[2],row[3],row[4],row[5])

	cursor.close()
	connection.close()
else:
	print("Content-type: text/html\n")
