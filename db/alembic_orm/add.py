from sqlalchemy import create_engine, Integer, Float, Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.mysql import TINYTEXT
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('mysql+pymysql://root:12345678@localhost:3306/pp?charset=utf8mb4', echo=True)
Base: DeclarativeMeta = declarative_base()
Session = sessionmaker(bind=engine)


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255))
    username = Column(String(255))
    password_hash = Column(String(255))
    orders = relationship('Orders', back_populates='users')
    demands = relationship('Demands', back_populates='users')
    """user_orders = relationship("Orders", back_populates="user")
    med_orders = relationship("Orders", back_populates="med")
    user_demands = relationship("Demands", back_populates="user")
    med_demands = relationship('Demands', back_populates="med")"""


class Medications(Base):
    __tablename__ = "medications"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(TINYTEXT)
    cost = Column(Float)
    quantity = Column(Integer)
    in_stock = Column(Boolean)

    orders = relationship('Orders', back_populates='medications')
    demands = relationship('Demands', back_populates='medications')


class Orders(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    completed = Column(Boolean)

    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship('Users', back_populates='orders')

    med_id = Column(Integer, ForeignKey('medications.id'))
    medications = relationship('Medications', back_populates='orders')
    """
    user = relationship("Users", back_populates="user_orders")
    med_id = Column(Integer, ForeignKey('medications.med_id'))
    med = relationship("Medications", back_populates="med_orders")"""


class Demands(Base):
    __tablename__ = "demand"
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)

    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship('Users', back_populates='demands')

    med_id = Column(Integer, ForeignKey('medications.id'))
    medications = relationship('Medications', back_populates='demands')
    """user_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship("Users", back_populates="user_demands")
    med_id = Column(Integer, ForeignKey('medications.med_id'))
    med = relationship("Medications", back_populates="med_demands")"""


