from pathlib import Path
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from yogapose import mail

def save_picture(form_picture, foldername='profile_pics', output_size=(125,125)):
    """ Resize and save picture"""
    random_hex = secrets.token_hex(8)
    f_ext = str(Path(form_picture.filename).suffix)
    picture_fn = random_hex + f_ext
    picture_path = Path(current_app.root_path).joinpath('static').joinpath(foldername).joinpath(picture_fn)

    output_size = output_size
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='admin@yogapose.app', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
