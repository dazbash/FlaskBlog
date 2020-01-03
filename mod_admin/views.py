from flask import session, render_template, request, abort, flash
from mod_users.forms import LoginForm
from mod_users.models import User
from . import admin
from .utils import protected_view

@admin.route('/')
@protected_view
def index():
    return "Hello admin index"
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
        session['email']= user.email
        session['user_id']= user.id
        return 'login success'
    if session.get('email') is not None:
        return "you are already logged in"
    return render_template('admin/login.html', form=frm)