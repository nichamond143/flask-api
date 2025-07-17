from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

# Creates Flask app
app = Flask(__name__)

# Set up DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Set up API
api = Api(app)

# Creates a table called User Model
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'User(name = {self.name}, email = {self.email})'

# Set up Input Parser
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")

# Controll API Output
usersFields = {
    'id':fields.Integer,
    'name':fields.String,
    'email':fields.String,
}

class Users(Resource):
    # Ensure it returns data in the format defined
    @marshal_with(usersFields)

    # Get all users
    def get(self):
        users = UserModel.query.all()
        return users
    
    # Add a new user
    @marshal_with(usersFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args["name"], email=args["email"])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201
    
class User(Resource):
    # Get user by ID
    @marshal_with(usersFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        return user
    
    # Update user by ID
    @marshal_with(usersFields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        user.name = args["name"]
        user.email = args["email"]
        db.session.commit()
        return user
    
    # Delete user by ID
    @marshal_with(usersFields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users

# Register API endpoints
api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')

# Root route
@app.route('/')
def home():
    return '<h1>Flask Rest API</h1>'

# Runs app
if __name__ == '__main__' :
    app.run(debug=True)