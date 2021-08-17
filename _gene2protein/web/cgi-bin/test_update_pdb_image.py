#!/usr/local/Python-3.7/bin/python3
import sys
import os
import pymysql
import cgi
import cgitb
import urllib.request
cgitb.enable()
form = cgi.FieldStorage()

print('Content-type: text/html\n')
submit = form.getvalue("submit")
PDB = form.getvalue("PDB")
PDB = "5ITA"
print("""
<html>
<head>
<script src="https://code.jquery.com/jquery-3.4.1.js"></script>
</head>
<body>

<h2>test for showing PDB 3D structure</h2>

<script type="text/javascript" src="https://chemapps.stolaf.edu/jmol/jmol.php?pdbid=%s&script=restrict not water; spacefill off; wireframe off; ribbons on; select 460:a; color red; spacefill 2.0&inline">
</script>


</body>
</html>
"""%(PDB))


