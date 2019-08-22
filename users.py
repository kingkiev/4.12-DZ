import uuid
import datetime

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class User(Base):
	__tablename__ = 'user'
	id = sa.Column(sa.Integer, primary_key=True)
	first_name = sa.Column(sa.Text)
	last_name = sa.Column(sa.Text)
	gender = sa.Column(sa.Text)
	email = sa.Column(sa.Text)
	birthdate = sa.Column(sa.Text)
	height = sa.Column(sa.REAL)

class UserId(Base):
	__tablename__ = 'sqlite_sequence'
	name = sa.Column(sa.Text, primary_key=True)
	seq = sa.Column(sa.Integer)

def connect_db():
	engine = sa.create_engine(DB_PATH)
	Base.metadata.create_all(engine)
	session = sessionmaker(engine)
	return session()

def request_data(id_seq):
	print("Введите свои данные!")
	first_name = input("Введите свое имя: ")
	last_name = input("Введите свою фамилию: ")
	gender = input("Введите свой пол: ")
	email = input("Введите адрес электронной почты: ")
	birthdate = input("Введите дату рождения в формате ГГГГ-ММ-ДД: ")
	height = input("Введите свой рост: ")
	
	user = User(
		id = id_seq,
		first_name = first_name,
		last_name = last_name,
		gender = gender,
		email = email,
		birthdate = birthdate,
		height = height
		)
	return user

def user_id_update(session):
	"""
	Обновляет максимальный id в таблице sqlite_sequence.
	Этот же id и присваивается пользователю.
	"""
	user_id_entry = session.query(UserId).filter(UserId.name == 'user').first()
	if user_id_entry is None:
		user_id_entry = UserId(name='user', seq=0)
	user_id_entry.seq += 1
	return user_id_entry.seq

def main():
	session = connect_db()
	user = request_data(user_id_update(session))
	session.add(user)
	session.commit()
	print("Спасибо, данные сохранены!")

if __name__ == '__main__':
	main()