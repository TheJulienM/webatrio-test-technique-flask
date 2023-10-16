# Web-atrio technical test Flask Version - Web application by Julien MARFELLA (@TheJulienM)

### How to install this project :

1. Clone the project : 
   - `git clone git@github.com:TheJulienM/webatrio-test-technique-flask.git`
2. Go to the project folder : 
   - `cd webatrio-test-technique-flask`
3. Create your virtualenv :
    - `virtualenv venv`
4. Activate your virtualenv :
    - On Windows : `venv\Scripts\activate`
    - On Linux / macOS : `source venv/bin/activate`
5. Create a .env file from the .env.example:
   - On Windows : `copy .env.example .env`
   - On Linux / macOS : `cp .env.example .env`
6. Edit the database URL with your own configuration
   - Note : Your can use the database of the first project https://github.com/TheJulienM/webatrio-test-technique
7. Install the necessary dependencies for this project in the virtualenv :
   - `pip install -r requirements.txt`
8. Run the project
   - `py app.py`
9. Now, the Flask application should be ready. Go to http://localhost:5000/ (the port may be different)
10. 