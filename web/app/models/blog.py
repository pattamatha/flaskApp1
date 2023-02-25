# Lab11_microblog

from app import db
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime


# SerializerMixin ใช้แปลงข้อมูลที่ดึงมาจาก Data base
# ให้กลายเป็นข้อมูล dict ใช้ใน python
class BlogEntry(db.Model, SerializerMixin):
    __tablename__ = "blog_entries"

    id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(50))
    message = db.Column(db.String(280))
    #email = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # constructor
    def __init__(self, message):
        #self.name = name
        self.message = message
        #self.email = email
    
    def update(self, message):
        #self.name = name
        self.message = message
        #self.email = email