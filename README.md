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

I have now completed milestone 3 and will move on to the next milestone.

I will first make user dashboard soo that I can make bookings and then it will also show upon admin's booking track page.

alright soo I have completed the whole project,
in the other milestones there are a lot of things that were overlapping the starting 4 milestones and while making the 4th one I saw the other milestones and just thougt it would be better to commit it fully now.

there were a lot of mistakes again 

1. I tested the delete option and then I ended up with an error from the database sqllite, the problem was that I was deleting the user but the bookings were still there and they needed the user id to keep the booking. I just put the cascading = all in the bookings relationship in models.py

2. I had to make changes in the db by adding the start_date so that I can state when the trek is gonna start and for that I had to remove all the data that was stored before(there was one other way but it was a lot to learn in such short time and I didn't have that much data).

3. because of these a lot of things had to be changed in the html and css plus also in the routes so that they can process the data store it and then it can be used later by other parts of the code.

4. VS code is still marking some part of my code red where I used jinja2 logics inside a style. I really don't know what I can do about it currently I am just ignoring the problem but I think in future it would affect me cause I would not be able to pinpoint a real bug that easily. 

future things I wanna add

I definetly wanna improve my css in the futurem the other extra milestones will be lovely to perform but I don't have time the submission is today only.

I would wanna implement more tables and more attributes in the current tables so that it can be proper and I have thought of ways it can be more amazing with API integration and all but for that I will have to research if that can happen or not.

My opinion

It is a very decent site the color pallet and everything looks pleasing to the eye and also a bit more nature related.

not everyone will be pleased with the er diagram that much cause there are not that many tables and not that many attributes to those tables.

but it is fine for the first time, can definitely improve.
