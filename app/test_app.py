#! /usr/bin/env python

from flask.ext.bootstrap import Bootstrap
from flask import Flask, session, request, render_template, flash, redirect, url_for, g
import model
from model import session as db_session, User, Rating, Movie
import os

app = Flask(__name__)
# heroku = Heroku(app)
# SECRET_KEY = "fish"z
app.config.from_object(__name__)

@app.teardown_request
def shutdown_session(exception = None):
    db_session.remove()

@app.before_request
def load_user_id():
    g.user_id = session.get('user_indx')

@app.route("/")
def main_page():
	return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/users")
def users():
    return render_template('users.html')

@app.route("/data")
def data():
    return render_template('data.html')

@app.route("/graphs")
def graphs():
    return render_template('graphs.html')

@app.route("/trial_experience")
def trial_experience():
    if g.user_id:
        return redirect(url_for("display_profile"))
    return render_template("trial_experience.html")


@app.route("/login", methods=["POST"])
def login():
    email = request.form['email']
    password = request.form['password']

    try:
        user = db_session.query(User).filter_by(email=email, password=password).one()
    except:
        flash("Invalid username or password", "error")
        return redirect(url_for("trial_experience"))

    session['user_indx'] = user.indx
    return redirect(url_for("display_profile"))

@app.route("/register", methods=["POST"])
def register():
    email = request.form['email']
    password = request.form['password']
    name = request.form['name']
    existing = db_session.query(User).filter_by(email=email).first()
    if existing:
        flash("Email already in use", "error")
        return redirect(url_for("trial_experience"))

    u = User(indx = 100000, email=email, password=password, name=name) #how to add indexes?
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    session['user_indx'] = u.indx 
    return redirect(url_for("display_profile"))

@app.route("/profile", methods=["GET"])
def display_profile():
    return render_template("profile.html")

@app.route("/search", methods=["GET"])
def display_profile():
    return render_template("profile.html")

@app.route("/search", methods=["POST"])
def search():
    query = request.form['query']
    movies = db_session.query(Movie).\
            filter(Movie.title.ilike("%" + query + "%")).\
            limit(20).all()

    return render_template("results.html", movies=movies)

@app.route("/movie/<int:indx>", methods=["GET"])
def view_movie(indx):
    movie = db_session.query(Movie).get(indx)
    ratings = movie.ratings #now it breaks here
    rating_nums = []
    user_rating = None
    for r in ratings:
        if r.user_indx == session['user_indx']:
            user_rating = r
        rating_nums.append(r.rating)
    avg_rating = float(sum(rating_nums))/len(rating_nums)

    prediction = None
    if not user_rating:
        user = db_session.query(User).get(g.user_indx) 
        prediction = user.predict_rating(movie)
        print prediction
    
    return render_template("movie.html", movie=movie, 
            average=avg_rating, user_rating=user_rating,
            prediction = prediction)

@app.route("/rate/<int:id>", methods=["POST"])
def rate_movie(id):
    rating_number = int(request.form['rating'])
    user_id = session['user_id']
    rating = db_session.query(Rating).filter_by(user_id=user_id, movie_id=id).first()

    if not rating:
        flash("Rating added", "success")
        rating = Rating(user_id=user_id, movie_id=id)
        db_session.add(rating)
    else:
        flash("Rating updated", "success")

    rating.rating = rating_number
    db_session.commit()

    return redirect(url_for("view_movie", id=id))

@app.route("/my_ratings")
def my_ratings():
    if not g.user_indx:
        flash("Please log in", "warning")
        return redirect(url_for("index"))

    ratings = db_session.query(Rating).filter_by(user_id=g.user_indx).all()
    return render_template("my_ratings.html", ratings=ratings)

@app.route("/logout")
def logout():
    del session['user_indx']
    return redirect(url_for("trial_experience"))

app.secret_key = '\xd0u\xf2g\xbc\xc5\x07e\xc6wz\x03\x05\xe2\xcd[d\xac\xd0\xe4\x8e\xe2\xb6\x82'

if __name__ == '__main__':
	db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
	if not db_uri:
		db_uri = "sqlite:///ratings.db"
	# model.connect(db_uri)
	Bootstrap(app)
	app.run(debug=True, port=int(os.environ.get("PORT", 5000)), host="0.0.0.0")

