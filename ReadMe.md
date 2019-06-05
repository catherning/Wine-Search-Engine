# Order for running the files:
1. database_wine.py
2. scrapy_spider
3. iwinedb_json_to_db.py
4. indexing.py
5. ranking.py
6. query.py in front-end

# Needed for server
- wines.db
- tf_idf.json
- vocabulary_id.json

# DB files
To put online:
- inverted_index.json -> to csv -> to db
- postings.json ? -> 
- tf_idf.json  
Could put postings and tf_idf in same database ? id (might be useless), word, doc, count, tf_idf
- vocabulary_database.json


To keep locally
- vocabulary_id (not used ?) -> to csv -> to db (word,id) but not necessary
- wines_iwinedb.json
-> directly add to pipeline of crawler in DB if possible ? 
No! Might be much slower bc for now, just 2 sec when put everything at once != one by one