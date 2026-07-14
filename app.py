from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, Staff_profiles, Trek, Booking
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
# new import for security 


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trekking_app_data.db'
# this is to tell flask where is our database file

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# already stated previously in I think init_db

app.config['SECRET_KEY'] = 'spy_from_blood_on_the_clock_tower'
# this is to securely encrypt user session, I key is related to my fav board game and one of it's charachter 

db.init_app(app)
# binding database to this server


@app.route('/')
def home():
   
    return render_template('TMA_base.html')

#let's make signuo first
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
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
            return redirect(url_for('signup'))
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
        if role == 'Staff':
            new_staff = Staff_profiles(user_id=new_user.id)
            db.session.add(new_staff)
            db.session.commit()
        # the final flash message of completion
        
        flash("WOOOO-HOOOOO your account was successfully created, now you can log in!!")
        return redirect(url_for('login'))
    return render_template('signup.html')

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
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'Staff':
                return redirect(url_for('staff_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        # else for wrong username or password

        else:
            flash("Invalid username or password")
            return redirect(url_for('login'))
    return render_template ('login.html')



#           ADMIN BLOCK            

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('role') != 'Admin':
        flash("Unauthorized access")
        return redirect(url_for('login'))
    
    # all data for the statistics
    total_users = User.query.filter_by(role='Trekker').count()
    total_staff = User.query.filter_by(role='Staff').count()
    total_treks = Trek.query.count()
    total_bookings = Booking.query.count()
    
    # staff who have not passed the sellection
    pending_staff = Staff_profiles.query.filter_by(status='pending').all()
    
    # sending data to render the template with this data.
    return render_template('admin-dashboard.html', 
                           total_users=total_users,
                           total_staff=total_staff,
                           total_treks=total_treks,
                           total_bookings=total_bookings,
                           pending_staff=pending_staff)

#  approved and reject route

@app.route('/admin/approve_staff/<int:id>', methods=['POST'])
def approve_staff(id):
    if 'user_id' not in session or session.get('role') != 'Admin':
        return redirect(url_for('login'))
        
    staff = Staff_profiles.query.get(id)
    if staff:
        staff.status = 'Approved'
        db.session.commit()
        flash(f"yayya {staff.users.name} user is now part of your staff ")
        
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/reject_staff/<int:id>', methods=['POST'])
def reject_staff(id):
    if 'user_id' not in session or session.get('role') != 'Admin':
        return redirect(url_for('login'))
        
    staff = Staff_profiles.query.get(id)
    if staff:
        # We grab the linked user account so we can delete that too
        user = staff.users 
        db.session.delete(staff)
        db.session.delete(user)
        db.session.commit()
        flash(f"user {user.name} has been rejected from being a part of staff.")
        
    return redirect(url_for('admin_dashboard'))

# adding sub parts of admin that need to be build under here
# just below the admin-board so it's in sequence

@app.route('/admin/treks')
# this is the main trek page, alwasy check for role first.
def admin_manage_treks():
    if 'user_id' not in session or session.get('role') != 'Admin':
        flash("Unauthorized access")
        return redirect(url_for('login'))
        
    all_treks = Trek.query.all()
    # Fetch approved staff to populate the dropdown menu
    approved_staff = Staff_profiles.query.filter_by(status='Approved').all()
    
    return render_template('admin_treks.html', treks=all_treks, approved_staff=approved_staff)


# this is for adding a trek
@app.route('/admin/treks/add', methods=['POST'])
def admin_add_trek():
    if 'user_id' not in session or session.get('role') != 'Admin':
        return redirect(url_for('login'))
        
    trek_name = request.form.get('trek_name')
    location = request.form.get('location')
    difficulty = request.form.get('difficulty')
    duration = request.form.get('duration')
    max_slots = request.form.get('max_slots')
    staff_id = request.form.get('staff_assigned_id') # Get the assigned staff ID
    start_date = request.form.get('start_date')

    new_trek = Trek(
        trek_name=trek_name,
        location=location,
        difficulty=difficulty,
        duration=duration,
        start_date=start_date,
        max_slots=max_slots,
        staff_assigned_id=staff_id if staff_id else None, # Assign them if selected
        booking_status='Open' 
    )
    
    db.session.add(new_trek)
    db.session.commit()
    flash(f"Successfully created the trek: {trek_name}")
    
    return redirect(url_for('admin_manage_treks'))

@app.route('/admin/treks/delete/<int:id>', methods=['POST'])
# this part is for removing or deleting the trek that was made
def admin_delete_trek(id):
    if 'user_id' not in session or session.get('role') != 'Admin':
        return redirect(url_for('login'))
        
    trek = Trek.query.get(id)
    if trek:
        db.session.delete(trek)
        db.session.commit()
        flash(f"Trek '{trek.trek_name}' has been deleted.")
        
    return redirect(url_for('admin_manage_treks'))

# we are making more admin routes to manage users and staff

@app.route('/admin/users')
def admin_manage_users():
    if 'user_id' not in session or session.get('role') != 'Admin':
        flash("Unauthorized access")
        return redirect(url_for('login'))
    
    search_query = request.args.get('q', '')
    
    if search_query:
        # If they searched something, filter by ID, Name, or Username
        # (We use or_ to check if the search term matches ANY of these columns)
        users = User.query.filter(
            or_(
                User.id == search_query,
                User.name.ilike(f'%{search_query}%'),
                User.username.ilike(f'%{search_query}%')
            )
        ).all()
    else:
        # If no search, just show everyone
        users = User.query.all()
        
    return render_template('admin_users.html', users=users, search_query=search_query)

@app.route('/admin/users/blacklist/<int:id>', methods=['POST'])
def admin_blacklist_user(id):
    if 'user_id' not in session or session.get('role') != 'Admin':
        return redirect(url_for('login'))
        
    user_to_delete = User.query.get(id)
    
    # Security check so the Admin doesn't accidentally delete themselves
    if user_to_delete and user_to_delete.role != 'Admin':
        username = user_to_delete.username
        
        # Because we set up cascade="all, delete-orphan" in models.py, 
        # deleting the user will automatically delete their staff profile!
        db.session.delete(user_to_delete)
        db.session.commit()
        
        flash(f"User '{username}' has been successfully blacklisted and removed from the system.")
    
    return redirect(url_for('admin_manage_users'))

# adding admin trek editing page and form

@app.route('/admin/treks/edit/<int:id>', methods=['GET', 'POST'])
def admin_edit_trek(id):
    if 'user_id' not in session or session.get('role') != 'Admin':
        return redirect(url_for('login'))
        
    # Find the specific trek we want to edit
    trek = Trek.query.get(id)
    approved_staff = Staff_profiles.query.filter_by(status='Approved').all()
    
    if request.method == 'POST':
        # Update the database with the newly submitted form data
        trek.trek_name = request.form.get('trek_name')
        trek.location = request.form.get('location')
        trek.difficulty = request.form.get('difficulty')
        trek.duration = request.form.get('duration')
        trek.start_date = request.form.get('start_date') # the new update so that we can have dates now
        trek.max_slots = request.form.get('max_slots')
        
        staff_id = request.form.get('staff_assigned_id')
        trek.staff_assigned_id = staff_id if staff_id else None
        
        db.session.commit()
        flash(f"Trek '{trek.trek_name}' has been successfully updated!")
        return redirect(url_for('admin_manage_treks'))
        
    return render_template('admin_edit_trek.html', trek=trek, approved_staff=approved_staff)
 #last part of the admin board, making the booking table and making it editable.
@app.route('/admin/bookings')
def admin_view_bookings():
    if 'user_id' not in session or session.get('role') != 'Admin':
        flash("Unauthorized access")
        return redirect(url_for('login'))
        
    # here we are fetching all the bookings and the newset ones will be the first.
    all_bookings = Booking.query.order_by(Booking.id.desc()).all()
    
    return render_template('admin_bookings.html', bookings=all_bookings)

@app.route('/admin/treks/info/<int:id>')
def admin_trek_info(id):
    if 'user_id' not in session or session.get('role') != 'Admin':
        flash("Unauthorized access")
        return redirect(url_for('login'))
        
    # Fetch the specific trek
    trek = Trek.query.get(id)
    
    if not trek:
        flash("Trek not found.")
        return redirect(url_for('admin_manage_treks'))
        
    return render_template('admin_trek_info.html', trek=trek)

#                 ADMIN BLOCK
# Here we end with the admin block and if there were to come some updates it would be inside this

#                 STAFF BLOCK

@app.route('/staff_dashboard')
def staff_dashboard():
    if 'user_id' not in session or session.get('role') != 'Staff':
        flash("Unauthorized access!")
        return redirect(url_for('login'))
        
    # Get the logged-in staff member's profile
    staff_profile = Staff_profiles.query.filter_by(user_id=session['user_id']).first()
    
    # Get their assigned treks using the relationship defined in models.py
    my_treks = staff_profile.assigned_treks
    
    return render_template('staff_dashboard.html', assigned_treks=my_treks)

@app.route('/staff/update_trek/<int:id>', methods=['POST'])
def staff_update_trek(id):
    if 'user_id' not in session or session.get('role') != 'Staff':
        return redirect(url_for('login'))
        
    trek = Trek.query.get(id)
    staff_profile = Staff_profiles.query.filter_by(user_id=session['user_id']).first()
    
    if trek and trek.staff_assigned_id == staff_profile.id:
        trek.booking_status = request.form.get('booking_status')
        new_trek_status = request.form.get('trek_status')
        trek.max_slots = request.form.get('max_slots')
        
        # Check if the guide just marked the trek as "Completed"
        if new_trek_status == 'Completed' and trek.trek_status != 'Completed':
            # Loop through all participants and auto-complete their personal booking status!
            for booking in trek.bookings:
                if booking.booking_status == 'Booked':
                    booking.booking_status = 'Completed'
                    
        trek.trek_status = new_trek_status
        db.session.commit()
        flash(f"Successfully updated details for '{trek.trek_name}'.")
    else:
        flash("You are not authorized to edit this trek.")
        
    return redirect(url_for('staff_dashboard'))

# approving the user or not is routed down here

@app.route('/staff/approve_booking/<int:booking_id>', methods=['POST'])
def staff_approve_booking(booking_id):
    if 'user_id' not in session or session.get('role') != 'Staff':
        return redirect(url_for('login'))
        
    booking = Booking.query.get(booking_id)
    staff_profile = Staff_profiles.query.filter_by(user_id=session['user_id']).first()
    
    if booking and booking.trek.staff_assigned_id == staff_profile.id:
        booking.booking_status = 'Booked' # Change from Pending to Booked!
        db.session.commit()
        flash(f"Approved {booking.trekker.name}'s request to join the trek!")
        
    return redirect(url_for('staff_view_participants', id=booking.trek_id))

@app.route('/staff/reject_booking/<int:booking_id>', methods=['POST'])
def staff_reject_booking(booking_id):
    if 'user_id' not in session or session.get('role') != 'Staff':
        return redirect(url_for('login'))
        
    booking = Booking.query.get(booking_id)
    staff_profile = Staff_profiles.query.filter_by(user_id=session['user_id']).first()
    
    if booking and booking.trek.staff_assigned_id == staff_profile.id:
        booking.booking_status = 'Rejected'
        db.session.commit()
        flash(f"Rejected {booking.trekker.name}'s booking request.")
        
    return redirect(url_for('staff_view_participants', id=booking.trek_id))


@app.route('/staff/trek_participants/<int:id>')
def staff_view_participants(id):
    if 'user_id' not in session or session.get('role') != 'Staff':
        return redirect(url_for('login'))
        
    trek = Trek.query.get(id)
    staff_profile = Staff_profiles.query.filter_by(user_id=session['user_id']).first()
    
    if trek and trek.staff_assigned_id == staff_profile.id:
        
        return render_template('staff_participants.html', trek=trek)
        
    flash("You are not authorized to view this trek.")
    return redirect(url_for('staff_dashboard'))

#                 STAFF BLOCK


#                 USER BLOCK

@app.route('/user_dashboard')
def user_dashboard():
    if 'user_id' not in session or session.get('role') != 'Trekker':
        flash("Unauthorized access!")
        return redirect(url_for('login'))
        
    search_query = request.args.get('q', '')
    diff_filter = request.args.get('difficulty', '')
    
    # 1. Start with all Open treks
    query = Trek.query.filter_by(booking_status='Open')
    
    # 2. Apply text search if it exists
    if search_query:
        query = query.filter(
            or_(
                Trek.trek_name.ilike(f'%{search_query}%'),
                Trek.location.ilike(f'%{search_query}%')
            )
        )
        
    # 3. Apply difficulty filter if it exists
    if diff_filter:
        query = query.filter_by(difficulty=diff_filter)
        
    open_treks = query.all()
    
    # 4. Fetch the user's specific booking history
    my_bookings = Booking.query.filter_by(user_id=session['user_id']).order_by(Booking.id.desc()).all()
    
    return render_template('user_dashboard.html', 
                           open_treks=open_treks, 
                           my_bookings=my_bookings, 
                           search_query=search_query, 
                           diff_filter=diff_filter)

@app.route('/user/book/<int:trek_id>', methods=['POST'])
def book_trek(trek_id):
    if 'user_id' not in session or session.get('role') != 'Trekker':
        return redirect(url_for('login'))
        
    trek = Trek.query.get(trek_id)
    user_id = session['user_id']
    
    if not trek or trek.booking_status != 'Open':
        flash("This trek is no longer available.")
        return redirect(url_for('user_dashboard'))
        
    # PDF Requirement: Prevent overbooking beyond available slots
    current_bookings_count = len(trek.bookings)
    if current_bookings_count >= trek.max_slots:
        flash("Sorry, this trek is completely full!")
        return redirect(url_for('user_dashboard'))
        
    # Prevent the user from double-booking the same trek
    existing_booking = Booking.query.filter_by(user_id=user_id, trek_id=trek.id, booking_status='Booked').first()
    if existing_booking:
        flash("You have already booked this trek!")
        return redirect(url_for('user_dashboard'))
        
    # Create the booking
    # Create the booking and set it to Pending
    new_booking = Booking(user_id=user_id, trek_id=trek.id, booking_status='Pending')
    db.session.add(new_booking)
    db.session.commit()
    
    flash(f"Success! You have booked your spot for {trek.trek_name}.")
    return redirect(url_for('user_dashboard'))


#               USER BLOCK

# common block

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash("Please log in to view your profile.")
        return redirect(url_for('login'))
        
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        new_username = request.form.get('username')
        new_password = request.form.get('new_password')
        
        # 1. Check if they changed their username, and if the new one is available
        if new_username != user.username:
            existing_user = User.query.filter_by(username=new_username).first()
            if existing_user:
                flash("That username is already taken. Please choose another one.")
                return redirect(url_for('profile'))
            user.username = new_username
            session['username'] = new_username # Update the session so the header changes immediately!

        # 2. Check if they typed a new password
        if new_password: # Only update if the field isn't blank
            user.password = generate_password_hash(new_password)
            
        # 3. Update the rest of their details
        user.name = request.form.get('name')
        user.email_id = request.form.get('email_id')
        user.contact_details = request.form.get('contact_details')
        
        db.session.commit()
        flash("Your profile has been successfully updated!")
        
        # Smart Redirect back to their specific dashboard
        role = session.get('role')
        if role == 'Admin':
            return redirect(url_for('admin_dashboard'))
        elif role == 'Staff':
            return redirect(url_for('staff_dashboard'))
        else:
            return redirect(url_for('user_dashboard'))
            
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()
 # I have set the debug to be true so that If anything occurs I won't have to restart app again and again
 