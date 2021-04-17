from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class UploadForm(FlaskForm):
    SongName = StringField('SongName', validators=[DataRequired(), Length(min=1, max=20)])
    Artist = StringField('Artist', validators=[DataRequired(), Length(min=1, max=50)])
    Genre = StringField('Genre', validators=[DataRequired(), Length(min=1, max=30)])
    
class MakePlaylistForm(FlaskForm):
    PlaylistName = StringField('Playlist Name', validators=[DataRequired(), Length(min=1)])
