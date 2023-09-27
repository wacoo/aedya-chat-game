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
   email = request.args.get("email")
   print('DDDD', email)
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