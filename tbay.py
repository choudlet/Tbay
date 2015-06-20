from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Numeric, Table, ForeignKey
from sqlalchemy.orm import relationship

engine = create_engine('postgresql://christopherhoudlette:action@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

user_bid_table = Table('user_bid_association', Base.metadata,
	Column('user_id', Integer, ForeignKey('users.id')),
	Column('bids.id', Integer, ForeignKey('bids.id'))
)

class Item(Base):
	__tablename__ = "items"
	def __repr__(self):
		return self.name

	
	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	description = Column(String)
	start_time = Column(DateTime, default=datetime.utcnow)
	
	seller_id = Column(Integer, ForeignKey('users.id'), nullable=False)
	
class User(Base):
	__tablename__ = "users"
	
	id = Column(Integer, primary_key=True)
	username = Column(String, nullable=False)
	password = Column(String, nullable=False)
	
	items = relationship('Item', backref='users')
	bids = relationship("Bid", secondary='user_bid_association', backref='users')
		
class Bid(Base):
	__tablename__ = "bids"
	id = Column(Integer, primary_key=True)
	price = Column(Numeric, nullable=False)
	item = Column(String, ForeignKey('items.name'), nullable = False)
	
Base.metadata.create_all(engine)