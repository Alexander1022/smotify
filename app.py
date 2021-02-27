from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import os, hashlib
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ONLY_ALLOWED = {'mp3', 'wav', 'ogg', 'wma'}
GENRES = {'rock', 'pop', 'hiphop', 'house', 'trap', 'chill', 'popfolk', 'metal', 'classical', 'kpop', 'polka', 'reggae', 'punk', 'funk', 'country'}
app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

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

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Please select file!')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file!')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            File = song(name = filename, artist_name = "Artist", genre = "genre")
            db.session.add(File)
            db.session.commit()

            return redirect(url_for('uploaded_file', filename = filename))
        else:
            flash('.mp3, .wav, .ogg and .wma are only supported')

    return render_template('upload.html')

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

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/songs', methods=['GET', 'POST'])
def songs():

    result = 0

    if result > 0:
        return render_template('songs.html', songs = songs)

    elif result <= 0 :
        return render_template('songs.html', error = "There are not any songs right now :(")

if __name__ == "__main__":
    db.create_all()
    app.secret_key='spotify'
    app.run(debug=True)