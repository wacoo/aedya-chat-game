from flask import Blueprint, jsonify, request, current_app
from models.base import session
from models.users import User
from models.chats import Chats
from models.games import Games
from auth.auth import TokenAuth

view = Blueprint('view', __name__)
auth = TokenAuth()

@view.route('/', methods=['GET', 'POST'])
#@auth.requires_token
def home():
    ''' home page '''
    email = 'wabaham9@gmail.com'#request.json.get("email")
    with current_app.app_context():
      chat_lst = {}
      game_lst = {}
      user_data = {}
      account = {}
      chat_collection = []
      game_collection = []
      games = session.query(Games).all()
      chats = session.query(Chats).filter_by(user_email=email).all()
      #user_data['chatentials'] = chats
      #user_data['games'] = games
      for chat in chats:
         chat_lst['id'] = chat.__dict__['id']
         chat_lst['chat'] = chat.__dict__['chat']
         chat_lst['created_at'] = str(chat.__dict__['created_at'])
         chat_lst['updated_at'] = str(chat.__dict__['updated_at'])
         chat_lst['sent_to'] = str(chat.__dict__['sent_to'])
         chat_collection.append(chat_lst)
         chat_lst = {}
      user_data['chats'] = chat_collection
      for game in games:
         game_lst['id'] = game.__dict__['id']
         game_lst['name'] = game.__dict__['name']
         game_lst['description'] = game.__dict__['description']
         game_lst['created_at'] = str(game.__dict__['created_at'])
         game_lst['updated_at'] = str(game.__dict__['updated_at'])
         game_collection.append(game_lst)
         game_lst = {}
      user_data['games'] = game_collection
      return jsonify(user_data)