from sqlalchemy import Column,Integer,String,Float,JSON,Text,ForeignKey
from src.config.database import Base
class User(Base):
 __tablename__='users'
 id=Column(Integer,primary_key=True);email=Column(String(100),unique=True);password=Column(String(200));role=Column(String(20))
class Sample(Base):
 __tablename__='samples'
 id=Column(Integer,primary_key=True);hour=Column(String(30),unique=True,nullable=False);pressure=Column(Float);flow=Column(Float);temperature=Column(Float);machines=Column(Integer);sensor_noise=Column(Float);kwh=Column(Float);note=Column(Text,default='')
class Run(Base):
 __tablename__='runs'
 id=Column(Integer,primary_key=True);name=Column(String(100));features=Column(JSON);alphas=Column(JSON);state=Column(String(20),default='queued');result=Column(JSON);error=Column(Text,default='')
class Review(Base):
 __tablename__='reviews'
 id=Column(Integer,primary_key=True);run_id=Column(Integer,ForeignKey('runs.id'));title=Column(String(100));finding=Column(Text);action=Column(Text);status=Column(String(20),default='draft')
class Audit(Base):
 __tablename__='audits'
 id=Column(Integer,primary_key=True);actor=Column(String(100));action=Column(String(200));created=Column(String(40))
