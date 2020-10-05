from flask import (render_template, url_for, flash, redirect, request, 
                    abort, Blueprint)
from flask_login import (login_user, current_user, logout_user, 
                        login_required)
from yogapose import db
from yogapose.models import Post
from yogapose.posts.forms import PostPoseForm, UpdatePostPoseForm
from yogapose.users.utils import save_picture

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostPoseForm()
    if form.validate_on_submit():
        picture_file = save_picture(form.pose_pic.data, foldername='posted_pics', output_size=(300,300) )
        post = Post(pose_name=form.pose_name.data, pose_pic=picture_file, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your pose has been posted!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', 
                            form=form)

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
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
        #post.pose_pic = form.pose_pic.data
        db.session.commit()
        flash('Your pose has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.pose_name.data = post.pose_name
        #form.pose_pic.data = post.pose_pic
    return render_template('update_post.html', title='Update Post', 
                            form=form, post=post)

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your pose has been deleted!', 'success')
    return redirect(url_for('main.home'))
