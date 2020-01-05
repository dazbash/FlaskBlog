from flask import request, render_template
from . import users
from .forms import RegisterForm


@users.route('/register/', methods= ['GET', 'POST'])
def register():
    form = RegisterForm(register.form)
    if register.method == 'POST':
        if form.validate_on_submit():
            pass
    return render_template('users/register.html', form=form)