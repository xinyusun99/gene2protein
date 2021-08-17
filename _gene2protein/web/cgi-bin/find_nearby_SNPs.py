#!/share/pkg.7/python3/3.6.10/install/bin/python3
import sys
import os
#import pymysql
import sqlite3
import cgi
import cgitb
import urllib.request
import numpy
cgitb.enable()
form = cgi.FieldStorage()
#form = 'y'
if form:
  # Connect to the database.
  connection = sqlite3.connect("/restricted/projectnb/casa/_jychung/_gene2protein/db_g2p/gene2protein_v1.db")
  cursor = connection.cursor()
  submit = form.getvalue("submit")
  #submit = 'y'
  if submit:
    print("Content-type: text/html\n")
    PDB=form.getvalue("PDB")
    PDB=PDB.upper()
    #PDB = '5DHG'
    select_chain=form.getvalue("chain")
    select_residue=form.getvalue("residue")
    nr = form.getvalue("range")
    #nr = 6
    if not nr:
      nr = 3
    else:
      nr = int(nr)
    #select_chain = 'A'
    #select_residue = '261'
    chain_num=[]
    residue_num=[]
    ###download pdb files from rcsb and parse the pdb name into two address below##
    dwnld_from = "http://files.rcsb.org/view/%s.pdb"%(PDB)
    dwnld_adrs = "/restricted/projectnb/casa/_jychung/_gene2protein/pdb_log/%s.pdb"%(PDB)
    urllib.request.urlretrieve(dwnld_from, dwnld_adrs)
    x_coord=[]
    y_coord=[]
    z_coord=[]
    with open(dwnld_adrs, 'r') as f:
        for line in f.readlines():
            if line[:4]=="ATOM":
                line=line.split()
                #print(line[4],line[5],line[6],line[7],line[8])
                try:
                    residue_num.append(str(int(line[5])))
                    chain_num.append(line[4])
                    x_coord.append(line[6])
                    y_coord.append(line[7])
                    z_coord.append(line[8])
                except ValueError:
                    continue
    x_coord = numpy.array(x_coord)
    y_coord = numpy.array(y_coord)
    z_coord = numpy.array(z_coord)
    atom_coord = numpy.column_stack((x_coord,y_coord,z_coord))
    atom_coord = atom_coord.astype(numpy.float)
    residue_chain_comb = list(zip(residue_num,chain_num))
    all_match=[]
    for i in range(len(residue_chain_comb)):
        if residue_chain_comb[i]==(select_residue,select_chain):
            all_match = numpy.append(all_match,atom_coord[i])
    all_match = numpy.array(all_match)
    all_match = all_match.reshape((len(all_match)//3,3))
    #print(all_match)
    avg_match = numpy.average(all_match,axis=0)
    #print(avg_match)
    nearby_residue=[]
    comp_residue_chain=[]
    for i in range(len(atom_coord)):
        if (avg_match[0]-nr)<=atom_coord[i][0]<=(avg_match[0]+nr):
            if (avg_match[1]-nr)<=atom_coord[i][1]<=(avg_match[1]+nr):
                if (avg_match[2]-nr)<=atom_coord[i][2]<=(avg_match[2]+nr):
                    nearby_residue = numpy.append(nearby_residue,atom_coord[i])
                    comp_residue_chain.append(residue_chain_comb[i])
    nearby_residue=numpy.array(nearby_residue)
    nearby_residue=nearby_residue.reshape((len(nearby_residue)//3,3))
    #print(comp_residue_chain)
    uniq_res_chain = list(set(comp_residue_chain))
    #print(uniq_res_chain)
    if len(uniq_res_chain) != 0:
      for i in range(len(uniq_res_chain)):     
          query2 = '''select distinct chr,position from Protein
                      where PDBID = "%s" and Chain_number = "%s" and AA_number = %d''' % (PDB,uniq_res_chain[i][1],int(uniq_res_chain[i][0]))
          cursor.execute(query2)
          results2 = cursor.fetchall()
          if results2:
              for x in results2:
                  query3='''select distinct snp,ENST,consequence,sift_prediction,sift_score,polyphen_prediction,polyphen_score from VEP
                            where chr="%s" and start_at=%d''' % (x[0],x[1])
                  cursor.execute(query3)
                  results3 = cursor.fetchall()
                  if not results3:
                      query4='''select distinct snp from Exon_SNP 
                                where chr="%s" and position=%d''' % (x[0],x[1])
                      cursor.execute(query4)
                      results3 = cursor.fetchall()
                      query5='''select distinct snp from Genome_SNP
                                where chr="%s" and position=%d''' % (x[0],x[1])
                      cursor.execute(query5)
                      while True:
                          record = cursor.fetchone()
                          if record:
                              results3.append(record)
                          else:
                              break
                  results3 = set(results3)
                  for row in results3:
                      if len(row) == 1:
                          print(str(row[0])+"\t"+str(x[0])+"\t"+str(x[1])+"\t"+str(uniq_res_chain[i][1])+"\t"+str(uniq_res_chain[i][0])+"\t"+PDB+"\t"+"."+"\t"+"."+"\t"+"."+"\t"+"."+"\t"+"."+"\t"+".")
                      else:
                          print(str(row[0])+"\t"+str(x[0])+"\t"+str(x[1])+"\t"+str(uniq_res_chain[i][1])+"\t"+str(uniq_res_chain[i][0])+"\t"+PDB+"\t"+row[1]+"\t"+row[2]+"\t"+row[3]+"\t"+str(row[4])+"\t"+row[5]+"\t"+str(row[6]))

          query_res = '''select chr,min(position),max(position) from Protein
                         where PDBID="%s" and Chain_number="%s" and AA_number=%d''' % (PDB,uniq_res_chain[i][1],int(uniq_res_chain[i][0]))
          cursor.execute(query_res)
          while True:
              record = cursor.fetchone()
              if record:
                  print("Residue:"+str(uniq_res_chain[i][0])+"\t"+str(record[0])+"\t"+str(record[1])+"-"+str(record[2])+"\t"+str(uniq_res_chain[i][1])+"\t"+str(uniq_res_chain[i][0])+"\t"+PDB+"\t"+"."+"\t"+"."+"\t"+"."+"\t"+"."+"\t"+"."+"\t"+".")
              else:
                  break
  cursor.close()
  connection.close()
else:
        print("Content-type: text/html\n")
