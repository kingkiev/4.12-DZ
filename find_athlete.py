import datetime

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

def connect_db():
	engine = sa.create_engine(DB_PATH)
	Base.metadata.create_all(engine)
	session = sessionmaker(engine)
	return session()

class User(Base):
	__tablename__ = 'user'
	id = sa.Column(sa.Integer, primary_key=True)
	first_name = sa.Column(sa.Text)
	last_name = sa.Column(sa.Text)
	gender = sa.Column(sa.Text)
	email = sa.Column(sa.Text)
	birthdate = sa.Column(sa.Text)
	height = sa.Column(sa.REAL)

class Athelete(Base):
	__tablename__ = 'athelete'
	id = sa.Column(sa.Integer, primary_key=True)
	age = sa.Column(sa.Integer)
	name = sa.Column(sa.Text)
	weight = sa.Column(sa.Integer)
	gender = sa.Column(sa.Text)
	birthdate = sa.Column(sa.Text)
	height = sa.Column(sa.REAL)
	gold_medals = sa.Column(sa.Integer)
	silver_medals = sa.Column(sa.Integer)
	bronze_medals = sa.Column(sa.Integer)
	total_medals = sa.Column(sa.Integer)
	sport = sa.Column(sa.Text)
	country = sa.Column(sa.Text)

def find_birthday(birthday, session):
	query = session.query(Athelete).filter(Athelete.birthdate != 0).all()
	id_ath = None
	delta_min = datetime.timedelta(days=999999)
	for id_a in query:
		birthday_a = datetime.datetime.strptime(id_a.birthdate, '%Y-%m-%d').date()
		delta_bithday = abs(birthday - birthday_a)
		if delta_bithday < delta_min:
			delta_min = delta_bithday
			id_ath = id_a.id
	target = session.query(Athelete).filter(Athelete.id == id_ath).first()
	id = id_ath
	name = target.name
	birthdate = target.birthdate
	delta_min = delta_min.days
	return (id, name, birthdate, delta_min)

def find_height(height, session):
	query = session.query(Athelete).filter(Athelete.height != 0).all()
	id_ath = None
	delta_min = 2
	for id_a in query:
		height_a = id_a.height
		delta_height = abs(height - height_a)
		if delta_height < delta_min:
			delta_min = delta_height
			id_ath = id_a.id
	target = session.query(Athelete).filter(Athelete.id == id_ath).first()
	id = id_ath
	name = target.name
	height_t = target.height
	return (id, name, height_t, delta_min)

def main():
	session = connect_db()
	id_in = input("Введите id пользователя, который Вас интересует: ")
	query = session.query(User).filter(User.id == id_in).first()
	if query:
		print ("Выбранный пользователь:")
		print ("{} {}, дата рождения - {}, рост - {}".format(query.first_name, query.last_name, query.birthdate, query.height))
		birthday = datetime.datetime.strptime(query.birthdate, '%Y-%m-%d').date()
		height = query.height
		print ("Ближайший атлет по дате рождения:")
		id, name, birthdate, delta_min = find_birthday(birthday, session)
		print ("id:{}, {}, {}. Разница дней - {}".format(id, name, birthdate, delta_min))
		id, name, height_t, delta_height = find_height(height, session)
		print ("Ближайший атлет по росту:")
		print ("id:{}, {}, {}. Разница в росте - {}".format(id, name, height_t, delta_height))

	else:
		print ("Пользователь с таким id не найден")
	
if __name__ == '__main__':
	main()