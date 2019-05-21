# coding: utf-8

# ======= Initializating the DB with winemag reviews

import sqlite3
import csv
import re
import datetime

path="D:/Documents/Tsinghua/WIR-WineSearch/"

conn = sqlite3.connect(path+'wines.db')

c = conn.cursor()
c.execute('''DROP TABLE wines''') #TODO remove when rest ok

# Create table
c.execute('''CREATE TABLE wines
             (wine_id INTEGER PRIMARY KEY,country TEXT,description TEXT,name TEXT,score INTEGER,price REAL,province TEXT,region_1 TEXT,region_2 TEXT, vintage INTEGER,variety TEXT,winery TEXT, url TEXT)''')

a=datetime.datetime.now()
to_insert=[]
with open(path+"wine-reviews/"+"winemag-data-130k-v2.csv",'r',encoding="utf-8") as f:
    spamreader = csv.reader(f)
    next(spamreader)
    for i,line in enumerate(spamreader):
        year=re.search("\d{4}", line[11], flags=0)
        if year:
            year=year.group()
        else:
            year=None
        to_insert.append(tuple([i]+line[1:9]+[year]+line[12:]+["www.winemag.com"]))

c.executemany('''INSERT INTO wines(wine_id,country,description,name,score,price,province,region_1,region_2,vintage,variety,winery,url)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)''', (to_insert))
conn.commit()

print("Duration: {}".format(datetime.datetime.now()-a))

# c.execute('''SELECT wine_id,country FROM wines''')
# print(c.fetchall())

conn.close()

