from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from collections import Counter
from operator import itemgetter
import heapq
import json
import sqlite3
from spellchecker import SpellChecker

NB_RESULTS=10
path="D:/Documents/Tsinghua/WIR-WineSearch/"

path_to_db=path+'wines.db'

conn = sqlite3.connect(path_to_db)
c = conn.cursor()
c.execute('''SELECT MAX(wine_id) from wines''')

TOTAL_DOCS=c.fetchone()[0]+1 
conn.commit()

with open(path+"vocabulary_id.json") as f:
    vocabulary=json.load(f)

with open(path+"tf_idf.json") as f:
    tf_idf_dict=json.load(f)

# Processing the query

ps = PorterStemmer()
stop_words = list(stopwords.words('english'))
tokenizer = RegexpTokenizer(r'\w+')
spell = SpellChecker(local_dictionary=path+'spellcheck_dict.json')

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def results_from_query(query,score=None,price=None):
    """
    returns:
        - results
        - FLAG_CONDITION: 0 if normal, 1 if the conditions give no relevant results, 
    """

    print(query)

    sentence = query.lower()
    tokens = tokenizer.tokenize(sentence)
    filtered_sentence = [w for w in tokens if not w in stop_words] 
    misspelled = spell.unknown (filtered_sentence)
    corrected_query=[]
    
    stemmed_query=[]

    for word in filtered_sentence:
        correct_spell= spell.correction(word)
        stem_w=ps.stem(correct_spell)

        if stem_w in vocabulary:
            stemmed_query.append(vocabulary[stem_w])

        corrected_query.append(correct_spell)
    
    if filtered_sentence==corrected_query:
        FLAG_CORRECT=True
    else:
        FLAG_CORRECT=False
    
    corrected_query = ' '.join(str(e) for e in corrected_query)

    # ============================ Finding the relevant results =================================

    #TODO check highest price, highest score

    conn = sqlite3.connect(path_to_db)
    c = conn.cursor()

    full_set=set([i for i in range(TOTAL_DOCS)])

    #Selecting wine id of score higher than score
    if score!='None' and score!=None:
        sql="SELECT wine_id from wines where score>(?)"
        c.execute(sql, (int(score),))

        wine_id_score=c.fetchall()
        conn.commit() 
        wine_id_score=set([el[0] for el in wine_id_score])
        
    else:
        wine_id_score=full_set

    # Selecting wine id of price between lowest price and highest price
    if price==[None,None]:
        wine_id_price=full_set
    else:
        if price[0]!=None and price[1]==None:
            sql="SELECT wine_id from wines where price>(?)"
            c.execute(sql, (float(price[0]),))
        elif price[0]==None and price[1]!=None:
            sql="SELECT wine_id from wines where price<(?)"
            c.execute(sql, (float(price[1]),))
        elif price[0]!=None and price[1]!=None:
            price.sort()
            sql="SELECT wine_id from wines where price>=(?) and price<=(?)"
            c.execute(sql, (float(price[0]),float(price[1])))

        wine_id_price=c.fetchall()
        conn.commit()
        wine_id_price=set([el[0] for el in wine_id_price])

    valid_condition_wine_id=wine_id_price.intersection(wine_id_score)


    def similarity_all():
        # Get similarity with docs
        query_dict=Counter(stemmed_query)
        size_query=len(stemmed_query)

        similarity_list=[0.]*TOTAL_DOCS
        for query_w_id, count in query_dict.items():
            tf_q=count/size_query

            for doc,weight in tf_idf_dict[str(query_w_id)].items():
                similarity_list[int(doc)]+=tf_q*weight
        
        return similarity_list

    if len(valid_condition_wine_id)==0:
        FLAG_CONDITION=1
        similarity_list=similarity_all()

    elif len(valid_condition_wine_id)==TOTAL_DOCS:
        FLAG_CONDITION=0
        similarity_list=similarity_all()
        
    else:
        # Get similarity with docs
        query_dict=Counter(stemmed_query)
        size_query=len(stemmed_query)

        similarity_list=[0.]*TOTAL_DOCS
        count_in_valid_cond=0

        for query_w_id, count in query_dict.items():
            tf_q=count/size_query

            for doc,weight in tf_idf_dict[str(query_w_id)].items():
                if int(doc) in valid_condition_wine_id:
                    similarity_list[int(doc)]+=tf_q*weight
                    count_in_valid_cond+=1

        # Goes back to case 1 if the words in the query were not present in enough documents
        if count_in_valid_cond< NB_RESULTS*size_query/2: # nb results bc we want the word to be in the 10 results, size_query: for all words, /2 bc not for all.. XXX Empirical
            similarity_list=similarity_all()
            FLAG_CONDITION=1
        else:        
            FLAG_CONDITION=0

    #TODO add relevance with price and score ? rel = tf_idf * score/100 * 1/log(price) for NB_results * 5, re-do  ranking
    relevant_doc=list(zip(*heapq.nlargest(NB_RESULTS, enumerate(similarity_list), key=itemgetter(1))))
    relevant_doc_id=relevant_doc[0]
    relevance_score=relevant_doc[1]

    sql="SELECT * from wines where wine_id in ({seq})".format(
        seq=','.join(['?']*len(relevant_doc_id)))


    c.execute(sql, relevant_doc_id)

    results=c.fetchall() 
    conn.commit()    
    conn.close()

    # Reorders by score in the end
    results_list = [dict((c.description[i][0], value) for i, value in enumerate(row)) for row in results]

    for wine in results_list:
        for key,value in wine.items():
            try:
                wine[key]=value.replace("&amp;","&")
            except Exception:
                continue
    
    results_list=sorted(results_list, key=itemgetter('score'), reverse=True)

    return results_list,FLAG_CONDITION,corrected_query,FLAG_CORRECT
    
    

if __name__ == "__main__":
    query="2010 château latour complex"
    results_from_query(query,price=[None,50]) 
