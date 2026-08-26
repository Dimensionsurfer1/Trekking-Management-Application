from flask import Flask
from models import db, User
from werkzeug.security import generate_password_hash

# we are creating this function so that we can create it only once and when we use this script in our terminal
# if I import this file into another script it won't trigger accidentally 
def initialize_database():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trekking_app_data.db'
    # it tells which database to use and where to find it and also creates a local file for it
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # this feature tracks every change in db and notifies python but uses a lot of RAM and therefore set to false.
    db.init_app(app)
    
    with app.app_context():
        db.drop_all()  # remember to delete this part before submitting it to production 
        # otherwise database will have no data everytime we run it, it is only for testing
        db.create_all()
        print("Tables created successfully!")
        
        
        admin = User(
            username="superadmin",
            password = generate_password_hash("admin123*"), # must work
            role="Admin",
            name="Aryan Saxena",
            contact_details="9295239548",
            email_id="aryan-trek-admin@gmail.com"
        )
        db.session.add(admin) # adds admin to the db
        db.session.commit() # finally commits the changes and the admin is created successfully
        print("Pre-existing Admin user created successfully!")


# this is the part that helps us not to triggre it accidentally the above function
if __name__ == "__main__":
    initialize_database()