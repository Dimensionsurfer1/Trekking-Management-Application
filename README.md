Trekking Management Application (TMA)

Hey! This is my project for the Modern Application Development I (MAD-I) course. It's a web app built to help adventure groups manage trekking trips, track bookings, and assign staff without messing things up with spreadsheets or manual phone calls.

## Tech Stack Used
* **Backend:** Flask
* **Frontend:** HTML, CSS, Bootstrap, and Jinja2 templates (No JS for core requirements!)
* **Database:** SQLite (SQLAlchemy ORM)

## Application Roles
1. **Admin:** Pre-created superuser who manages treks, approves/blacklists staff, and looks at overall stats.
2. **Trek Staff:** Registers and waits for admin approval, then manages assigned treks and tracks participants.
3. **User (Trekker):** Registers, searches/filters open treks, and books trips.

## How to Run Locally
*(Will add exact commands once the virtual environment and app.py are set up!)*

## Difficulties faced:

1. The biggest challenge that I faced was that I wanted both my users and staff table to have contact info but the problem was I made it so that it called for sepearate contacts in both the table, the problem arises if a person updates his/her profile contact then it will have to be updated in both the table and also I will have to store two seperate contacts for a single user, which is not ideal. To solve it I used the decorator to call upon the contacts from the user table.

2. I also got stuck thinking what will happen if user deletes his/her data, and worse if they were staff member I would have to delete all the data from both the tables, I looked online for the solution and came across this (cascade="all, delete-orphan") This management rule decides what happens once the parent is deleted and orphan data is left

3. some small mistakes that i made was with the first letter capital letter when we write db.Column but it is not the same case for db.relationship, still have to figure this out.

after testing db:

1.there were a lot of mistakes, like while making Foreignkey the K should be capital, and more with the capital letter once also wrote ProfileStaff while my table was named profile_staff
2. I did not remove the manual contact so it was having conflict basically overriding the data.

This is the completion of the milestone 1
I encountered countless spelling mistakes like user and users, it must be there in my previous commit too also I made a init_db.py to initialize the databse and also I inserted an admin with name Aryan Saxena.