from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(200), nullable=False)
    lastname = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

# Create
@app.route('/users', methods=['POST'])
def postUser():

    user = User(firstname = request.json['firstname'], 
                  lastname = request.json['lastname'], 
                  email = request.json['email'])

    db.session.add(user)
    db.session.commit()

    return jsonify({'id': user.id, 'firstname':user.firstname,'lastname':user.lastname, 'email': user.email}), 201

# Read
@app.route('/users/<int:id>', methods=['GET'])
def getUserById(id):

    user = User.query.get_or_404(id)

    return jsonify({'id': user.id, 'firstname':user.firstname,'lastname':user.lastname, 'email': user.email})

# Update
@app.route('/users/<int:id>', methods=['PUT'])
def putUser(id):

    user = User.query.get_or_404(id)
    user.firstname = request.json['firstname']
    user.lastname = request.json['lastname']
    user.email = request.json['email']
    db.session.commit()
    return jsonify({'id': user.id, 'firstname':user.firstname,'lastname':user.lastname, 'email': user.email})

# Delete
@app.route('/users/<int:id>', methods=['DELETE'])
def deleteUser(id):

    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'id': user.id, 'firstname':user.firstname,'lastname':user.lastname, 'email': user.email}), 200

# Get All
@app.route('/users', methods=['GET'])
def getUsers():
    users = User.query.all()
    all_users = [{'id': user.id, 'firstname':user.firstname,'lastname':user.lastname, 'email': user.email} for user in users]
    return jsonify(all_users)


if __name__ == "__main__":
    app.run(debug=True)