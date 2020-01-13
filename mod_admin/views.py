from flask import session, render_template, request, abort, flash, redirect, url_for
from mod_users.forms import LoginForm, RegisterForm
from mod_users.models import User
from . import admin
from .utils import admin_only_viwe
from mod_blog.forms import CreatePostForm, ModifyPostForm
from mod_blog.models import Post
from app import db
from sqlalchemy.exc import IntegrityError

@admin.route('/')
@admin_only_viwe
def index():
    return render_template('admin/index.html')

@admin.route('/login/', methods=['GET','POST'])
def login():
    frm = LoginForm(request.form)
    if request.method == 'POST':
        if not frm.validate_on_submit():
            abort(400)
        user = User.query.filter(User.email.ilike("%s" % frm.email.data)).first()
        if  not user:
            flash('Incorrect Credentials', category='error')
            return render_template('admin/login.html', form=frm)
        if not user.check_password(frm.password.data):
            flash('Incorrect Credentials', category='error')
            return render_template('admin/login.html', form=frm)
        if not user.is_admin():
            flash('Incorrect Credentials', category='error')
            return render_template('admin/login.html', form=frm)
        session['email']= user.email
        session['user_id']= user.id
        session['role']= user.role
        return redirect(url_for('admin.index'))
    if session.get('role') == 1:
        return redirect(url_for('admin.index'))
    return render_template('admin/login.html', form=frm)


@admin.route('/logout', methods= ['GET'])
@admin_only_viwe
def logout():
    session.clear()
    flash('You are logged out successfully. ', 'warning')
    return redirect(url_for('admin.login'))

@admin.route('/users/', methods=['GET', ])
@admin_only_viwe
def list_users():
    users = User.query.order_by(User.id.desc()).all()
    return render_template('admin/list_users.html', users=users)

@admin.route('/users/new/', methods=['GET'])
@admin_only_viwe
def get_create_user():
    form = RegisterForm()
    return render_template('admin/create_user.html', form=form)


@admin.route('/users/new/', methods=['POST'])
@admin_only_viwe
def post_create_user():
    form = RegisterForm(request.form)
    if not form.validate_on_submit():
        return render_template('admin/create_user.html', form=form)
    if not form.password.data == form.confirm_password.data:
        error_msg = 'Password and Confirm_password dose not match'
        form.password.errors.append(error_msg)
        form.confirm_password.errors.append(error_msg)
        return render_template('admin/create_user.html', form=form)
    old_user = User.query.filter(User.email.ilike(form.email.data)).first()
    if old_user:
        flash('EMail is in Use', 'error')
        return render_template('admin/create_user.html', form=form)
    new_user = User()
    new_user.full_name = form.full_name.data
    new_user.email = form.email.data
    new_user.set_password(form.password.data)
    # try:
    db.session.add(new_user)
    db.session.commit()
    flash('You created your account successfully.', 'success')
    return render_template('admin/register.html', form=form)


    # except IntegrityError:
    #     db.session.rollback()
    #     flash('Email is in Use. ', 'error' )


@admin.route('/posts/new/', methods=['GET', 'POST'])
@admin_only_viwe
def create_post():
    form = CreatePostForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            return '1'
        new_post = Post()
        new_post.title = form.title.data
        new_post.content = form.content.data
        new_post.slug = form.slug.data
        new_post.summary = form.summary.data
        try:
            db.session.add(new_post)
            db.session.commit()
            flash('Post created!  ')
            return redirect(url_for('admin.index'))
        except IntegrityError:
            db.session.rollback()
            flash('Slug Duplicated')
    return render_template('admin/create_post.html', form=form)


@admin.route('/posts', methods=['GET'])
@admin_only_viwe
def list_posts():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('admin/list_posts.html', posts=posts)


@admin.route('/posts/delete/<int:post_id>', methods=['GET'])
@admin_only_viwe
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post Deleted, !')
    return redirect(url_for('admin.list_posts'))


@admin.route('/posts/modify/<int:post_id>', methods=['GET', 'POST'])
@admin_only_viwe
def modify_post(post_id):
    post= Post.query.get_or_404(post_id)
    form= ModifyPostForm(obj=post)
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('admin/modify_post.html', form=form, post=post)
        post.title = form.title.data
        post.content = form.content.data
        post.slug = form.slug.data
        post.summary = form.summary.data
        try:
            db.session.commit()
            flash('Post modified!  ')
        except IntegrityError:
            db.session.rollback()
            flash('Slug Duplicated')
    return render_template('admin/modify_post.html', form=form, post=post)
