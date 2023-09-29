import bcrypt
from flask import request, jsonify, Blueprint, current_app
from models.users import User
from models.base import session
from auth.auth import TokenAuth
from sqlalchemy.exc import SQLAlchemyError

auth_view = Blueprint('auth_view', __name__)

@auth_view.route("/login", methods=["POST"])
def login():
    ''' get the username and password from the request '''
    email = request.json.get("email")
    password = request.json.get("password")
    if not email:
        return jsonify({"message": "Email is required"}), 400
    if not password:
        return jsonify({"message": "Password is required"}), 400
    auth = TokenAuth(current_app)

    user = session.query(User).filter_by(email=email).first()
    if not user:
        return jsonify({"message": "Invalid username or password"}), 401
    hashed_password = user.password.encode("utf-8")

    if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
        token = auth.generate_token(user.email)
        return jsonify({"token": token, 'email': user.email, 'country': user.country}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401


@auth_view.route('/register', methods=['POST'])
def register():
    ''' get the user data from the request '''
    try:
        data = request.json
        email = data.get('email')
        fname = data.get('fname')
        lname = data.get('lname')
        country = data.get('country')
        score = 0
        password = data.get('password')

        if not fname:
            print(11)
            return jsonify({"message": "First name is required"}), 400
        if not lname:
            print(22)
            return jsonify({"message": "Last name is required"}), 400
        if not email:
            print(55)
            return jsonify({"message": "Email is required"}), 400
        if not password:
            print(66)
            return jsonify({"message": "Password is required"}), 400

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = User(email=email, fname=fname, lname=lname, country=country, total_score=score, password=hashed_password)
        session.add(user)
        session.commit()

        return jsonify({'message': 'User created successfully!'})
    except SQLAlchemyError as e:
        session.rollback();
        print(e);
        return jsonify({'error': 'Database error'})
    except Exception as e:
        session.rollback();
        print(e);
        return jsonify({'error': 'Submission error'})


@auth_view.errorhandler(400)
def bad_request(error):
    ''' handle bad request error '''
    return jsonify({'message': 'Bad request'}), 400

@auth_view.errorhandler(401)
def unauthorized(error):
    ''' handle unautorized '''
    return jsonify({'message': 'Unauthorized'}), 401

@auth_view.errorhandler(500)
def internal_server_error(error):
    ''' handle internal server error '''
    return jsonify({'message': 'Internal server error'}), 500
