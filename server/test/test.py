from models.base import session, engine, Base
from models.users import User
from models.credentials import Credential
from models.notes import Note

# create a new user
'''user = User(fname='John', lname='Doe', email='johndoe@example.com', password='123')
session.add(user)
session.commit()

user2 = User(fname='Wondmagegn', lname='Chosha', email='wabaham9@gmail.com', password='123')
session.add(user2)
session.commit()

user3 = User(fname='Bishaw', lname='Abraham', email='aboanarges@gmail.com', password='321')
session.add(user3)
session.commit()

u1 = session.query(User).filter_by(email='wabaham9@gmail.com').all()
u2 = session.query(User).filter_by(email='aboanarges@gmail.com').all()'''

'''for us in u1:
    us.delete()
for us in u2:
    us.delete() 
session.commit()'''

# create a new credential for the user
credential = Credential(url='https://facebook.com', username='wac', password='wac123', name='Facebook', user_email='wabaham9@gmail.com', auto_fill=False)
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
user.password = 'newpassword456'
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