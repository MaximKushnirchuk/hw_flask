import os

POSTGRES_USER = os.getenv('POSTGRES_USER', 'app')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'secret')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'app')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5431')

PG_DNS = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

# ДЕЛАЕМ ДВИЖОК
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker
import atexit

engine = create_engine(PG_DNS)
Session = sessionmaker(bind=engine)
atexit.register(engine.dispose)

#  СОЗДАЕМ ТАБЛИЦЫ
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
import datetime
				
class Base(DeclarativeBase):
	pass
					
class User(Base):
    __tablename__ = 'app_users'   
							
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, 	index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(50), unique=True, 	nullable=False) 

    @property 
    def make_dict(self):
        user_data = {	
			'id': self.id,	
			'name': self.name,	
			'password': self.password
			}		
        return user_data

class Advertisement(Base):
    __tablename__ = 'app_advertisement'   

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(40))
    description: Mapped[str] = mapped_column(String(200))
    created: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    owner: Mapped[int] = mapped_column(ForeignKey('app_users.id'))

    @property 
    def make_dict(self):
        adv_data = {	
			'id': self.id,	
			'title': self.title,	
			'description': self.description,
            'created': self.created,
            'owner': self.owner
			}		
        return adv_data

Base.metadata.create_all(bind=engine)