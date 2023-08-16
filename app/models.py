from datetime import datetime
from time import time
from app import db, login, app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

import jwt

# Định nghĩa lớp User kế thừa từ UserMixin và db.Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # Biểu diễn đối tượng User dưới dạng chuỗi
    def __repr__(self):
        return '<User {}>'.format(self.username)

    # Phương thức để đặt password hash cho người dùng
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Phương thức để kiểm tra xem password được cung cấp có khớp với hash lưu trữ hay không
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Phương thức để tạo mã token cho việc đặt lại mật khẩu
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    # Phương thức tĩnh để xác minh và giải mã token đặt lại mật khẩu
    @staticmethod
    def verify_reset_password_token(token):
        try:
            idd = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(idd)

# Hàm tải người dùng cho Flask-Login từ cơ sở dữ liệu
@login.user_loader
def load_user(idd):
    return User.query.get(int(idd))
