from flask import Flask, request, jsonify
from models.People import People, db
from models.Job import Job
from datetime import datetime
import uuid

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1:3306/webatrio'  # Remplacez par votre URI de base de données
db.init_app(app)


@app.route('/new-people', methods=['POST'])
def create_person():
    try:
        # Récupérez les données de la requête JSON
        data = request.get_json()
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        birthdate = data.get('birthdate')

        # Créez une nouvelle personne
        new_person = People(firstname=firstname, lastname=lastname, birthdate=birthdate)

        # Ajoutez la nouvelle personne à la base de données
        db.session.add(new_person)
        db.session.commit()

        # Répondre avec un message de succès
        response = jsonify({"message": "Success! New person created", "people": {
            "uuid": uuid.UUID(bytes=new_person.uuid),
            "firstname": new_person.firstname,
            "lastname": new_person.lastname,
            "birthdate": new_person.birthdate
        }})
        response.status_code = 201  # Code HTTP 201 pour la création réussie
        return response

    except Exception as e:
        # En cas d'erreur, renvoyez un message d'erreur avec le code HTTP 400
        response = jsonify({"message": "Bad request. Please provide valid data."})
        response.status_code = 400
        return response


@app.route('/add-job-people', methods=['POST'])
def add_job_people():
    try:
        # Récupérez les données de la requête JSON
        data = request.get_json()
        company_name = data.get('companyName')
        position = data.get('position')
        start_date = data.get('startDate')
        end_date = data.get('endDate')
        people_uuid = data.get('peopleUuid')

        # Recherchez la personne (People) par son UUID
        person = People.query.filter_by(uuid=uuid.UUID(people_uuid).bytes).first()

        if person is not None:
            # Créez un nouvel emploi (Job)
            print(start_date)
            # Convertir les dates de chaînes en objets datetime
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
            except ValueError:
                return jsonify({"status": 400,
                                "message": "Bad request. Please respect this format : 'Y-m-d'. Example : '2000-05-27'"}), 400

            job = Job(company_name=company_name, position=position, start_date=start_date, end_date=end_date)
            job.people = person  # Associez l'emploi à la personne

            # Ajoutez et enregistrez l'emploi dans la base de données
            db.session.add(job)
            db.session.commit()

            # Répondre avec un message de succès
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
            response.status_code = 201  # Code HTTP 201 pour la création réussie
            return response
        else:
            # Si la personne n'est pas trouvée, renvoyez un message d'erreur
            response = jsonify({"message": "Bad request. People unknown. Please check the UUID."})
            response.status_code = 400
            return response


    except Exception as e:
        # En cas d'erreur, renvoyez un message d'erreur avec le code HTTP 400
        response = jsonify({"message": "Bad request. Please provide valid data."})
        response.status_code = 400
        return response


if __name__ == '__main__':
    app.run(debug=True)
