from flask import Blueprint, jsonify, request, current_app
from models.base import session
from models.users import User
from models.chats import Chats
from models.oppnent import Opponent
from models.games import Games
from auth.auth import TokenAuth
from sqlalchemy import or_, and_
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
import random

view = Blueprint('view', __name__)
auth = TokenAuth()

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

@view.route('/', methods=['GET'])
#@auth.requires_token
def home():
    ''' home page '''
    try:
        email1 = request.args.get("email1")
        email2 = request.args.get("email2")
        with session_scope() as session:
            chats = session.query(Chats).filter(
                or_(and_(Chats.sent_from == email1, Chats.sent_to == email2),
                    and_(Chats.sent_from == email2, Chats.sent_to == email1))).all()

            chat_lst = []
            for chat in chats:
                chat_dict = {}
                if chat.sent_from == email1 and chat.sent_to == email2:
                    chat_dict['direction'] = 'outgoing'
                elif chat.sent_from == email2 and chat.sent_to == email1:
                    chat_dict['direction'] = 'incoming'
                chat_dict['msg'] = chat.__dict__['chat']
                chat_dict['created_at'] = str(chat.__dict__['created_at'])
                chat_dict['updated_at'] = str(chat.__dict__['updated_at'])
                chat_dict['sent_from'] = chat.__dict__['sent_from']
                chat_dict['sent_to'] = chat.__dict__['sent_to']
                chat_lst.append(chat_dict)
            return jsonify({'status': 200, 'chats': chat_lst})
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)})

@view.route('/send', methods=['POST'])
#@auth.requires_token
def send_chat():
    ''' stores chat to database '''
    try:
        sent_from = request.json.get("sent_from")
        sent_to = request.json.get("sent_to")
        msg = request.json.get("msg")
        print(sent_from, sent_to, msg)
        chat1 = Chats(chat=msg, sent_from=sent_from, sent_to=sent_to)
        session.add(chat1)
        session.commit()

        return jsonify({'message': 'Sent'})
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': 'Error: Message not sent'})
    finally:
        session.close()

@view.route('/newgame', methods=['POST'])
@auth.requires_token
def new_game():
    ''' create a new game '''
    try:
        player1_email = request.json.get("player1")
        country = request.json.get("country")

        all_emails, all_users = get_available_users(session, player1_email, country)

        if len(all_emails) > 0:
            valid_opponents = get_valid_opponents(session, player1_email, all_emails)

            if len(valid_opponents) > 0:
                player2_email = random.choice(valid_opponents)

                session.query(Games).filter(
                    or_(Games.player1 == player1_email, Games.player2 == player1_email),
                    Games.done == False
                ).update({Games.done: True}, synchronize_session=False)

                game_id = create_new_game(session, player1_email, player2_email)

                opponent_entry = Opponent(player_email=player1_email, opponent_email=player2_email)
                session.add(opponent_entry)
                session.commit()

                return jsonify({'message': 'Game created', 'game_id': game_id, 'opponent': player2_email})
            else:
                return jsonify({'error': 'No available players. All opponents have been played.'})
        else:
            return jsonify({'error': 'No available players.'})

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': 'Error: Game not created' + str(e)})
    finally:
        session.close()

@view.route('/getgame', methods=['GET'])
@auth.requires_token
def getGame():
    ''' get game '''
    try:
        email = request.args.get("email")
        game1 = session.query(Games).filter(
            or_(Games.player1 == email , Games.player2 == email), Games.done == False).first()
        opponent = ''

        if game1:
            if game1.player2 == email:
                opponent = game1.player1
            elif game1.player1 == email:
                opponent = game1.player2
            result = {'message': 'Game found', 'game_id': game1.id, 'opponent': opponent}
        else:
            result = {'error': 'No game in progress'}

        session.commit()
        return jsonify(result)
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': 'Can\'t get game data!'})
    finally:
        session.close()

@view.route('/updatecount', methods=['PUT'])
@auth.requires_token
def update_count():
    ''' update chat count '''
    try:
        game_id = request.json.get('game_id')
        game = session.query(Games).filter(Games.id == game_id).first()
        game.chat_count += 1
        session.commit()
        return jsonify({'message': 'Update successful!', 'count': game.chat_count})
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': 'Update not successful: ' + str(e)})
    finally:
        session.close()

@view.route('/addeval', methods=['PUT'])
@auth.requires_token
def add_evaluation():
    ''' add evaluation '''
    game_id = request.json.get('game_id')
    user_email = request.json.get('email')
    review_value = request.json.get('value')

    try:
        game = session.query(Games).filter(Games.id == game_id).first()
        if user_email == game.player1:
            game.player1_review = review_value
        elif user_email == game.player2:
            game.player2_review = review_value

        session.commit()

        return jsonify({'message': 'Update successful!'})
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': 'Update not successful: ' + str(e)})
    finally:
        session.close()


@view.route('/addscore', methods=['PUT'])
@auth.requires_token
def add_score():
    ''' add score '''
    try:
        game_id = request.json.get('game_id')
        game = session.query(Games).filter(Games.id == game_id).first()
        player1_review_value = game.player1_review
        player2_review_value = game.player2_review

        if player1_review_value < 0 or player2_review_value < 0:
            return jsonify({'error': 'Review not complete!', 'success': False})

        player1_review_value = max(player1_review_value, 0)
        player2_review_value = max(player2_review_value, 0)

        player1_email, player2_email = game.player1, game.player2
        player1, player2 = session.query(User).filter(User.email.in_([player1_email, player2_email])).all()

        player1_score = player2_score = 1
        if player1_review_value == 0 and player2_review_value == 0:
            player1_score = 2
            player2_score = 2
        elif player1_review_value != player2_review_value:
            player1_score = 3 if player1_review_value == 0 else 0
            player2_score = 3 if player1_score == 0 else 0

        player1.total_score += player1_score
        player2.total_score += player2_score

        player1_country = player1.country
        all_emails = session.query(User.email).filter(User.country == player1_country, User.email.notin_([player1_email, player2_email])).all()
        all_emails = [email[0] for email in all_emails]

        games_to_update = session.query(Games).filter(
            Games.done.is_(False),
            or_(
                and_(Games.player1 == player1_email, Games.player2 == player2_email),
                and_(Games.player1 == player2_email, Games.player2 == player1_email)
            )
        ).all()

        if games_to_update:
            for game in games_to_update:
                game.done = True

            max_score_user = session.query(User.email, User.total_score).filter(User.country == player1_country).order_by(User.total_score.desc()).first()
            if max_score_user:
                for game in games_to_update:
                    game.winner = max_score_user[0]
            else:
                return jsonify({'error': 'No user with the highest score found.'})
        else:
            return jsonify({'error': 'No game in progress'})

        session.commit()

        game1 = Games(name='AEDYA', description='At the end of the day you are alone.', player1=player1_email, player2=player2_email, winner='', done=False)
        session.add(game1)
        session.commit()

        played_opponents = session.query(Opponent.opponent_email).filter(Opponent.player_email.in_([player1_email, player2_email])).distinct().all()
        played_opponents = [opponent[0] for opponent in played_opponents]
        valid_opponents = [email for email in all_emails if email not in played_opponents]

        session.close()

        return jsonify({
            'message': 'Score added successfully!',
            'scores': {player1.email: player1.total_score, player2.email: player2.total_score},
            'valid_opponents': valid_opponents,
            'success': True
        })
    except SQLAlchemyError as e:
        session.rollback()
        session.close()
        return jsonify({'error': 'Score not added: ' + str(e)})

@view.route('/getuser', methods=['GET'])
@auth.requires_token
def get_user():
    ''' get user '''
    try:
        email = request.args.get('email')
        user = session.query(User).filter(User.email == email).first()

        if user:
            user_data = {
                'email': user.email,
                'fname': user.fname,
                'lname': user.lname,
                'country': user.country,
                'total_score': user.total_score,
            }
            return jsonify(user_data)
        else:
            return jsonify({'error': 'User not found'})
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': 'Error occurred', 'message': str(e)})
    finally:
        session.commit()
        session.close()


def get_available_users(session, player1_email, country):
    '''retrieve available users from the same country as player1.'''
    try:
        all_users = session.query(User.email, User.total_score).filter(User.country == country).all()
        all_emails = [user[0] for user in all_users if user[0] != player1_email]
        session.commit()
        return all_emails, all_users
    except SQLAlchemyError as e:
        session.rollback()
        raise e
    finally:
        session.close()


def update_previous_game(session, player1_email, all_users):
    '''update the winner of the previous game with the user having the highest total score.'''
    try:
        game_to_update = session.query(Games).filter(Games.done == False, Games.player1 == player1_email).first()
        if game_to_update:
            max_score_user = max(all_users, key=lambda x: x[1])
            if max_score_user:
                game_to_update.done = True
                game_to_update.winner = max_score_user[0]
                session.commit()
                print("Game updated successfully.")
            else:
                print("No user with the highest score found.")
        else:
            print("No game found where done is False.")
    except SQLAlchemyError as e:
        session.rollback()
        raise e
    finally:
        session.close()


def create_new_game(session, player1_email, player2_email):
    ''' create a new game with player1 and player2. '''
    try:
        game1 = Games(name='AEDYA', description='At the end of the day you are alone.',
                      player1=player1_email, player2=player2_email, winner='', done=False)
        session.add(game1)
        session.commit()
        return game1.id
    except SQLAlchemyError as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_valid_opponents(session, player1_email, all_emails):
    ''' return valid opponent '''
    try:
        played_opponents = session.query(Opponent.opponent_email).filter(Opponent.player_email == player1_email).all()
        played_opponents = [opponent[0] for opponent in played_opponents]
        valid_opponents = [email for email in all_emails if email not in played_opponents]
        session.commit()
        return valid_opponents
    except SQLAlchemyError as e:
        session.rollback()
        raise e
    finally:
        session.close()
