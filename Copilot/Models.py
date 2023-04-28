from flask_script import Manager
from app import db

# 创建一个 Speaker 类，包含以下字段： name, bio, linkedin URL
class Speaker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    bio = db.Column(db.String(256))
    linkedin = db.Column(db.String(128))

    def __repr__(self):
        return '<Speaker %r>' % self.name