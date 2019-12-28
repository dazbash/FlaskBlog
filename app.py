from flask import Flask


app = Flask(__name__)

@app.route('/')
def index():
    return 'blog home.'


from mod_admin import admin

app.register_blueprint(admin)