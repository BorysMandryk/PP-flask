import enum
from sqlalchemy import create_engine, Integer, Float, Column, String, Text, Boolean, DateTime, ForeignKey, Enum, MetaData
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.engine import URL
connection_string = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:online-pharmacy.database.windows.net,1433;Database=online-pharmacy-main;Uid=web;Pwd=Pp123456;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})

engine = create_engine(connection_url)
metadata = MetaData()
Base: DeclarativeMeta = declarative_base(metadata)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class RoleEnum(enum.Enum):
    provisor = 0
    user = 1


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    patronymic = Column(String(50))
    phone = Column(String(10))
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    address = Column(String(255))
    orders = relationship('Order', back_populates='users', cascade="all, delete-orphan")

    def get_role(self):
        return self.role


class Medication(Base):
    __tablename__ = "medications"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text())
    cost = Column(Float)
    quantity = Column(Integer)
    on_sale = Column(Boolean, nullable=False)

    products = relationship('Product', back_populates='medications', cascade="all, delete-orphan")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    created_at = Column(DateTime, nullable=False)
    completed = Column(Boolean, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    users = relationship('User', back_populates='orders')

    products = relationship('Product', back_populates='orders', cascade="all, delete-orphan")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    amount = Column(Integer, nullable=False)

    med_id = Column(Integer, ForeignKey('medications.id'), nullable=False)
    medications = relationship('Medication', back_populates='products')

    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    orders = relationship('Order', back_populates='products')

