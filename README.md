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
How to Run Locally
Follow these steps to set up and run the Trek Management App on your local machine.

1. Clone the repository
First, download the code and navigate into the project folder:
git clone <your-github-repo-url>
cd <your-project-folder-name>

2. Create a virtual environment
It is highly recommended to run this project inside a virtual environment to keep dependencies isolated.
python -m venv .venv

3. Activate the virtual environment
Activate the environment based on your operating system:
.venv\Scripts\activate

4. Install dependencies
Install all required Python packages (like Flask and Flask-SQLAlchemy): pip install -r requirements.txt

5. Initialize the Database
Before running the app for the first time, you need to generate the SQLite database and create the default Superadmin account. Run the initialization script from your terminal:
        python init_db.py
(Note: This script will create the trekking_app_data.db file and automatically generate an Admin user with the username superadmin and password admin123*).

6. Run the application
Start the Flask development server: python app.py

7. Access the App
Open your web browser and navigate to: http://127.0.0.1:5000 or whatever you set your port to.

I have made a mistake of naming my local git config to 23f3001234 while it should have been 23f2005368
I should have looked more closely before commiting this is the second time 1st time it was my main git HUB Id i did not see it then and I could not see now.


With this my core requirements for this application are all complete.

