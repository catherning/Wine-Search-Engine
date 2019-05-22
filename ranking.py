#https://github.com/3003/Text-Retrieval-Python/blob/master/tfidf.py
#https://towardsdatascience.com/tf-idf-for-document-ranking-from-scratch-in-python-on-real-world-dataset-796d339a4089
# https://www.researchgate.net/post/What_is_a_good_way_to_perform_topic_modeling_on_short_text
#Don't normalize with doc length as doc are short

#https://www.cl.cam.ac.uk/teaching/1314/InfoRtrv/lecture4.pdf

#VSM

import json
import math
import sqlite3

#TODO for query to move later
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from collections import Counter
from operator import itemgetter
import heapq

path="D:/Documents/Tsinghua/WIR-WineSearch/"

conn = sqlite3.connect(path+'wines.db')
c = conn.cursor()
# (wine_id INTEGER PRIMARY KEY,country TEXT,description TEXT,name TEXT,score INTEGER,price REAL,province TEXT,region_1 TEXT,region_2 TEXT, vintage INTEGER,variety TEXT,winery TEXT, url TEXT)''')

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
        tf_idf_dict[t_id][doc]=(1+math.log10(tf_td))*df_t
        #XXX it's sparse, but there's no count if word not present in doc (not a matrix in itself)

print(tf_idf_dict)
print("Calculation of tf-idf of all words in vocabulary done.")

#================================= Query, TODO later in another file

with open(path+"vocabulary_id.json") as f:
    vocabulary=json.load(f)

ps = PorterStemmer()
stop_words = list(stopwords.words('english')) 
tokenizer = RegexpTokenizer(r'\w+')

query="cheval blanc white citrus"

sentence = query.lower()
tokens = tokenizer.tokenize(sentence)
filtered_sentence = [w for w in tokens if not w in stop_words] 

stemmed_query=[]
not_in_voc=[] #XXX TODO process them by checking if they are winery, region, country, vintage, type of wine etc ??
#XXX And/Or later add filters for price, score

for word in filtered_sentence:
    stem_w=ps.stem(word)

    #XXX if query word not in vocabulary, not taken care of with VSM!!!!
    if stem_w in vocabulary:
        stemmed_query.append(vocabulary[stem_w])
    else:
        not_in_voc.append(word) #keeping the full word for checking against the other values in database

#Get similarity with docs
query_dict=Counter(stemmed_query)
size_query=len(stemmed_query)

similarity_list=[0.]*TOTAL_DOCS
for query_w_id, count in query_dict.items():
    tf_q=count/size_query

    for doc,weight in tf_idf_dict[query_w_id].items():
        similarity_list[int(doc)]+=tf_q*weight

#TODO how to get the pages with no description of wine? How to get results if no word matches any description ???????

print("Calculated similarity for all with the terms.")

relevant_doc_id=list(zip(*heapq.nlargest(5, enumerate(a), key=itemgetter(1)))[0])

print(relevant_doc_id)

conn = sqlite3.connect(path+'wines.db')
c = conn.cursor()
# (wine_id INTEGER PRIMARY KEY,country TEXT,description TEXT,name TEXT,score INTEGER,price REAL,province TEXT,region_1 TEXT,region_2 TEXT, vintage INTEGER,variety TEXT,winery TEXT, url TEXT)''')


sql="select * from wines where wine_id in ({seq})".format(
seq=','.join(['?']*len(relevant_doc_id)))

c.execute(sql, relevant_doc_id)

results=c.fetchall() 
conn.commit()    

print(results)

conn.close()

