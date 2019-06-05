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
    return render_template('index.html', title='WineSearch', form=search,cur_page='home')


#@app.route('/results')
def search_query(query,first_time=True):
    search2 = SearchBox()
    if search2.validate_on_submit() and first_time:
        # flash('Query {}'.format(
        #     search.query.data))
        return search_query(search2,first_time=False)

    search_string = query.data['query']
    score=query.data['score']
    price=[query.data['price_l'],query.data['price_h']]
    results,FLAG_CONDITION,corrected_query,FLAG_CORRECT = results_from_query(search_string,score=score,price=price)

    return render_template('results.html', title='WineSearch', query=corrected_query, wines=results, form=search2,cur_page='results',score=score,flag_cond=FLAG_CONDITION,flag_correct=FLAG_CORRECT)


@app.route('/about')
def about_page():
    return render_template('about.html', title='WineSearch',cur_page='about')