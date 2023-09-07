from flask_script import Manager
from app import db

# 创建一个 Speaker 类，包含以下字段： name, bio, linkedin URL
class Speaker(db.Model):
