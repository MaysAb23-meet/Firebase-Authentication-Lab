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
  "measurementId": "G-944E7PESXZ",
  "databaseURL":"https://fb-proj-5f40b-default-rtdb.europe-west1.firebasedatabase.app"
}



firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

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
       full_name = request.form['full_name']
       username = request.form['username']
       bio = request.form['bio']

       user = {"full_name": full_name, "username": username,"bio":bio,"email":email,"password":password}
       try:
            login_session['user'] =  auth.create_user_with_email_and_password(email, password)
            db.child("Users").child(login_session['user']['localId']).set(user)
            
            return redirect(url_for('add_tweet'))
       except:
           error = "authentication failed"
    return render_template("signup.html")




@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        try:
            tweet = {"text": text, "title": title,"UID":login_session['user']['localId']}
            db.child("tweet").push(tweet)
            return redirect(url_for('all_tweets'))
        except:
            print("authentication failed")
    else:
        return render_template("add_tweet.html")
    return render_template("add_tweet.html")


@app.route('/signout', methods=['GET', 'POST'])
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

@app.route('/all_tweets')
def all_tweets():
    tweets= db.child('Tweets').get().val()
    print (tweets)
    return render_template("tweets.html", tweets= tweets)


if __name__ == '__main__':
    app.run(debug=True)