from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

# 확장 객체들을 여기서 생성
db = SQLAlchemy()
mail = Mail()