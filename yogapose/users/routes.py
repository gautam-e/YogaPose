from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app, abort
from flask_login import login_user, current_user, logout_user, login_required
from yogapose import db, bcrypt
from yogapose.models import User, Post
from yogapose.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from yogapose.posts.forms import PostPoseForm
from yogapose.users.utils import send_reset_email, predict_picture
from pathlib import Path

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.user_posts', username=current_user.username))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data.lower(), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('users.user_posts', username=user.username))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.user_posts', username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email_or_username.data.lower()).first() or \
            User.query.filter_by(username=form.email_or_username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            #so that user gets directed to last page he tried to access after logging in
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users.user_posts', username=current_user.username))
        else:
            flash('Login Unsuccessful. Please check your login credentials', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)

@users.route("/user/<string:username>", methods=['GET', 'POST'])
@login_required
def user_posts(username):
    if username != current_user.username: 
        abort(403)
    form = PostPoseForm()
    if form.validate_on_submit():
        picture_file, score, pose_name = predict_picture(form.pose_pic.data, foldername='posted_pics', output_size=(224,224) )
        post = Post(pose_pic=picture_file, pose_name=pose_name, pose_score=score, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your pose has been posted!', 'success')
#        return redirect(url_for('users.user_posts', username=username))

    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts_query = Post.query.filter_by(author=user)
    number_of_poses = len({post.pose_name for post in posts_query.all() if post.pose_name!= 'No pose'} )
    posts = posts_query\
            .order_by(Post.date_posted.desc())\
            .paginate(page=page, per_page=6)
    return render_template('user_posts.html', user=user, posts=posts, form=form, \
        number_of_poses=number_of_poses)

@users.route("/user/<string:username>/delete", methods=['POST'])
@login_required
def delete_user(username):
    if username != current_user.username: 
        abort(403)
    # delete all posts from user
    user_query = User.query.filter_by(username=username)
    user_posts_query = Post.query.filter_by(author=user_query.first_or_404())
    user_posts_list = user_posts_query.all()
    for user_post in user_posts_list:
        rem_file = Path(current_app.root_path).joinpath('static','posted_pics',user_post.pose_pic)
        if rem_file.is_file(): rem_file.unlink()
    user_posts_query.delete()
    # delete user from database
    user_query.delete()
    db.session.commit()
    flash('Your account has been deleted!', 'success')
    return redirect(url_for('main.home'))

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('users.user_posts', username=current_user.username))
    form = RequestResetForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('users.user_posts', username=current_user.username))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


    