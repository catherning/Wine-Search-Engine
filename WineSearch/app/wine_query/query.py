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

path_to_db=path+'wines.db'

conn = sqlite3.connect(path_to_db)
c = conn.cursor()
# (wine_id INTEGER PRIMARY KEY,country TEXT,description TEXT,name TEXT,score INTEGER,price REAL,province TEXT,region_1 TEXT,region_2 TEXT, vintage INTEGER,variety TEXT,winery TEXT, url TEXT)''')


c.execute('''SELECT MAX(wine_id) from wines''')

TOTAL_DOCS=c.fetchone()[0]+1 
conn.commit()

#print(TOTAL_DOCS)


with open(path+"vocabulary_id.json") as f:
    vocabulary=json.load(f)

with open(path+"tf_idf.json") as f:
    tf_idf_dict=json.load(f)

with open(path+"vocabulary_database.json") as f:
    vocab_database=json.load(f)

# Processing the query

ps = PorterStemmer()
stop_words = list(stopwords.words('english'))
tokenizer = RegexpTokenizer(r'\w+')

query="dom perignon citrus sweet young"

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def results_from_query(query):#,vocab_database,vocabulary,TOTAL_DOCS,tf_idf_dict,NB_RESULTS,path_to_db):

    #TODO some spelling check of the query beforehand ? add vocabulary (both) to the spelling check dictionary possible ?
    sentence = query.lower()
    tokens = tokenizer.tokenize(sentence)
    filtered_sentence = [w for w in tokens if not w in stop_words] 

    stemmed_query=[]
    not_in_voc=[] #XXX TODO process them by checking if they are winery, region, country, vintage, type of wine etc ??
    #XXX And/Or later add filters for price, score

    for word in filtered_sentence:
        stem_w=ps.stem(word)

        in_database_list=[k for k, v in vocab_database.items() if word in v]

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
    #TODO make faster!!!!!!
    for query_w_id, count in query_dict.items():
        tf_q=count/size_query

        for doc,weight in tf_idf_dict[str(query_w_id)].items():
            similarity_list[int(doc)]+=tf_q*weight

    #TODO how to get the pages with no description of wine? How to get results if no word matches any description ???????

    #print("Calculated similarity for all with the terms.")

    relevant_doc_id=list(zip(*heapq.nlargest(NB_RESULTS, enumerate(similarity_list), key=itemgetter(1))))[0]
    #[1] is the similarity score

    #print(relevant_doc_id)

    #XXX can do above in C++ faster ??


    conn = sqlite3.connect(path_to_db)
    c = conn.cursor()
    # (wine_id INTEGER PRIMARY KEY,country TEXT,description TEXT,name TEXT,score INTEGER,price REAL,province TEXT,region_1 TEXT,region_2 TEXT, vintage INTEGER,variety TEXT,winery TEXT, url TEXT)''')


    sql="select * from wines where wine_id in ({seq})".format(
    seq=','.join(['?']*len(relevant_doc_id)))

    c.execute(sql, relevant_doc_id)

    results=c.fetchall() 
    conn.commit()    
    conn.close()

    r = [dict((c.description[i][0], value) \
        for i, value in enumerate(row)) for row in results]
    
    for result in r:
        # print(result)
        for key,value in result.items():
            try:
                result[key]=value.replace("&amp;","&")
            except Exception:
                continue


    return r
    


if __name__ == "__main__":
    results_from_query(query)#,vocab_database,vocabulary,TOTAL_DOCS,tf_idf_dict,NB_RESULTS,path+'wines.db')

    
