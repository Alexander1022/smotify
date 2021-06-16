import app
from app import app
from app import db
from app import utils
from app import routes
from flask import render_template, flash, redirect, url_for, session, logging, request, send_from_directory
from app.models import user, song, playlist
from app.forms import UploadForm, MakePlaylistForm
from app.utils import *
from app import app, db, UPLOAD_FOLDER
import os
from fuzzywuzzy import fuzz
from tinytag import TinyTag
import logging


if __name__ == "__main__":
    db.create_all()
    app.secret_key='melodicapp00'
    logging.debug("The server is started. Enjoy using Melodic!")
    app.run(debug=True)
