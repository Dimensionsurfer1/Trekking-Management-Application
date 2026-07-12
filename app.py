from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User, Staff_profiles, Trek

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trekking_app_data.db'
# this is to tell flask where is our database file

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# already stated previously in I think init_db

app.config['SECRETE_KEY'] = 'spy_from_blood_on_the_clock_tower'
# this is to securely encrypt user session, I key is related to my fav board game and one of it's charachter 

db.init_app(app)
# binding database to this server


@app.route('/')
def home():
    # first gonna test with just text
    return f"the trekking management app is alive and thriving lol, the db should be connected"

if __name__ == '__main__':
    app.run(debug=True)
 # I have set the debug to be true so that If anything occurs I won't have to restart app again and again
 