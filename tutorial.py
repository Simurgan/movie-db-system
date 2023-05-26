from flask import Flask, render_template

# Create a Flask Instance
app = Flask(__name__)

# Create a rouote decorator
@app.route('/')

def index():
    return render_template("index.html")

@app.route('/signin/')
def sign_in():
    return "<h1>Sign-in Page</h1>"

@app.route('/instance_user_page/<name>')
def instance_user_page(name):
    return render_template("instance.html", name=name)

# some filters
# safe
# capitalize
# upper
# title
# trim
# striptags