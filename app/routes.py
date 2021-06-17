from flask import render_template, flash, redirect, url_for, session, logging, request, send_from_directory, abort
from flask_wtf import form
from app.models import user, song, playlist
from app.forms import UploadForm, MakePlaylistForm
from app.utils import *
from app import app, db, UPLOAD_FOLDER
import os
from fuzzywuzzy import fuzz
from tinytag import TinyTag
from flask_login import login_user, current_user, logout_user, login_required

#from werkzeug.utils import secure_filename

@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
@login_required
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
            File = song(name = form.SongName.data, artist_name = form.Artist.data, genre = form.Genre.data, filename = filename, uploader = current_user)
            
            db.session.add(File)
            db.session.commit()

            # [DEBUG] The line bellow is for metadata - name and artist of the song.
            print("Metadata: " + str(tag.title) + " - " + str(tag.artist))

            return redirect(url_for('songs'))
        else:
            flash('.mp3, .wav, .ogg and .wma are only supported')

    return render_template('upload.html', form = form)
    
@app.route('/my_songs')
@login_required
def my_songs():
    my_songs = song.query.filter_by(uploader = current_user)
    return render_template('my_songs.html', my_songs = my_songs)
    
@app.route('/my_songs/edit/<int:song_id>', methods=["GET", "POST"])
@login_required
def edit_song(song_id):
    s = song.query.get_or_404(song_id)
    if s.uploader != current_user:
        abort(403)
        
    form = UploadForm()
    if request.method == 'POST':
        s.name = form.SongName.data
        s.artist_name = form.Artist.data
        s.genre = form.Genre.data
        db.session.commit()
        flash('Your song has been updated!', 'success')
        return redirect(url_for('my_songs'))
    elif request.method == 'GET':
        form.SongName.data = s.name
        form.Artist.data = s.artist_name
        form.Genre.data = s.genre
    
    return render_template('edit_song.html', form = form, s = s)
    
@app.route('/my_songs/delete/<int:song_id>', methods=["GET", "POST"])
@login_required
def delete_song(song_id):
    s = song.query.get_or_404(song_id)
    if s.uploader != current_user:
        abort(403)
    db.session.delete(s)
    db.session.commit()
    flash('Your song has been deleted!', 'success')
    return redirect(url_for('my_songs'))
    

@app.route('/uploads/static/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/login",methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        
        login = user.query.filter_by(username = uname, password = hash_password(passw)).first()

        if login is not None:
            #session['logged_in'] = True
            #session['username'] = uname
            login_user(login)
            return redirect(url_for("index"))

        elif login is None:
            flash("Incorrect username or password! Please try again.")
        
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

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
def logout():
    #session.clear()
    logout_user()
    return redirect(url_for('index'))

@app.route('/songs', methods=['GET', 'POST'])
def songs():
    page = request.args.get('page', 1, type=int)
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
        songs = song.query.paginate(page = page, per_page = 10) # пагинация
        random.shuffle(songs.items)
        #songs = songs[:20]
        #songs = songs.paginate(page = page, per_page = 20)

    return render_template('songs.html', songs = songs)

@app.route('/forYou', methods=['GET', 'POST'])
def forYou():
    forYouSongs = song.query.all()
    a = 0
    random.shuffle(forYouSongs)
    return render_template('forYou.html', songs = forYouSongs, a = a)
    
@app.route('/make_playlist', methods = ['GET', 'POST'])
@login_required
def make_playlist():
    if request.method == "POST":
        pl_name = request.form["playlist"]
        pl = playlist(playlist_name = pl_name)
        db.session.add(pl)
        db.session.commit()
        return redirect(url_for("forYou"))

    return render_template('make_playlist.html', songs = songs, form = form)
    
@app.route('/playlists')
def playlists():
    playlists = playlist.query.all()
    return render_template('playlists.html', playlists = playlists)
    
@app.route('/playlists/<int:pl_id>')
def pl(pl_id):
    pl = playlist.query.get_or_404(pl_id)
    songs = pl.songs_in_playlist
    return render_template('playlist.html', pl = pl, songs = songs)
    
    
