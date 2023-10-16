# Importing the libraries needed for the project
from flask import Flask, request, jsonify
from models.People import People, db
from models.Job import Job
from datetime import datetime
import uuid
import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import text

# Get the database information from .env file
if os.path.exists(".env"):

    load_dotenv(find_dotenv())
    db_url = os.getenv("DB_URL")

    # Creation of Flask application
    app = Flask(__name__)
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = db_url
    db.init_app(app)
    is_db_correct = False
    try:
        # Test the database connection
        with app.app_context():
            db.session.execute(text("SELECT 1"))
        is_db_correct = True
    except Exception as e:
        print("Error ! Please read instructions in README.md Check your database information")
        print(f"Failed to create the database: {str(e)}")

    # Route to add people in database
    @app.route('/new-people', methods=['POST'])
    def create_person():
        try:
            # Get data from request
            data = request.get_json()
            firstname = data.get('firstname')
            lastname = data.get('lastname')
            birthdate = data.get('birthdate')

            # Create a new People object
            new_person = People(firstname=firstname, lastname=lastname, birthdate=birthdate)

            # Add the new person to the database
            db.session.add(new_person)
            db.session.commit()

            # Return response with message and information about the new person
            response = jsonify({"message": "Success! New person created", "people": {
                "uuid": uuid.UUID(bytes=new_person.uuid),
                "firstname": new_person.firstname,
                "lastname": new_person.lastname,
                "birthdate": new_person.birthdate
            }})
            response.status_code = 201  # Code HTTP 201 pour la création réussie
            return response

        # If we have an error (invalid data in request)
        except Exception as e:
            # En cas d'erreur, renvoyez un message d'erreur avec le code HTTP 400
            response = jsonify({"message": "Bad request. Please provide valid data."})
            response.status_code = 400
            return response


    # Route to add a job to a person
    @app.route('/add-job-people', methods=['POST'])
    def add_job_people():
        try:
            # Get the data from the request
            data = request.get_json()
            company_name = data.get('companyName')
            position = data.get('position')
            start_date = data.get('startDate')
            end_date = data.get('endDate')
            people_uuid = data.get('peopleUuid')

            # Get the people selected by his/her uuid
            person = People.query.filter_by(uuid=uuid.UUID(people_uuid).bytes).first()

            if person is not None:
                # We must convert date (string) in datetimes objects, and we check if the data are valid
                try:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d')
                    end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
                except ValueError:
                    return jsonify({"status": 400,
                                    "message": "Bad request. Please respect this format : 'Y-m-d'. Example : '2000-05-27'"}), 400

                # We create a new job object
                job = Job(company_name=company_name, position=position, start_date=start_date, end_date=end_date)
                # We associated the person and his/her job
                job.people = person

                # Add the new job to the database
                db.session.add(job)
                db.session.commit()

                # Return response with message and information about the person and his/her new job
                response_data = {
                    "status": 201,
                    "message": "Success : New job created !",
                    "people": {
                        "uuid": uuid.UUID(bytes=person.uuid),
                        "firstname": person.firstname,
                        "lastname": person.lastname,
                        "birthdate": person.birthdate,
                    },
                    "job": {
                        "companyName": job.company_name,
                        "position": job.position,
                        "startDate": job.start_date,
                        "endDate": job.end_date,
                    }
                }
                response = jsonify(response_data)
                response.status_code = 201
                return response
            else:
                # If the UUID is not valid, the people is impossible to find
                response = jsonify({"message": "Bad request. People unknown. Please check the UUID."})
                response.status_code = 400
                return response


        except Exception as e:
            # If the data are not valid in the request
            response = jsonify({"message": "Bad request. Please provide valid data."})
            response.status_code = 400
            return response


    @app.route('/peoples', methods=['GET'])
    def get_peoples():
        # Ge get all the perople in the database
        peoples = People.query.order_by(People.lastname).all()
        # We serialize the recovered data
        peoples = People.query.order_by(People.lastname).all()
        serialized_peoples = []
        # For each person, we need to retrieve their current job(s) and serialize them as well.
        for person in peoples:
            current_jobs = [job.serialize() for job in person.current_jobs()]
            serialized_person = person.serialize()
            serialized_person['current_jobs'] = current_jobs
            serialized_peoples.append(serialized_person)

        # We return the result in the   response
        return jsonify(serialized_peoples), 200


    @app.route('/company-members/<string:company_name>', methods=['GET'])
    def company_members(company_name):
        # With SQLAlchemy, we obtain the list of employees of a company entered as route parameter
        company_members = (
            db.session.query(People)
            .join(Job, People.jobs)
            .filter(Job.company_name == company_name, Job.end_date.is_(None))
            .all()
        )

        # And then we serialize people data
        serialized_members = [person.serialize() for person in company_members]

        response = {
            "status": 200,
            "companyName": company_name,
            "employees": serialized_members
        }

        return jsonify(response), 200

    if __name__ == '__main__' and is_db_correct is True:
        print("Web-atrio technical test (Flask Version) - API REST by Julien MARFELLA (@TheJulienM)")
        app.run(debug=True)
    else:
        print("Error ! Please read instructions in README.md Check your database information")

else:
    print("Error ! Please read instructions in README.md")
