from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Enum
import enum
db = SQLAlchemy()

class Ptype(enum.Enum):
    OFFER = "OFFER"
    CATEGORY = "CATEGORY"

class abs_product(db.Model):
    __abstract__=True
    name = db.Column(db.String())
    type = db.Column(Enum(Ptype), nullable=False)
    price = db.Column(db.Integer)
    path = db.Column(db.Text, index=True)

class Product(abs_product):
    __tablename__ = "products"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parentId = db.Column(UUID(as_uuid=True), db.ForeignKey("products.id", ondelete='CASCADE'))
    isupdated = db.Column(db.Boolean,default=False)
    date = db.Column(db.DateTime(timezone=True))
    Children = db.relationship(
        'Product',
        cascade="all",
        backref=db.backref("Parent", remote_side='Product.id'),
    )
    def __init__(self,id,name,parentId,type,price,date,path):
        self.id = id
        self.name = name
        self.parentId = parentId
        self.type = type
        self.price = price
        self.date = date
        self.path = path

class Update(abs_product):
    __tablename__ = "updates"
    id = db.Column(UUID(as_uuid=True), db.ForeignKey("products.id", ondelete='CASCADE'),primary_key=True)
    date =  db.Column(db.DateTime(timezone=True),primary_key=True)
    parentId = db.Column(UUID(as_uuid=True), db.ForeignKey("products.id", ondelete='CASCADE'))
    rebased = db.Column(db.Boolean, default=False)
    def __init__(self,id,name,parentId,type,price,date,path):
        self.id = id
        self.name = name
        self.parentId = parentId
        self.type = type
        self.price = price
        self.date = date
        self.path = path