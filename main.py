
from flask import Flask, request,json,render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/movies.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToWatch(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    genre = db.Column(db.String(400), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno}- {self.title} - {self.genre} - {self.date_created}"


@app.route('/')
def home():
    data = {'showall': '/show',
            'addmovie': '/addmovie',
            'filtermovie': '/filter/<title you want to search>',
            'updatemovie': '/update/<sno of movie>',
            'deletemovie': '/delete/<sno of movie>'}
    return render_template('index.html', data= data)

@app.route('/show')
def show_movies():
    movies = ToWatch.query.all()
    li_movies = []
    for movie in movies:
        data = {"id": movie.sno, "title": movie.title, "genre": movie.genre,
                "date_added": movie.date_created}
        li_movies.append(data)
    if len(li_movies) == 0:
        return "Empty List. Please add some movies to view."
    else:
        return json.jsonify({"Your movie list is: ": li_movies})
    # return {"movie": movies}

@app.route('/addmovie', methods=['POST'])
def add_movies():
    movie = ToWatch(title=request.json['title'], genre=request.json['genre'])
    db.session.add(movie)
    db.session.commit()
    return json.jsonify({"Successfully added movie no: ": movie.sno})


@app.route('/filter/<string:title>')
def filter_movie(title):
    movie = ToWatch.query.filter_by(title=title).first()
    if movie != None:
        data = {"id": movie.sno, "title": movie.title, "genre": movie.genre,
                "date_added": movie.date_created}
        return json.jsonify({'movie': data})
    else:
        return json.jsonify({"Movies found with this title": 0})


@app.route('/update/<int:sno>', methods= ['GET', 'PUT'])
def update_movie(sno):
    
    if request.method == "PUT":
        title=request.json['title']
        genre=request.json['genre']
        movie = ToWatch.query.filter_by(sno=sno).first()
        movie.title = json.dumps(title).strip('"')
        movie.genre = json.dumps(genre).strip('"')
        movie.date_created = datetime.now()
        # if len(title) != 0 and len(genre) != 0:
        db.session.add(movie)
        db.session.commit()
        # return redirect('/')
        data = {"id": movie.sno, "title": movie.title, "genre": movie.genre,
                "date_added": movie.date_created}
        return json.jsonify({'movie updated': data})
    else:
        return json.jsonify({"Movies updated": 0})


@app.route('/delete/<int:sno>', methods= ['GET','DELETE'])
def delete_movie(sno):
    movie = ToWatch.query.filter_by(sno=sno).first()
    if movie is None:
        return json.jsonify({"Movie": "not found"})
    db.session.delete(movie)
    db.session.commit()
    return json.jsonify({"Movies deleted": 1})

if __name__ == "__main__":
    app.run(debug=True)