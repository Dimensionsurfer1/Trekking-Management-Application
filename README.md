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

in the second milestone:
I forgot to maintain this part of the difficulty faced.
some mistakes that I remember:

1. I was very confused with the wasy I structured the home page and all so at the end I made it as simple as possible with two button and heading and slogan with bg picture.

2. I got confused and made two separate css files thinking that it would be better to make one for each page but then in a yt video it said it would be better to just use one cause you can use previous classes and also you won't have to make it again and again, if the nav bar is in all the pages i would have had to iterate every page but that is the case no more.

3. while routing and making the function inside it I did not think the procedure and directly started coding, I then realised I messed up things and then made a flow in my copy and then wrote the code for it.

4. This mistake is yet to be fixed, with this update I will fix it. The problem was that I imported the hashing system from "werkzeug.security" and it would work but the problem is that I have stated my password already and it is not hashed so when I will login and the password I type in will be hashed but the saved password is not hashed so it would not match in my db, for that I will update my init_db.py to hash the password.


A VERY BIG PROBLEM I commited the milestone and didn't check for the mistakes, the mistakes are minor but i am in the fault of not checking it prior to commiting to the repo.


admin-dashboard report:
gonna check it first and then gonna commit this time,
I am trying to put some gandalf memes although haven't watched lord of the rings lol.

will update what was wrong and all , lmao I forgot to update app.py , will meet after routing

Also I forgot to add reject button, I did it now I am gonna route


BIG problem - somewhere int the code I messed up and now my normal user is being in the admin dashboard for approval of becoming a staff, which should not be the case cause I selected a Trekker not Staff_trek, will look at the issue thoroughly.


    AHH found it i did not add if while making staff in app.py and therefore it was making everyone staff. 
    issue fixed.

    