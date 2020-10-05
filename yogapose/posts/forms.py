from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired

class PostPoseForm(FlaskForm):
    pose_name = StringField('Title', validators=[DataRequired()])
    pose_pic = FileField(label='Post Your Pose', validators=[FileAllowed(['jpg', 'png', 'jpeg']), DataRequired()])
    submit = SubmitField('Post')

class UpdatePostPoseForm(FlaskForm):
    pose_name = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Post')
