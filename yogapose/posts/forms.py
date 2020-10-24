from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired

class PostPoseForm(FlaskForm):
    pose_pic = FileField(label='Select an image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!'), DataRequired()])
    submit = SubmitField('Upload and score')

class UpdatePostPoseForm(FlaskForm):
    pose_name = StringField('Pose name', validators=[DataRequired()])
    submit = SubmitField('Update')
