from models.base import session, engine, Base
from models.users import User
from models.chats import Chats
from models.games import Games
from models.oppnent import Opponent

Base.metadata.create_all(bind=engine)

# Create a new user
# user = User(fname='John', lname='Doe', email='johndoe@example.com', password='123', country='X', total_score=0)
# session.add(user)
# session.commit()
'''
user2 = User(email='wabaham9@gmail.com', fname='Wondmagegn', lname='Chosha', country='Kenya', score=0, password='123')
session.add(user2)
#session.commit()

user3 = User(email='albert@gmail.com', fname='Albert', lname='David', country='Nigeria', score=0, password='123')
session.add(user3)
session.commit()
user4 = User(email='solomon@gmail.com', fname='Solomon', lname='Kane', country='South Africa', score=0, password='123')
session.add(user4)'''
#session.commit()


#Chat
'''chat1 = Chats(chat='Hi albert, how is the day going? I am having some problem with the project. Can you help?', sent_from='wabaham9@gmail.com', sent_to='albert@gmail.com')
session.add(chat1)
session.commit()
chat2 = Chats(chat='Sorry man, I am in bit fo trouble. I can not.', sent_from='albert@gmail.com', sent_to='wabaham9@gmail.com')
session.add(chat2)
session.commit()'''
'''
u1 = session.query(User).filter_by(email='wabaham9@gmail.com').all()
u2 = session.query(User).filter_by(email='aboanarges@gmail.com').all()'''

'''for us in u1:
    us.delete()
for us in u2:
    us.delete() 
session.commit()
'''

# create a new credential for the user
'''credential = Credential(url='https://facebook.com', username='wac', password='wac123', name='Facebook', user_email='wabaham9@gmail.com', auto_fill=False)
session.add(credential)
session.commit()

# create a new note for the user
note = Note(title='My Capstone Project', content='This is  my capstone project.', user_email='wabaham9@gmail.com')
session.add(note)
session.commit()

# create a new credential for the user
credential = Credential(url='https://facebook.com', username='johndoe', password='secret', name='Facebook', auto_fill=True, user_email='aboanarges@gmail.com')
session.add(credential)
session.commit()

# create a new note for the user
note = Note(title='Presidential schedule', content='Monday 8:00AM, breakfast.', user_email='aboanarges@gmail.com')
session.add(note)
session.commit()

# create a new credential for the user
credential = Credential(url='https://twitter.com', username='johndoe', password='secret', name='Twitter', auto_fill=True, user_email='aboanarges@gmail.com')
session.add(credential)
session.commit()

# create a new note for the user
note = Note(title='Example Note', content='Example data', user_email='wabaham9@gmail.com')
session.add(note)
session.commit()

'''
# update the user's password
'''user.password = 'newpassword456'
session.commit()
'''
'''# delete the credential
cred = session.query(Credential).all()
note = session.query(Note).all()

for c in cred:
    session.delete(c)
for n in note:
    session.delete(n)'''

'''user = session.query(User).all()
for u in user:
    session.delete(u) 
session.commit()'''

'''session.delete(credential)
session.commit()

# delete the user and all associated credentials and notes
session.delete(user)
session.commit() '''