from flask import render_template
from app import app
from app.wine_query.query import results_from_query
from app.search_box import SearchBox

@app.route('/')
@app.route('/index')
def login():
    form = SearchBox()
    return render_template('index.html', title='Search', form=form)


@app.route('/results')
def index():
    user_query={"string":"dom perignon sweet citrus"}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

    results = results_from_query(user_query["string"])

    return render_template('results.html', title='Results', query=user_query, wines=results)