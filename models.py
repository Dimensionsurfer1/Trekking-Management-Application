from flask_sqlalchemy import SQLAlchemy as sa
from datetime import datetime

db = sa()

#alright so I am going to design the tables on the basis of the ER diagram (there might be some other additions as well)
#first is user
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(67), unique = True, nullable = False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Admin, Staff, Trekker are going to be the options 
    name = db.Column(db.String(100), nullable=False)
    contact_details = db.Column(db.String(15), nullable=False)
    email_id = db.Column(db.String(100), unique=True, nullable=False)

    # include the FK or realtions after completeing all the oter tables.
    staff_profile = db.relationship('StaffProfile', backref='user', uselist=False, cascade="all, delete-orphan")
    # here cascade is a management rule to determine what to do with the child data once their parent recod is deleted or modified 
    bookings = db.relationship('Booking', backref='trekker', lazy=True)
    # lazy helps in not showing unecessary data

class Staff_profiles(db.Model):
    __tablename__ = "staff_profiles"

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.Foreignkey("user.id"),nullable = False)
    status = db.Column(db.String(30), default = "pending") # other values can be Approved and Balcklisted also idle & approved, approved & working
    contact_details = db.Column(db.String(15), nullable = False)

    #reference

    assigned_treks = db.relationship('Trek', backref='guide', lazy=True) # remeber to use "r" not "R" in the db.relationship (third time)

    @property # this is a decorator, calls a diff function and modifies it
    def contact_details(self): # here we are trying to get contacts from the user table 
        return self.user.contact_details

class Trek(db.Model):
    __tablename__ = 'treks'
    
    id = db.Column(db.Integer, primary_key=True)
    trek_name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)  # Easy, Moderate , Hard
    duration = db.Column(db.Integer, nullable=False)       # in Hours
    max_slots = db.Column(db.Integer, nullable=False)
    booking_status = db.Column(db.String(20), default='Open')  # Pending, Open, Closed are the tags that can be used 
    
    # Foreign Key pointing to StaffProfile
    staff_assigned_id = db.Column(db.Integer, db.ForeignKey('staff_profiles.id'), nullable=True)
    # I think it should be nullable cause maybe we haven't assigned a staff to that trek yet

    # Relationships
    bookings = db.relationship('Booking', backref='trek', lazy=True)

    # I used backref before but stating here - It is used for creating a bidirectional access meaning we can access trek from bookings and bookings from trek

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    # this basically helps bridge user and trek.
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('treks.id'), nullable=False)
    booking_date = db.Column(db.Date, default=db.func.current_date())
    booking_status = db.Column(db.String(20), default='Booked')  # Booked, Cancelled, Completed
