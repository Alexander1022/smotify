from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, send_from_directory
import logging 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from functools import wraps
import os, hashlib
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length
import random
import string

UPLOAD_FOLDER = './uploads'
ONLY_ALLOWED = {'mp3', 'wav', 'ogg', 'wma'}
GENRES = {'rock', 'pop', 'hiphop', 'house', 'trap', 'chill', 'popfolk', 'metal', 'classical', 'kpop', 'polka', 'reggae', 'punk', 'funk', 'country'}
app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

def generate_random_filename():
    symbols = string.ascii_lowercase + string.ascii_uppercase + string.digits
    res = ''.join(random.choice(symbols) for i in range(25))
    res = res + '.mp3'
    return res

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ONLY_ALLOWED

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(30))

class song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    artist_name = db.Column(db.String(50))
    genre = db.Column(db.String(20))
    filename = db.Column(db.String(80))
    
class UploadForm(FlaskForm):
    SongName = StringField('SongName', validators=[DataRequired(), Length(min=1, max=20)])
    Artist = StringField('Artist', validators=[DataRequired(), Length(min=1, max=50)])
    Genre = StringField('Genre', validators=[DataRequired(), Length(min=1, max=30)])
    
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap
	

@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
@is_logged_in
def upload():

    form = UploadForm()

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Please select file!')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file!')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            
            filename = generate_random_filename()
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            File = song(name = form.SongName.data, artist_name = form.Artist.data, genre = form.Genre.data, filename = filename)
            db.session.add(File)
            db.session.commit()

            return redirect(url_for('songs'))
        else:
            flash('.mp3, .wav, .ogg and .wma are only supported')

    return render_template('upload.html', form = form)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        
        login = user.query.filter_by(username = uname, password = hash_password(passw)).first()

        if login is not None:
            session['logged_in'] = True
            session['username'] = uname
            return redirect(url_for("index"))

        elif login is None:
            flash("Incorrect username or password! Please try again.")
        
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        register = user(username = uname, email = mail, password = hash_password(passw))
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/songs', methods=['GET', 'POST'])
def songs():
    q = request.args.get('q')
    
    if q:
        songs = song.query.filter(song.name.contains(q) | song.artist_name.contains(q) | song.genre.contains(q))
    else:
        songs = song.query.all()
        random.shuffle(songs)
        songs = songs[:20]
        
    return render_template('songs.html', songs = songs)

if __name__ == "__main__":
    db.create_all()
    app.secret_key='melodicapp00'
    logging.debug("The server is started. Enjoy using Melodic!")
    app.run(debug=True)
