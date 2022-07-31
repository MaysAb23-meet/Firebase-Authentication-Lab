from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyCz0FV6eI5o61OZ6uPi0l5zN7R9POXIXaU",
  "authDomain": "fb-proj-5f40b.firebaseapp.com",
  "projectId": "fb-proj-5f40b",
  "storageBucket": "fb-proj-5f40b.appspot.com",
  "messagingSenderId": "145320707025",
  "appId": "1:145320707025:web:8b3e9912bcb0ef0f0b16f0",
  "measurementId": "G-944E7PESXZ", "databaseURL":""
}



firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       return redirect(url_for('add_tweet'))
       try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
       except:
           error = "Authentication failed"

    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       return redirect(url_for('add_tweet'))
       try:
            login_session['user'] =  auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
       except:
           error = "authentication failed"
    return render_template("signup.html")




@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True)