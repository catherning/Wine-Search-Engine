from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from collections import Counter
from operator import itemgetter
import heapq
import json
import sqlite3

NB_RESULTS=10
path="D:/Documents/Tsinghua/WIR-WineSearch/"

conn = sqlite3.connect(path+'wines.db')
c = conn.cursor()
# (wine_id INTEGER PRIMARY KEY,country TEXT,description TEXT,name TEXT,score INTEGER,price REAL,province TEXT,region_1 TEXT,region_2 TEXT, vintage INTEGER,variety TEXT,winery TEXT, url TEXT)''')

c.execute('''SELECT MAX(wine_id) from wines''')

TOTAL_DOCS=c.fetchone()[0]+1 
conn.commit()
conn.close()

print(TOTAL_DOCS)


with open(path+"vocabulary_id.json") as f:
    vocabulary=json.load(f)

with open(path+"tf_idf.json") as f:
    tf_idf_dict=json.load(f)

# Processing the query

ps = PorterStemmer()
stop_words = list(stopwords.words('english'))
tokenizer = RegexpTokenizer(r'\w+')

query="domb perignon citrus sweet young"

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


# ============================ Finding the relevant results =================================

# Get similarity with docs
query_dict=Counter(stemmed_query)
size_query=len(stemmed_query)

similarity_list=[0.]*TOTAL_DOCS
for query_w_id, count in query_dict.items():
    tf_q=count/size_query

    for doc,weight in tf_idf_dict[str(query_w_id)].items():
        similarity_list[int(doc)]+=tf_q*weight

#TODO how to get the pages with no description of wine? How to get results if no word matches any description ???????

print("Calculated similarity for all with the terms.")

relevant_doc_id=list(zip(*heapq.nlargest(NB_RESULTS, enumerate(similarity_list), key=itemgetter(1))))[0]
#[1] is the similarity score

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
