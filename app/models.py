from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return user.query.get(int(user_id))

class user(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(30))
    songs = db.relationship('song', backref = 'uploader', lazy = True)

songs_playlists = db.Table('songs_playlists',
    db.Column('song_id', db.Integer, db.ForeignKey('song.id')),
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.playlist_id'))
)
class song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    artist_name = db.Column(db.String(50))
    genre = db.Column(db.String(20))
    filename = db.Column(db.String(80))
    connections = db.relationship('playlist', secondary = songs_playlists, backref = db.backref('songs_in_playlist', lazy='dynamic'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    

class playlist(db.Model):
    playlist_id = db.Column(db.Integer, primary_key=True)
    playlist_name = db.Column(db.String(20))
