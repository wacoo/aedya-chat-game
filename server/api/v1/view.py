from flask import Blueprint, jsonify, request, current_app
from models.base import session
from models.users import User
from models.chats import Chats
from models.games import Games
from auth.auth import TokenAuth
from sqlalchemy import or_

view = Blueprint('view', __name__)
auth = TokenAuth()

@view.route('/', methods=['GET', 'POST'])
#@auth.requires_token
def home():
   ''' home page '''
   email = 'wabaham9@gmail.com'#request.json.get("email")    
   #games = session.query(Games).all()
   chats = session.query(Chats).filter(or_(Chats.sent_from == email, Chats.sent_to == email)).all()
   #user_data['chatentials'] = chats
   #user_data['games'] = games
   chat_lst = []
   for chat in chats:
      chat_dict = {}
      chat_dict['chat'] = chat.__dict__['chat']
      chat_dict['created_at'] = str(chat.__dict__['created_at'])
      chat_dict['updated_at'] = str(chat.__dict__['updated_at'])
      chat_dict['sent_from'] = chat.__dict__['sent_from']
      chat_dict['sent_to'] = chat.__dict__['sent_to']
      chat_lst.append(chat_dict)
      return jsonify({'status': 200, 'chats': chat_lst})