from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets
import string

# database.py에서 db를 import
from models.database import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(1), nullable=False)  # 'M' or 'F'
    
    # 계정 상태
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(100), unique=True, nullable=True)
    verification_token_expires = db.Column(db.DateTime, nullable=True)
    
    # 비밀번호 재설정
    reset_token = db.Column(db.String(100), unique=True, nullable=True)
    reset_token_expires = db.Column(db.DateTime, nullable=True)
    
    # 타임스탬프
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        """비밀번호 해싱"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """비밀번호 확인"""
        return check_password_hash(self.password_hash, password)
    
    def generate_verification_code(self):
        """6자리 인증번호 생성"""
        code = ''.join(secrets.choice(string.digits) for _ in range(6))
        self.verification_token = code
        self.verification_token_expires = datetime.utcnow() + timedelta(minutes=10)
        return code
    
    def generate_reset_token(self):
        """비밀번호 재설정 토큰 생성"""
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        return self.reset_token
    
    def is_verification_token_valid(self, token):
        """인증 토큰 유효성 검사"""
        if not self.verification_token or not self.verification_token_expires:
            return False
        return (self.verification_token == token and 
                datetime.utcnow() < self.verification_token_expires)
    
    def is_reset_token_valid(self, token):
        """재설정 토큰 유효성 검사"""
        if not self.reset_token or not self.reset_token_expires:
            return False
        return (self.reset_token == token and 
                datetime.utcnow() < self.reset_token_expires)
    
    def clear_verification_token(self):
        """인증 토큰 삭제"""
        self.verification_token = None
        self.verification_token_expires = None
    
    def clear_reset_token(self):
        """재설정 토큰 삭제"""
        self.reset_token = None
        self.reset_token_expires = None
    
    def __repr__(self):
        return f'<User {self.username}>'