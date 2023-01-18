from database import Base
from sqlalchemy import Column, String, Date, DateTime

class UserInfo(Base):
	__tablename__ = 'user'
	username = Column(String, primary_key = True)
	password = Column(String, nullable = False)
	birthday = Column(Date)
	create_time = Column(DateTime)
	last_login = Column(DateTime, nullable = True)