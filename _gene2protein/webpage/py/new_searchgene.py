#!/usr/local/Python-3.7/bin/python3
import sys
import os
import pymysql
import cgi
import cgitb
cgitb.enable()
form = cgi.FieldStorage()
if form:
	# Connect to the database.
	connection = pymysql.connect(host='bioed.bu.edu',database='groupE',user='xdhan',password='xdhan',port=4253)
	cursor = connection.cursor()
	submit = form.getvalue("submit")
	if submit:
		symbol = form.getvalue("symbol")
		ENSG = form.getvalue("ENSG")
		if symbol and ENSG:
			query1 = """SELECT ENSG, symbol, chr, start_at, end_at, description FROM Gene WHERE symbol="%s" AND ENSG="%s";"""%(symbol,ENSG)
			cursor.execute(query1)
			rows=cursor.fetchall()
			print("Content-type: text/html\n")
			for row in rows:
				print(row[0],row[1],row[2],row[3],row[4],row[5])                        
		elif symbol:
			query1 = """SELECT ENSG, symbol, chr, start_at, end_at, description FROM Gene WHERE symbol="%s";"""%symbol
			cursor.execute(query1)
			rows=cursor.fetchall()
			print("Content-type: text/html\n")
			for row in rows:
				print(row[0],row[1],row[2],row[3],row[4],row[5])
		elif ENSG:
			query1 = """SELECT ENSG, symbol, chr, start_at, end_at, description FROM Gene WHERE ENSG="%s";"""%ENSG
			cursor.execute(query1)
			rows=cursor.fetchall()
			print("Content-type: text/html\n")
			for row in rows:
				print(row[0],row[1],row[2],row[3],row[4],row[5])
	
	cursor.close()
	connection.close()
else:
	print("Content-type: text/html\n")
	
