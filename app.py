import os
from flask import Flask, request, jsonify, abort
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from models import db, User, Profile
from werkzeug.security import generate_password_hash, check_password_hash 

app = Flask(__name__)
app.config['DEBUG'] = os.getenv('DEBUG', False)
app.config['ENV'] = os.getenv('ENV', 'production') 
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

db.init_app(app)
Migrate(app, db)
CORS(app)

@app.route('/')
def main():
    return jsonify({ "message": "Welcome to API REST Flask" }), 200


@app.route('/api/users', methods=['GET'])
def get_all_users():
    users = User.query.all() # [<User 1>, <User 2>]
    users = list(map(lambda user: user.serialize(), users)) # [{"id": 1}, {"id": 2}]
    return jsonify(users), 200


@app.route('/api/users', methods=['POST'])
def create_user():

    username = request.json.get('username')
    password = request.json.get('password')
    bio = request.json.get('bio', "")
    facebook = request.json.get('facebook', "")
    twitter = request.json.get('twitter', "")
    instagram = request.json.get('instagram', "")
    linkedin = request.json.get('linkedin', "")
    github = request.json.get('github', "")

    if not username:
        return jsonify({ "msg": "username is required"}), 422

    if not password:
        return jsonify({ "msg": "password is required"}), 422

    # Primera Forma

    """ 
    user = User()
    user.username = username
    user.password = password
    user.save()

    profile = Profile()
    profile.bio = bio
    profile.facebook = facebook
    profile.twitter = twitter
    profile.instagram = instagram
    profile.linkedin = linkedin
    profile.github = github
    profile.users_id = user.id
    profile.save() 
    """

    # Segunda Forma

    user = User()
    user.username = username
    user.password = generate_password_hash(password)

    profile = Profile()
    profile.bio = bio
    profile.facebook = facebook
    profile.twitter = twitter
    profile.instagram = instagram
    profile.linkedin = linkedin
    profile.github = github

    user.profile = profile
    user.save()

    return jsonify({ "status": 201, "message": "user created", "user": user.serialize_with_profile()}), 201

@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):

    username = request.json.get('username')
    password = request.json.get('password')
    bio = request.json.get('bio', "")
    facebook = request.json.get('facebook', "")
    twitter = request.json.get('twitter', "")
    instagram = request.json.get('instagram', "")
    linkedin = request.json.get('linkedin', "")
    github = request.json.get('github', "")

    if not username:
        return jsonify({ "msg": "username is required"}), 422

    if not password:
        return jsonify({ "msg": "password is required"}), 422

    # Primera Forma
 
    """
    user = User.query.get(id)
    user.username = username
    user.password = generate_password_hash(password)
    user.update()

    profile = Profile.query.filter_by(users_id=id).first()
    profile.bio = bio
    profile.facebook = facebook
    profile.twitter = twitter
    profile.instagram = instagram
    profile.linkedin = linkedin
    profile.github = github
    profile.update() 

    """
    # Segunda Forma
    # variable = valor1 if condition else valor2

    user = User.query.get(id)
    user.username = username
    user.password = generate_password_hash(password)
    user.bio = bio if bio is not None else user.profile.bio
    if bio: user.profile.bio = bio
    if facebook: user.profile.facebook = facebook
    if twitter: user.profile.twitter = twitter
    if instagram: user.profile.instagram = instagram
    if linkedin: user.profile.linkedin = linkedin
    if github: user.profile.github = github 
    user.update() 

    return jsonify({ "status": 201, "message": "user created", "user": user.serialize_with_profile()}), 200

@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    
    user = User.query.get(id)
    #user.profile.delete() # Eliminar primero registros que dependan del usuario
    user.delete()
    
    return jsonify({"msg": "user deleted"}), 200

if __name__ == '__main__':
    app.run()
