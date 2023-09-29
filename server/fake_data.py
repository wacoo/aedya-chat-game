from models.base import Session
from models.users import User
import datetime

session = Session()

prefixes = ['eth', 'usa', 'chi', 'ken', 'nig']

for prefix in prefixes:
    for i in range(4):
        fname = f'{prefix}_fname{i+1}'
        lname = f'{prefix}_lname{i+1}'
        country = prefix.upper()
        score = (i + 1) * 10
        email = f'{prefix}_{i+1}@example.com'
        password = f'{prefix}_password{i+1}'
        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()

        user = User(fname=fname, lname=lname, country=country, score=score, email=email, password=password)
        user.created_at = created_at
        user.updated_at = updated_at

        session.add(user)

session.commit()
session.close()