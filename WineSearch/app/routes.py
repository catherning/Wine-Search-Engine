from flask import render_template, flash, redirect, url_for
from app import app
from app.wine_query.query import results_from_query
from app.search_box import SearchBox

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    search = SearchBox()
    if search.validate_on_submit():
        # flash('Query {}'.format(
        #     search.query.data))
        return search_query(search)
    return render_template('index.html', title='WineSearch', form=search)


@app.route('/results')
def search_query(query):
    search2 = SearchBox()
    if search2.validate_on_submit():
        # flash('Query {}'.format(
        #     search.query.data))
        return search_query(search2)

    search_string = query.data['query']

    results = results_from_query(search_string)

    return render_template('results.html', title='Results', query=search_string, wines=results, form=search2)


@app.route('/about')
def about_page():
    return render_template('about.html', title='About')