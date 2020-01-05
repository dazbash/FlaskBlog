from flask import session, render_template, request, abort, flash
from mod_users.forms import LoginForm
from mod_users.models import User
from . import admin
from .utils import admin_only_viwe

@admin.route('/')
@admin_only_viwe
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
            return render_template('admin/login.html', form=frm)
        if not user.is_admin():
            flash('Incorrect Credentials', category='error')
            return render_template('admin/login.html', form=frm)
        session['email']= user.email
        session['user_id']= user.id
        session['role']= user.role
        return 'login success'
    if session.get('role') == 1:
        print(session)
        return "you are already logged in"
    return render_template('admin/login.html', form=frm)