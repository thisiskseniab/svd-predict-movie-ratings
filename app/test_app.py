#! /usr/bin/env python

from flask.ext.bootstrap import Bootstrap
from flask import Flask, session, request, render_template, flash, redirect, url_for, g
import model
from model import session as db_session, User, Rating, Movie, Prediction
import os

app = Flask(__name__)
# heroku = Heroku(app)
# SECRET_KEY = "fish"z
app.config.from_object(__name__)

# fix unicode in place
def fix_unicode_movie(m):
    m.title = m.title.decode('UTF-8')

@app.teardown_request
def shutdown_session(exception = None):
    db_session.remove()

@app.before_request
def load_user_indx():
    g.user_indx = session.get('user_indx')

@app.route("/")
def main_page():
    if g.user_indx:
        return redirect(url_for("display_profile"))
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    user_indx = request.form['user_indx']
    try:
        user = db_session.query(User).filter_by(indx=user_indx).one()
    except Exception, e:
        print str(e)
        flash("Invalid user id", "error")
        return redirect(url_for("main_page"))

    session['user_indx'] = user.indx
    return redirect(url_for("display_profile"))

@app.route("/profile", methods=["GET"])
def display_profile():
    ratings = db_session.query(User).filter_by(indx=g.user_indx).one().rating
    
    ratings = sorted(ratings, key=lambda ratings:ratings.rating, reverse=True)[:10]
    for rat in ratings:
        fix_unicode_movie(rat.movie)
    recommendations = db_session.query(User).filter_by(indx=g.user_indx).one().prediction
    max_score = max(recommendations, key=lambda r: r.rating_score).rating_score
    for r in recommendations:
        fix_unicode_movie(r.movie)

    recommendations = filter(lambda r: r.human_score > 1, recommendations)
    recommendations = sorted(recommendations, key=lambda r: r.human_score, reverse=True)[:10]

    return render_template("profile.html", user_indx=g.user_indx, ratings=ratings, recommendations=recommendations)

@app.route("/search", methods=["GET"])
def movie_search():
    return render_template("profile.html")

@app.route("/search", methods=["POST"])
def search():
    query = request.form['query']
    movies = db_session.query(Movie).\
            filter(Movie.title.ilike("%" + query + "%")).\
            limit(20).all()
    for movie in movies:
        print movie.indx        
    return render_template("results.html", movies=movies)

@app.route("/overview", methods=["GET"])
def overview():
    #1
    ratings_1 = db_session.query(User).filter_by(indx=556).one().rating
    ratings_1 = sorted(ratings_1, key=lambda ratings:ratings.rating, reverse=True)[:5]
    for rat_1 in ratings_1:
        fix_unicode_movie(rat_1.movie)
    recommendations_1 = db_session.query(User).filter_by(indx=556).one().prediction
    max_score_1 = max(recommendations_1, key=lambda r: r.rating_score).rating_score
    for r_1 in recommendations_1:
        fix_unicode_movie(r_1.movie)
    recommendations_1 = sorted(recommendations_1, key=lambda r: r_1.human_score, reverse=True)[:5]
    #2
    ratings_2 = db_session.query(User).filter_by(indx=5774).one().rating
    ratings_2 = sorted(ratings_2, key=lambda ratings:ratings.rating, reverse=True)[:5]
    for rat_2 in ratings_2:
        fix_unicode_movie(rat_2.movie)  
    recommendations_2 = db_session.query(User).filter_by(indx=5774).one().prediction
    max_score_2 = max(recommendations_2, key=lambda r: r.rating_score).rating_score
    for r_2 in recommendations_2:
        fix_unicode_movie(r_2.movie)
    recommendations_2 = sorted(recommendations_2, key=lambda r: r_2.human_score, reverse=True)[:5]
    #3
    ratings_3 = db_session.query(User).filter_by(indx=10216).one().rating
    ratings_3 = sorted(ratings_3, key=lambda ratings:ratings.rating, reverse=True)[:5]
    for rat_3 in ratings_3:
        print rat_3.movie.title
        fix_unicode_movie(rat_3.movie)   
    recommendations_3 = db_session.query(User).filter_by(indx=10216).one().prediction
    max_score_3 = max(recommendations_3, key=lambda r: r.rating_score).rating_score
    for r_3 in recommendations_3:
        fix_unicode_movie(r_3.movie)
    recommendations_3 = sorted(recommendations_3, key=lambda r: r_3.human_score, reverse=True)[:5]
    return render_template('overview.html', ratings_1=ratings_1, recommendations_1=recommendations_1,\
                ratings_2=ratings_2, recommendations_2=recommendations_2, ratings_3=ratings_3, recommendations_3=recommendations_3)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/svd")
def svd():
    return render_template('svd_page.html')

@app.route("/lazy-eval")
def lazy_eval():
    return render_template('lazy-eval.html')

@app.route("/challenges")
def challenges():
    return render_template('challenges.html')

@app.route("/data")
def data():
    return render_template('data.html')

@app.route("/logout")
def logout():
    del session['user_indx']
    return redirect(url_for("main_page"))

app.secret_key = '\xd0u\xf2g\xbc\xc5\x07e\xc6wz\x03\x05\xe2\xcd[d\xac\xd0\xe4\x8e\xe2\xb6\x82'

if __name__ == '__main__':
	app.run(debug=True, port=int(os.environ.get("PORT", 5000)), host="0.0.0.0")

