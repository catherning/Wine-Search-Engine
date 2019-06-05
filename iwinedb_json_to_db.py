import sqlite3
import json
import datetime
import locale

path="D:/Documents/Tsinghua/WIR-WineSearch/"
locale.setlocale(locale.LC_NUMERIC, 'enn')

conn = sqlite3.connect(path+'wines.db')
c = conn.cursor()

# c.execute('''CREATE TABLE wines
            #  (wine_id INTEGER PRIMARY KEY,country TEXT,description TEXT,name TEXT,score INTEGER,price REAL,province TEXT,region_1 TEXT,region_2 TEXT, vintage INTEGER,variety TEXT,winery TEXT,type TEXT, url TEXT)''')


c.execute('''SELECT MAX(wine_id) from wines''')

init_nb_wines=c.fetchone()[0]+1 

print(init_nb_wines)


with open(path+"wines_iwinedb.json") as f:
    data=json.load(f)



a=datetime.datetime.now()
to_insert=[]
for i,wine in enumerate(data):
    
    row=[init_nb_wines+i]+[wine["country"],"",wine["name"].replace(wine["winery"],""),wine["score"]]
    
    if wine["price"]==None:
        price=[None]
    # Remove the $
    else:
        price=[locale.atof(wine["price"][1:])] 
    
    if len(wine["region"])<=3:
        regions=wine["region"]+[None]*(3-len(wine["region"]))
    else:
        regions=wine["region"][:3]
    row=row+price+regions+[wine["vintage"],wine["variety"],wine["winery"],wine["type_wine"],wine["url"]]

    to_insert.append(tuple(row))

    
c.executemany('''INSERT INTO wines(wine_id,country,description,name,score,price,province,region_1,region_2,vintage,variety,winery,type,url)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (to_insert))

conn.commit()

print("Duration: {}".format(datetime.datetime.now()-a))

conn.close()