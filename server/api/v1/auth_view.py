import bcrypt
from flask import request, jsonify, Blueprint, current_app
from models.users import User
from models.base import session
from auth.auth import TokenAuth
from sqlalchemy.exc import SQLAlchemyError

auth_view = Blueprint('auth_view', __name__)

# Your user database and authentication logic here

@auth_view.route("/login", methods=["POST"])
def login():
    # Get the username and password from the request
    email = request.json.get("email")
    password = request.json.get("password")

    print(email, password)
    # Validate input
    if not email:
        print('1111')
        return jsonify({"message": "Email is required"}), 400
    if not password:
        print('2222')
        return jsonify({"message": "Password is required"}), 400

    # Create a TokenAuth instance for this request context
    auth = TokenAuth(current_app)

    user = session.query(User).filter_by(email=email).first()
    # Get the hash of the user's password from the database
    if not user:
        return jsonify({"message": "Invalid username or password"}), 401
    hashed_password = user.password.encode("utf-8")

    # Verify the password using bcrypt
    if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
        # Generate a token for the user
        token = auth.generate_token(user.email)

        # Return the token to the client
        return jsonify({"token": token, 'email': user.email}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

# Define a registration route
@auth_view.route('/register', methods=['POST'])
def register():
    # Get the user data from the request
    try:
        data = request.json
        email = data.get('email')
        fname = data.get('fname')
        lname = data.get('lname')
        country = data.get('country')
        score = data.get('score')
        password = data.get('password')

        # Validate input
        if not fname:
            print(11)
            return jsonify({"message": "First name is required"}), 400
        if not lname:
            print(22)
            return jsonify({"message": "Last name is required"}), 400
        # if not country:
        #     print(33)
        #     return jsonify({"message": "Country is required"}), 400
        # if not score:
        #     print(44)
        #     return jsonify({"message": "Score is required"}), 400
        if not email:
            print(55)
            return jsonify({"message": "Email is required"}), 400
        if not password:
            print(66)
            return jsonify({"message": "Password is required"}), 400

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        #salt = bcrypt.gensalt()
        #hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8'))

        # Create a new User object and add it to the database
        user = User(email=email, fname=fname, lname=lname, country=country, score=score, password=hashed_password)
        session.add(user)
        session.commit()

        # Return a success message to the client
        return jsonify({'message': 'User created successfully!'})
    except SQLAlchemyError as e:
        session.rollback();
        print(e);
        return jsonify({'error': 'Database error'})
    except Exception as e:
        session.rollback();
        print(e);
        return jsonify({'error': 'Submission error'})


# Handle errors
@auth_view.errorhandler(400)
def bad_request(error):
    return jsonify({'message': 'Bad request'}), 400

@auth_view.errorhandler(401)
def unauthorized(error):
    return jsonify({'message': 'Unauthorized'}), 401

@auth_view.errorhandler(500)
def internal_server_error(error):
    return jsonify({'message': 'Internal server error'}), 500
