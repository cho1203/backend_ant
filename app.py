from flask import Flask, render_template, redirect, url_for, session
from flask_login import LoginManager, current_user, logout_user
from dotenv import load_dotenv
from routes.main import main as main_bp
# 🔧 chat_bp import를 여기서 제거하고 함수 내부로 이동
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
    
    # 🆕 블루프린트 등록 (순서 중요!)
    from routes.auth import auth
    from routes.api import api
    
    # 🔧 chat_routes import를 여기로 이동하고 디버깅 추가
    try:
        print("🔄 chat_routes.py 임포트 시도 중...")
        from routes.chat_routes import chat_bp
        print("✅ chat_routes.py 임포트 성공!")
    except Exception as e:
        print(f"❌ chat_routes.py 임포트 오류: {e}")
        import traceback
        print(f"🔍 상세 오류: {traceback.format_exc()}")
        # 임시로 빈 Blueprint 생성 (에러 방지)
        from flask import Blueprint
        chat_bp = Blueprint('chat_bp_temp', __name__)
    
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(api)
    app.register_blueprint(main_bp)
    
    # 🔧 chat_bp 등록을 별도로 처리
    try:
        app.register_blueprint(chat_bp)
        print("✅ chat_bp Blueprint 등록 성공!")
    except Exception as e:
        print(f"❌ chat_bp Blueprint 등록 오류: {e}")
    
    # 메인 라우트 - 무조건 로그인 페이지로 (강제 로그아웃)
    @app.route('/')
    def index():
        # 모든 세션 데이터 삭제
        session.clear()
        # 강제 로그아웃
        logout_user()
        # 로그인 페이지로 리다이렉트
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
    
    # 🆕 데이터베이스 초기화 (SimpleSchedule 모델 포함) - 완전 수정된 부분
    with app.app_context():
        from models.user import User
        from routes.api import SimpleSchedule  # 🆕 SimpleSchedule 모델 임포트
        
        # 🆕 모든 테이블 생성 (User + SimpleSchedule)
        db.create_all()
        print("🗄️ 데이터베이스 테이블 생성 완료")
        
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
        
        # 🆕 테스트 일정 데이터 생성 (개발용) - 완전히 새로 작성
        try:
            existing_schedules = SimpleSchedule.query.filter_by(user_id='admin001').count()
            print(f"🔍 기존 일정 개수: {existing_schedules}")
            
            if existing_schedules == 0:
                from datetime import date, time
                
                sample_schedules = [
                    {
                        'user_id': 'admin001',
                        'schedule_date': date(2025, 8, 6),
                        'title': '🎨 디자인 작업',
                        'schedule_time': time(9, 0),
                        'color': '#2196f3',
                        'description': 'UI 디자인 작업'
                    },
                    {
                        'user_id': 'admin001',
                        'schedule_date': date(2025, 8, 7),
                        'title': '🤝 클라이언트 미팅',
                        'schedule_time': time(14, 0),
                        'color': '#4caf50',
                        'description': '프로젝트 논의'
                    },
                    {
                        'user_id': 'admin001',
                        'schedule_date': date(2025, 8, 8),
                        'title': '📚 스터디 모임',
                        'schedule_time': time(10, 30),
                        'color': '#ff9800',
                        'description': '기술 스터디'
                    },
                    {
                        'user_id': 'admin001',
                        'schedule_date': date(2025, 8, 9),
                        'title': '🍗 친구들과 치킨',
                        'schedule_time': time(19, 0),
                        'color': '#f44336',
                        'description': '친구 모임'
                    },
                    {
                        'user_id': 'admin001',
                        'schedule_date': date(2025, 8, 10),
                        'title': '💪 헬스장 운동',
                        'schedule_time': time(7, 0),
                        'color': '#9c27b0',
                        'description': '주말 운동'
                    },
                    {
                        'user_id': 'admin001',
                        'schedule_date': date(2025, 8, 13),
                        'title': '🏥 병원 방문',
                        'schedule_time': time(15, 30),
                        'color': '#ff5722',
                        'description': '정기 검진'
                    },
                    {
                        'user_id': 'admin001',
                        'schedule_date': date(2025, 8, 15),
                        'title': '🎬 영화 관람',
                        'schedule_time': time(20, 0),
                        'color': '#673ab7',
                        'description': '친구와 영화보기'
                    }
                ]
                
                # 각 일정을 하나씩 추가하면서 로그 출력
                for i, schedule_data in enumerate(sample_schedules, 1):
                    schedule = SimpleSchedule(**schedule_data)
                    db.session.add(schedule)
                    print(f"📅 [{i}/{len(sample_schedules)}] 테스트 일정 추가: {schedule_data['title']} ({schedule_data['schedule_date']}) {schedule_data['schedule_time']}")
                
                # 모든 일정을 한 번에 커밋
                db.session.commit()
                print(f"✅ 테스트 일정 {len(sample_schedules)}개 생성 완료!")
                
                # 생성된 일정 검증
                created_schedules = SimpleSchedule.query.filter_by(user_id='admin001').count()
                print(f"🔍 생성 후 일정 개수: {created_schedules}")
                
            else:
                print(f"ℹ️ 기존 일정이 {existing_schedules}개 있으므로 테스트 일정을 생성하지 않습니다.")
                
                # 기존 일정 목록 출력 (개발 참고용)
                existing_list = SimpleSchedule.query.filter_by(user_id='admin001').order_by(SimpleSchedule.schedule_date).all()
                print("📋 기존 일정 목록:")
                for schedule in existing_list:
                    print(f"   - {schedule.title} ({schedule.schedule_date})")
                    
        except Exception as e:
            print(f"❌ 테스트 일정 생성 오류: {e}")
            import traceback
            print(f"🔍 상세 오류: {traceback.format_exc()}")
            db.session.rollback()
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("🚀 ANT TOGETHER 서버 시작!")
    print("📍 접속 주소: http://127.0.0.1:5000")
    print("👤 테스트 계정: admin001 / admin123!")
    print("📅 테스트 일정이 자동으로 생성됩니다!")
    app.run(debug=True, host='0.0.0.0', port=5000)