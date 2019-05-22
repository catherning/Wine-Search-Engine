# coding: utf-8

# ======= Initializating the DB with winemag reviews

import sqlite3
import csv
import re
import datetime
from os import listdir


path="D:/Documents/Tsinghua/WIR-WineSearch/"

conn = sqlite3.connect(path+'wines.db')

c = conn.cursor()
c.execute('''DROP TABLE wines''') #TODO remove when rest ok

# Create table
c.execute('''CREATE TABLE wines
             (wine_id INTEGER PRIMARY KEY,country TEXT,description TEXT,name TEXT,score INTEGER,price REAL,province TEXT,region_1 TEXT,region_2 TEXT, vintage INTEGER,variety TEXT,winery TEXT,type TEXT, url TEXT)''')


a=datetime.datetime.now()
to_insert=[]
# 2nde Winemag dataset with 250K wines
# 0 alcohol, 1 category, 2 country, 3 description, 4 designation,5 price,6 rating,7 region,
# 8 subregion,9 subsubregion,10 title,11 url,12 varietal,13v intage,14 winery
#XXX name is either designation or title (removed vintage and winery so designation ?)

# temp=[]

count_wine=0
winemag_files = listdir(path+"winemag-raw-250k-v1/")
for csv_f in winemag_files:
    with open(path+"winemag-raw-250k-v1/"+csv_f,'r',encoding="utf-8") as f:
        spamreader = csv.reader(f)
        next(spamreader)
        for line in spamreader:

            to_insert.append(tuple([count_wine]+line[2:4]+[line[4],line[6],line[5]]+line[7:10]+[line[13],line[12],line[14],line[1],line[11]]))
            count_wine+=1
            
            # temp.append(line[3])

#print(to_insert)

# count_already_in=0
# # 150K dataset ===============> 116348/129970 already in the bigger dataset..
# with open(path+"wine-reviews/"+"winemag-data-130k-v2.csv",'r',encoding="utf-8") as f:
#     spamreader = csv.reader(f)
#     next(spamreader)
#     for i,line in enumerate(spamreader):
#         year=re.search("\d{4}", line[11], flags=0)
#         if year:
#             year=year.group()
#         else:
#             year=None
        
#         if i%1000==0:
#             print(i)

#         processed_line=tuple([i]+line[1:9]+[year]+line[12:]+["","www.winemag.com"])
#         # Check if not already in the first dataset
#         if line[2] in temp:
#             count_already_in+=1
#             temp.remove(line[2])
#             # print(line[0])
#         else:
#             continue
        
#             # to_insert.append(processed_line)
# print(count_already_in)



c.executemany('''INSERT INTO wines(wine_id,country,description,name,score,price,province,region_1,region_2,vintage,variety,winery,type,url)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', to_insert) #TODO check if ok ? removed () for to_insert
conn.commit()
conn.close()

print("Duration: {}".format(datetime.datetime.now()-a))



