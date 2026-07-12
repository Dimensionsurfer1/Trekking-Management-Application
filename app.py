from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, Staff_profiles, Trek
from werkzeug.security import generate_password_hash, check_password_hash
# new import for security 


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
   
    return render_template('TMA_base.html')

#let's make signuo first
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'post':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email_id')
        contact = request.form.get('contact_details')
        password = request.form.get('password')
        role = request.form.get('role')
        # to check if the username already exists

        existing_user = User.query.filter((User.username == username) | (User.email_id == email)).first()
        # basically filters and then checks for the first value
        if existing_user:
            flash("This email id or username already exists! please choose a different one")
            return redirect(url_for(signup))
        # now if the person signs up perfectly then
        # we have got all the details now we store data, but before that we hash password with our new imports
        hased_password = generate_password_hash(password)
        #now create user and store it will info
        new_user = User(
            name = name,
            username = username,
            email_id = email,
            contact_details = contact,
            password = hased_password,
            role = role 
        )
        # start a db session and add the data then commit
        db.session.add(new_user)
        db.session.commit()

        # now if the role was selected to be staff then 
        new_staff = Staff_profiles(user_id=new_user.id)
        db.session.add(new_staff)
        db.session.commit()
        # the final flash message of completion
        flash("WOOOO-HOOOOO your account was successfully created, now you can log in!!")
        return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # got the info
        # now we check if legit
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # check the staff cause we don't want staff that has not been approved by admin
            if user.role == 'Staff':
                staff_profile = Staff_profiles.query.filter_by(user_id=user.id).first()
                if staff_profile and staff_profile.status != 'Approved':
                    flash("Your staff account is pending Admin approval.")
                    return redirect(url_for('login'))
            
            # logging the user in or staff
            # we have to create a session for them 
            session['user_id'] = user.id
            session['role'] = user.role
            session['username'] = user.username

            # now to each their own dashboard
            if user.role == 'Admin':
                return redirect(url_for('admin-dashboard'))
            elif user.role == 'Staff':
                return redirect(url_for('staff-dashboard'))
            else:
                return redirect(url_for('user-dashboard'))
        # else for wrong username or password

        else:
            flash("Invalid username or password")
            return redirect(url_for('login'))
    return render_template ('login.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('role') != 'Admin':
        # if not in session or not admin role
        flash("unauthorized access")
        return redirect(url_for(login))
    return "<h1> Admin Dashboard (under construction) <h1>"
@app.route('/staff_dashboard')
def staff_dashboard():
    if 'user_id' not in session or session.get('role') != 'Staff':
        flash("Unauthorized access!")
        return redirect(url_for('login'))
    return "<h1>Staff Dashboard (Under Construction)</h1>"

@app.route('/user_dashboard')
def user_dashboard():
    if 'user_id' not in session or session.get('role') != 'Trekker':
        flash("Unauthorized access!")
        return redirect(url_for('login'))
    return "<h1>Trekker Dashboard (Under Construction)</h1>"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
 # I have set the debug to be true so that If anything occurs I won't have to restart app again and again
 