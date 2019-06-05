#https://github.com/3003/Text-Retrieval-Python/blob/master/tfidf.py
#https://towardsdatascience.com/tf-idf-for-document-ranking-from-scratch-in-python-on-real-world-dataset-796d339a4089
# https://www.researchgate.net/post/What_is_a_good_way_to_perform_topic_modeling_on_short_text
#Don't normalize with doc length as doc are short

#https://www.cl.cam.ac.uk/teaching/1314/InfoRtrv/lecture4.pdf

#VSM

import json
import math
import sqlite3

path="D:/Documents/Tsinghua/WIR-WineSearch/"

conn = sqlite3.connect(path+'wines.db')
c = conn.cursor()
# (wine_id INTEGER PRIMARY KEY,country TEXT,description TEXT,name TEXT,score INTEGER,price REAL,province TEXT,region_1 TEXT,region_2 TEXT, vintage INTEGER,variety TEXT,winery TEXT,type TEXT, url TEXT)''')

c.execute('''SELECT MAX(wine_id) from wines''')

TOTAL_DOCS=c.fetchone()[0]+1 
conn.commit()
conn.close()

print(TOTAL_DOCS)

with open(path+"inverted_index.json") as f:
    inverted_index_dict=json.load(f)

with open(path+"postings.json") as f:
    postings=json.load(f)

print("Loaded inverted index and postings.")

tf_idf_dict={}

for t_id,word_data in inverted_index_dict.items():
    df_t=word_data["doc_nb"]
    idf_t=math.log10(TOTAL_DOCS/df_t)

    tf_idf_dict[t_id]={}
    for doc,tf_td in postings[t_id].items():
        tf_idf_dict[t_id][doc]=(1+math.log10(tf_td))*idf_t

print("Calculation of tf-idf of all words in vocabulary done.")

with open(path+"tf_idf.json","w") as f:
    json.dump(tf_idf_dict, f, sort_keys=True, indent=4)

