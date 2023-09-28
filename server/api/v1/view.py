from flask import Blueprint, jsonify, request, current_app
from models.base import session
from models.users import User
from models.chats import Chats
from models.games import Games
from auth.auth import TokenAuth
from sqlalchemy import or_, and_
import random

view = Blueprint('view', __name__)
auth = TokenAuth()

@view.route('/', methods=['GET'])
#@auth.requires_token
def home():
   ''' home page '''
   try:
      email1 = request.args.get("email1")
      email2 = request.args.get("email2")
      #games = session.query(Games).all()
      chats = session.query(Chats).filter(or_(and_(Chats.sent_from == email1, Chats.sent_to == email2), and_(Chats.sent_from == email2, Chats.sent_to == email1))).all()
      #user_data['chatentials'] = chats
      #user_data['games'] = games
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
   except Exception as e:
      session.rollback()
      return jsonify({"error": 'e'})

@view.route('/send', methods=['POST'])
#@auth.requires_token
def send_chat():
   ''' stores chat to database '''
   try:
      sent_from = request.json.get("sent_from"),
      sent_to = request.json.get("sent_to"),
      msg = request.json.get("msg"),
      print(sent_from, sent_to, msg)
      chat1 = Chats(chat= msg, sent_from=sent_from, sent_to=sent_to)
      session.add(chat1)
      session.commit()

      return jsonify({'message': 'Sent'})
   except Exception as e:
      session.rollback()
      return jsonify({'error': 'Error: Message not sent'})
   
@view.route('/newgame', methods=['POST'])
#@auth.requires_token
def new_game():
   ''' create a new game '''
   try:
      player1_email = request.json.get("player1")
      country = request.json.get("country")
      all_users = session.query(User.email).filter(User.country == country).all()
      player2_email = random.choice(all_users)[0]

      print('P1', player1_email)
      all_users = session.query(User.email).filter(User.country == country).all()
      all_emails = [user[0] for user in all_users if user[0] != player1_email]
      player2_email = random.choice(all_emails)
      #Update previous game
      game_to_update = session.query(Games).filter(Games.done == False, Games.player1 == player1_email).first()
      if game_to_update:
         game_to_update.done = True
         game_to_update.winner = random.choice([player1_email, player2_email])
         session.commit()
         print("Game updated successfully.")
      else:
         print("No game found where done is False.")

      game1 = Games(name= 'AEDYA', description='At the end of the day you are alone.', player1=player1_email, player2=player2_email, winner='', done=False)
      session.add(game1)
      session.commit()

      return jsonify({'message': 'Game created', 'game_id': game1.id, 'opponent': player2_email})
   except Exception as e:
      #session.rollback()
      return jsonify({'error': 'Error: Game not created' + str(e)})

@view.route('/getgame', methods=['GET'])
#@auth.requires_token
def getGame():
   ''' get game '''
   try:
      email = request.args.get("email")
      #games = session.query(Games).all()
      game1 = session.query(Games).filter(or_(Games.player1 == email, Games.player2 == email), Games.done == False).first()
      opponent = ''
      
      if game1:
         if game1.player2 == email:
            opponent = game1.player1
         elif game1.player1 == email:
            opponent = game1.player2
         return {'message': 'Game found', 'game_id': game1.id, 'opponent': opponent} #jsonify({'id':game1.id, 'player1': game1.player1, 'player2': game1.player2})
      else:
         return jsonify({'error': 'No game in progress'})
      session.commit()
   except Exception as e:
      session.rollback()
      return jsonify({'error': 'Can\'t get game data!'})

@view.route('/updatecount', methods=['PUT'])
#@auth.requires_token
def update_count():
   ''' update chat count '''
   try:
      game_id = request.json.get('game_id')
      game = session.query(Games).filter(Games.id == game_id).first()
      game.chat_count += 1
      session.commit()
      return jsonify({'message': 'Update successful!', 'count': game.chat_count})
   except Exception as e:
      session.rollback()
      return jsonify({'error': 'Update not successful: ' + e})

@view.route('/addeval', methods=['PUT'])
#@auth.requires_token
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
   except Exception as e:
      session.rollback()
      return jsonify({'error': 'Update not successful: ' + str(e)})


@view.route('/addscore', methods=['PUT'])
#@auth.requires_token
def add_score():
   ''' add score '''
   try:
      game_id = request.json.get('game_id')
      game = session.query(Games).filter(Games.id == game_id).first()
      player1_review = game.player1_review
      player2_review = game.player2_review

      if player1_review < 0 or player2_review < 0:
         return jsonify({'error': 'Review not complete!', 'success': False})

      player1_review = max(player1_review, 0)
      player2_review = max(player2_review, 0)

      if player1_review == player2_review:
         player1_score = 1
         player2_score = 1
      else:
         if player1_review == 1:
               player1_score = 0
               player2_score = 3
         else:
               player1_score = 3
               player2_score = 0

      print(player1.total_score + player1_score)
      player1 = session.query(User).filter(User.email == game.player1).first()
      player1.total_score += player1_score

      player2 = session.query(User).filter(User.email == game.player2).first()
      player2.total_score += player2_score

      session.commit()
      return ({'message': 'Score added successfully!', 'scores': {player1.email: player1.total_score, player2.email: player2.total_score}, 'success': True  })
   except Exception as e:
      session.rollback()
      return jsonify({'error': 'Score not added! ' + str(e)})
   
@view.route('/getuser', methods=['GET'])
#@auth.requires_token
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
            # ...include other attributes as needed
         }
      session.commit()
      return jsonify(user_data)
   except Exception as e:
      session.rollback()
      return jsonify({'error': 'Can\'t load data for ' + email})

