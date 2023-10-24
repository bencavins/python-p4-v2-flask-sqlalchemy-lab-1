# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    # query db for the earthquake obj
    earthq = Earthquake.query.filter(Earthquake.id == id).first()

    if earthq is None:
        return make_response({"message": f"Earthquake {id} not found."}, 404)

    # turn obj -> dict -> json
    body = jsonify(earthq.to_dict())
    # return response with body and status code
    return make_response(body, 200)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_by_magnitude(magnitude):
    # query db for all matching objs
    earthqs = Earthquake.query.filter(
        Earthquake.magnitude >= magnitude
    ).all()
    body = {
        'count': len(earthqs)
    }
    # turned each obj into a dict
    quakes = []
    for earthq in earthqs:
        quakes.append(earthq.to_dict())
    # add quakes list to the body under the key 'quakes'
    body['quakes'] = quakes
    # returning list of dicts in the response
    return make_response(body, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
