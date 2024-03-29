from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired

class PostPoseForm(FlaskForm):
    render_kw={'accept':"image/jpg,image/jpeg"}
    pose_pic = FileField(label='Select an image', validators=[FileAllowed(['jpg', 'jpeg'], 'JPGs only!'), DataRequired()], render_kw=render_kw)
    submit = SubmitField(label='Upload and Score')

class UpdatePostPoseForm(FlaskForm):
    pose_name = StringField('Pose name', validators=[DataRequired()])
    submit = SubmitField('Update')
