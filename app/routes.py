from flask import render_template, flash, redirect, url_for, session, logging, request, send_from_directory
from app.models import user, song, playlist
from app.forms import UploadForm, MakePlaylistForm
from app.utils import *
from app import app, db, UPLOAD_FOLDER
import os
from fuzzywuzzy import fuzz
from tinytag import TinyTag
from bs4 import BeautifulSoup

#from werkzeug.utils import secure_filename

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
            tag = TinyTag.get(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            title = tag.title
            artist = tag.artist
            File = song(name = form.SongName.data, artist_name = form.Artist.data, genre = form.Genre.data, filename = filename)
            db.session.add(File)
            db.session.commit()

            # [DEBUG] The line bellow is for metadata - name and artist of the song.
            print("Metadata: " + str(tag.title) + " - " + str(tag.artist))

            return redirect(url_for('songs'))
        else:
            flash('.mp3, .wav, .ogg and .wma are only supported')

    return render_template('upload.html', form = form)

@app.route('/uploads/static/<filename>')
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
        records = song.query.all()
        songs = []
        
        for s in records:
            # търси в името, изпълнителя и жанра и, ако е над 60% се вкарват в списък, който накрая излиза на страницата 
            name = fuzz.token_sort_ratio(q, s.name)
            artist = fuzz.token_sort_ratio(q, s.artist_name)
            genre = fuzz.token_sort_ratio(q, s.genre)
            
            if name > 60 or artist > 60 or genre > 60:
                if s not in songs: 
                    songs.append(s)

    else:
        songs = song.query.all()
        random.shuffle(songs)
        songs = songs[:20]
 
    return render_template('songs.html', songs = songs)
    
@app.route('/make_playlist', methods = ['GET', 'POST'])
@is_logged_in
def make_playlist():

    form = MakePlaylistForm() 

    q = request.args.get('q')
    
    if q:
        songs = song.query.filter(song.name.contains(q) | song.artist_name.contains(q) | song.genre.contains(q))
    else:
        songs = []

    return render_template('make_playlist.html', songs = songs, form = form)
