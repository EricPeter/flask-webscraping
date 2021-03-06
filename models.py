from sqlalchemy import Column, Integer, String ,Float
from database import Base
from flask_login import UserMixin

class Products(Base):
    __tablename__ = 'Products'
    id = Column(Integer, primary_key=True)
    product_name = Column(String(120))
    product_desc = Column(String(120))
    product_price = Column(String())
    image=Column(String(300))
    product_discount = Column(String(100))
    
    def __init__(self, product_name,product_desc,product_price,image,product_discount):
        self.product_name = product_name
        self.product_desc = product_desc
        self.product_price = product_price
        self.image = image
        self.product_discount=product_discount
class Phones(Base):
    __tablename__ = 'Phones'
    id = Column(Integer, primary_key=True)
    product_name = Column(String(120))
    product_desc = Column(String(120))
    product_price = Column(String())
    image=Column(String(300))
    product_discount = Column(String(100))
    
    def __init__(self, product_name,product_desc,product_price,image,product_discount):
        self.product_name = product_name
        self.product_desc = product_desc
        self.product_price = product_price
        self.image = image
        self.product_discount=product_discount

class Fashion(Base):
    __tablename__ = 'Fashion'
    id = Column(Integer, primary_key=True)
    product_name = Column(String(120))
    product_desc = Column(String(120))
    product_price = Column(String())
    image=Column(String(300))
    product_discount = Column(String(100))
    
    def __init__(self, product_name,product_desc,product_price,image,product_discount):
        self.product_name = product_name
        self.product_desc = product_desc
        self.product_price = product_price
        self.image = image
        self.product_discount=product_discount

class Bucket(Base):
    __tablename__='Bucket'
    id = Column(Integer, primary_key=True)
    product_name = Column(String(120))
    product_desc = Column(String(120))
    product_price = Column(String(120))
    username=Column(String(120))
    image=Column(String(300))

    def __init__(self, product_name,product_desc,product_price,image,username):
        self.product_name = product_name
        self.product_desc = product_desc
        self.product_price = product_price
        self.image = image
        self.username=username


class Login(UserMixin,Base):
    __tablename__='Login'
    id = Column(Integer, primary_key=True)
    Email = Column(String(120))
    Password= Column(String(120))
    def __init__(self,Email,Password):
        self.Email= Email
        self.Password = Password