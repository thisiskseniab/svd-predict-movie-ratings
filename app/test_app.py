#! /usr/bin/env python

from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap


app = Flask(__name__)
# heroku = Heroku(app)
# SECRET_KEY = "fish"
app.config.from_object(__name__)

@app.teardown_request
def shutdown_session(exception = None):
    db_session.remove()

@app.before_request
def load_user_id():
    g.user_id = session.get('user_id')

@app.route("/")
def main_page():
	return render_template('index.html')

@app.route("/trial_experience")
def trial_experience():
    if g.user_id:
        return redirect(url_for("display_search"))
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

    session['user_id'] = user.id
    return redirect(url_for("display_search"))

@app.route("/register", methods=["POST"])
def register():
    email = request.form['email']
    password = request.form['password']
    existing = db_session.query(User).filter_by(email=email).first()
    if existing:
        flash("Email already in use", "error")
        return redirect(url_for("trial_experience"))

    u = User(email=email, password=password)
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    session['user_id'] = u.id 
    return redirect(url_for("display_search"))

@app.route("/search", methods=["GET"])
def display_search():
    return render_template("search.html")

@app.route("/search", methods=["POST"])
def search():
    query = request.form['query']
    movies = db_session.query(Movie).\
            filter(Movie.title.ilike("%" + query + "%")).\
            limit(20).all()

    return render_template("results.html", movies=movies)

@app.route("/movie/<int:id>", methods=["GET"])
def view_movie(id):
    movie = db_session.query(Movie).get(id)
    ratings = movie.ratings
    rating_nums = []
    user_rating = None
    for r in ratings:
        if r.user_id == session['user_id']:
            user_rating = r
        rating_nums.append(r.rating)
    avg_rating = float(sum(rating_nums))/len(rating_nums)

    prediction = None
    if not user_rating:
        user = db_session.query(User).get(g.user_id) 
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
    if not g.user_id:
        flash("Please log in", "warning")
        return redirect(url_for("index"))

    ratings = db_session.query(Rating).filter_by(user_id=g.user_id).all()
    return render_template("my_ratings.html", ratings=ratings)

@app.route("/logout")
def logout():
    del session['user_id']
    return redirect(url_for("index"))

if __name__ == '__main__':
	db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
	if not db_uri:
		db_uri = "sqlite:///ratings.db"
	model.connect(db_uri)
	Bootstrap(app)
	app.run(debug=True, port=int(os.environ.get("PORT", 5000)), host="0.0.0.0")

