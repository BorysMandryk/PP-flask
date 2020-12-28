import enum
from sqlalchemy import create_engine, Integer, Float, Column, String, Boolean, ForeignKey, Enum
from sqlalchemy.dialects.mysql import TINYTEXT
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('mysql+pymysql://lab:password@localhost:3306/pplab?charset=utf8mb4')
Base: DeclarativeMeta = declarative_base()
Session = sessionmaker(bind=engine)


class RoleEnum(enum.Enum):
    provisor = 0
    user = 1


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255))
    username = Column(String(255))
    password_hash = Column(String(255))
    role = Column(Enum(RoleEnum))
    orders = relationship('Order', back_populates='users', cascade="all, delete-orphan")
    demands = relationship('Demand', back_populates='users', cascade="all, delete-orphan")
    """user_orders = relationship("Orders", back_populates="user")
    med_orders = relationship("Orders", back_populates="med")
    user_demands = relationship("Demands", back_populates="user")
    med_demands = relationship('Demands', back_populates="med")"""

    def get_role(self):
        return self.role


class Medication(Base):
    __tablename__ = "medications"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(TINYTEXT)
    cost = Column(Float)
    quantity = Column(Integer)
    in_stock = Column(Boolean)

    orders = relationship('Order', back_populates='medications', cascade="all, delete-orphan")
    demands = relationship('Demand', back_populates='medications', cascade="all, delete-orphan")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    completed = Column(Boolean)

    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship('User', back_populates='orders')

    med_id = Column(Integer, ForeignKey('medications.id'))
    medications = relationship('Medication', back_populates='orders')
    """
    user = relationship("Users", back_populates="user_orders")
    med_id = Column(Integer, ForeignKey('medications.med_id'))
    med = relationship("Medications", back_populates="med_orders")"""


class Demand(Base):
    __tablename__ = "demand"
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)

    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship('User', back_populates='demands')

    med_id = Column(Integer, ForeignKey('medications.id'))
    medications = relationship('Medication', back_populates='demands')
    """user_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship("Users", back_populates="user_demands")
    med_id = Column(Integer, ForeignKey('medications.med_id'))
    med = relationship("Medications", back_populates="med_demands")"""
