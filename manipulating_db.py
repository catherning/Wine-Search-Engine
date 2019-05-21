import sqlite3
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from collections import Counter
import json
from operator import itemgetter
from itertools import groupby

path="D:/Documents/Tsinghua/WIR-WineSearch/"

conn = sqlite3.connect(path+'wines.db')
c = conn.cursor()
# (wine_id INTEGER PRIMARY KEY,country TEXT,description TEXT,name TEXT,score INTEGER,price REAL,province TEXT,region_1 TEXT,region_2 TEXT, vintage INTEGER,variety TEXT,winery TEXT, url TEXT)''')


c.execute('''SELECT MAX(wine_id) from wines''')

init_nb_wines=c.fetchone()[0]+1 
conn.commit()

print(init_nb_wines)


#TODO add wine name/ winery, country, region to stemmed vocab and indexing ? or useless as are already in database in specific columns?

# Selecting stemmed keywords and calculating occurences
c.execute('''SELECT wine_id,description from wines''')
data=c.fetchall()
conn.commit()
conn.close()

ps = PorterStemmer()
stop_words = list(stopwords.words('english')) 
tokenizer = RegexpTokenizer(r'\w+')

vocabulary={}
inverted_index_dict={}
w_id=0

# Stemming the words (removed the stopwords) for the description of each wine from each website of the database
#dict_index={}
tuple_index=[]

for i,row in enumerate(data):
    sentence = row[1].lower()
    tokens = tokenizer.tokenize(sentence)
    filtered_sentence = [w for w in tokens if not w in stop_words] 

    stemmed_sent=[]
    for word in filtered_sentence:
        stem_w=ps.stem(word)

        if stem_w not in vocabulary:
            vocabulary[stem_w]=w_id
            inverted_index_dict[w_id]={"stemmed_word":stem_w}

            stemmed_sent.append(w_id)

            w_id+=1
        else:
            stemmed_sent.append(vocabulary[stem_w])        

    sent_dict=Counter(stemmed_sent)
    for sent_w_id, count in sent_dict.items():
        tuple_index.append((sent_w_id,int(row[0]),count))

    #dict_index[int(row[0])]=sent_dict

print("Processed all rows. Creating the inverted index.")

# Inverted index
tuple_index.sort(key=itemgetter(0))


# Creating postings
postings={}
for w_id,doc_id,count in tuple_index:
    if w_id in postings:
        postings[w_id][doc_id]=count
    else:
        postings[w_id]={doc_id:count}


# Completing inverted_index_dict
doc_count=Counter(elem[0] for elem in tuple_index)
for w_id in inverted_index_dict:
    inverted_index_dict[w_id]["doc_nb"]=doc_count[w_id]

for w_id, group in groupby(tuple_index, lambda x: x[0]):
    total_count=0
    for tuple_ in group:
        total_count+=tuple_[2]
    inverted_index_dict[w_id]["total_count"]=total_count


print("Created the inverted index (dictionary and postings). Saving it and the vocabulary.")

# Variables to keep: inverted_index_dict, postings, vocabulary
# Eventually dict_index which is reverse inverted_index_dict ?

with open(path+'inverted_index.json', 'w') as fp:
    json.dump(inverted_index_dict, fp, sort_keys=True, indent=4)

with open(path+'postings.json', 'w') as fp:
    json.dump(postings, fp, sort_keys=True, indent=4)

with open(path+'vocabulary_id.json', 'w') as fp:
    json.dump(vocabulary, fp, sort_keys=True, indent=4)

