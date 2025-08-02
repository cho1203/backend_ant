from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from dotenv import load_dotenv
import os
import logging

# 환경변수 로드
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # 설정
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///ant_together.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 이메일 설정
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    
    # 데이터베이스와 메일 확장 초기화
    from models.database import db, mail
    db.init_app(app)
    mail.init_app(app)
    
    # Flask-Login 설정
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '로그인이 필요합니다.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from models.user import User
        return User.query.get(int(user_id))
    
    # 블루프린트 등록
    from routes.auth import auth
    from routes.main import main
    
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(main)
    
    # 메인 라우트 - 항상 로그인 페이지로
    @app.route('/')
    def index():
        # 로그인 상태와 상관없이 항상 로그인 페이지로 이동
        return redirect(url_for('auth.login'))
    
    # 간단한 에러 핸들러
    @app.errorhandler(404)
    def not_found_error(error):
        return f"""
        <div style="text-align: center; padding: 50px; font-family: Arial; background: #111; color: #fff; min-height: 100vh;">
            <h1>404 - 페이지를 찾을 수 없습니다</h1>
            <p><a href="{url_for('auth.login')}" style="color: #fff;">로그인 페이지로 돌아가기</a></p>
        </div>
        """, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from models.database import db
        db.session.rollback()
        return f"""
        <div style="text-align: center; padding: 50px; font-family: Arial; background: #111; color: #fff; min-height: 100vh;">
            <h1>500 - 서버 오류</h1>
            <p>잠시 후 다시 시도해주세요.</p>
            <p><a href="{url_for('auth.login')}" style="color: #fff;">로그인 페이지로 돌아가기</a></p>
        </div>
        """, 500
    
    # 데이터베이스 초기화
    with app.app_context():
        from models.user import User
        
        db.create_all()
        
        # 테스트 사용자 생성 (개발용)
        if not User.query.filter_by(username='admin001').first():
            test_user = User(
                username='admin001',
                email='test@example.com',
                phone_number='010-1234-5678',
                gender='M',
                is_verified=True
            )
            test_user.set_password('admin123!')
            db.session.add(test_user)
            db.session.commit()
            print("✅ 테스트 사용자 생성: admin001 / admin123!")
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("🚀 ANT TOGETHER 서버 시작!")
    print("📍 접속 주소: http://127.0.0.1:5000")
    print("👤 테스트 계정: admin001 / admin123!")
    app.run(debug=True, host='0.0.0.0', port=5000)