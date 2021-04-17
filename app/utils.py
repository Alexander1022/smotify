import random
import string
import hashlib
from functools import wraps
from flask import session
from app import ONLY_ALLOWED

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
               
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

