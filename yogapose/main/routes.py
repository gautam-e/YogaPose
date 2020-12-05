from flask import render_template, request, Blueprint, url_for, flash, redirect
from yogapose.models import Post
from yogapose.posts.forms import PostPoseForm
from yogapose.users.utils import save_picture
from flask_login import current_user
from yogapose import db

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home", methods=['GET', 'POST'])
def home():
    form = PostPoseForm()
    if form.validate_on_submit():
        picture_file = save_picture(form.pose_pic.data, foldername='posted_pics', output_size=(300,300) )
        post = Post(pose_pic=picture_file, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your pose has been posted!', 'success')
        #return render_template('user_posts.html', user=user, posts=posts, form=form)
    page = request.args.get('page', 1, type=int)
    return render_template('home.html', form=form)


@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/privacy_policy")
def privacy_policy():
    return render_template('privacy_policy.html', title='Privacy Policy')

@main.route("/terms_of_service")
def terms_of_service():
    return render_template('terms_of_service.html', title='Terms of Service')

@main.route("/impressum")
def impressum():
    return render_template('impressum.html', title='Contact and Legal Notice')