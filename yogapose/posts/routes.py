from flask import (render_template, url_for, flash, redirect, request, 
                    abort, Blueprint, current_app)
from flask_login import (login_user, current_user, logout_user, 
                        login_required)
from yogapose import db
from yogapose.models import Post
from yogapose.posts.forms import PostPoseForm, UpdatePostPoseForm
from pathlib import Path

posts = Blueprint('posts', __name__)


@posts.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    return render_template('post.html', title=post.pose_name, post=post)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = UpdatePostPoseForm()
    if form.validate_on_submit():
        post.pose_name = form.pose_name.data
        db.session.commit()
        flash('Your pose has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.pose_name.data = post.pose_name
    return render_template('update_post.html', title='Update Post', 
                            form=form, post=post)

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    # Delete image file
    # Get path to image
    rem_file = Path(current_app.root_path).joinpath('static','posted_pics',post.pose_pic)
    # Check if file exists and NOT EQUAL TO 'default.jpg" then delete
    if rem_file.is_file():
        rem_file.unlink()
    # Delete post from database
    db.session.delete(post)
    db.session.commit()
    
    flash('Your pose has been deleted!', 'success')
    return redirect(url_for('users.user_posts', username=current_user.username))
