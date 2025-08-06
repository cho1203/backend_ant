from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
import logging

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """로그인 처리 - 기존 login.html 그대로 사용"""
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.calendar'))
    
    if request.method == 'POST':
        # 기존 HTML의 input name에 맞춰서 받기
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        # remember = bool(request.form.get('remember'))
        
        if not username or not password:
            flash('아이디와 비밀번호를 모두 입력해주세요.')
            return render_template('login.html')
        
        from models.user import User
        from models.database import db
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if not user.is_verified:
                flash('이메일 인증을 완료해주세요.')
                session['unverified_user_id'] = user.id
                return redirect(url_for('auth.verify_email'))
            
            login_user(user, remember=False)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            flash(f'환영합니다, {user.username}님!')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main_routes.calendar'))
        else:
            flash('아이디 또는 비밀번호가 잘못되었습니다.')
    
    return render_template('login.html')

@auth.route('/signup', methods=['GET'])
def signup():
    # """소셜 회원가입 선택 화면 - 기존 new_login.html 활용"""
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.calendar'))
    
    return render_template('new_login.html')

@auth.route('/signup/form', methods=['GET', 'POST'])
def signup_form():
    # """실제 회원가입 폼 처리"""
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.calendar'))
    
    if request.method == 'POST':
        data = {
            'username': request.form.get('username', '').strip(),
            'password': request.form.get('password', ''),
            'password_confirm': request.form.get('password_confirm', ''),
            'email': request.form.get('email', '').strip().lower(),
            'phone': request.form.get('phone', '').strip(),
            'gender': request.form.get('gender', '')
        }
        
        # 유효성 검증
        from utils.validators import Validators
        errors = Validators.validate_signup_data(data)
        if errors:
            for error in errors:
                flash(error)
            return render_template('signup_form.html', form_data=data)
        
        try:
            from models.user import User
            from models.database import db
            
            # 새 사용자 생성
            user = User(
                username=data['username'],
                email=data['email'],
                phone_number=data['phone'],
                gender=data['gender']
            )
            user.set_password(data['password'])
            
            db.session.add(user)
            db.session.commit()
            
            # 인증 이메일 발송
            from utils.email_service import EmailService
            verification_code = EmailService.send_verification_email(user)
            db.session.commit()
            
            session['unverified_user_id'] = user.id
            flash(f'회원가입이 완료되었습니다! 이메일로 발송된 6자리 인증번호를 입력해주세요.')
            return redirect(url_for('auth.verify_email'))
            
        except Exception as e:
            from models.database import db
            db.session.rollback()
            flash('회원가입 중 오류가 발생했습니다. 다시 시도해주세요.')
            logging.error(f"회원가입 오류: {str(e)}")
            return render_template('signup_form.html', form_data=data)
    
    return render_template('signup_form.html')

@auth.route('/verify-email', methods=['GET', 'POST'])
def verify_email():
    """이메일 인증 처리"""
    user_id = session.get('unverified_user_id')
    if not user_id:
        flash('잘못된 접근입니다.')
        return redirect(url_for('auth.login'))
    
    from models.user import User
    from models.database import db
    
    user = User.query.get(user_id)
    if not user:
        flash('사용자를 찾을 수 없습니다.')
        return redirect(url_for('auth.login'))
    
    if user.is_verified:
        flash('이미 인증된 계정입니다.')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        verification_code = request.form.get('verification_code', '').strip()
        
        if user.is_verification_token_valid(verification_code):
            user.is_verified = True
            user.clear_verification_token()
            db.session.commit()
            
            session.pop('unverified_user_id', None)
            flash('이메일 인증이 완료되었습니다! 이제 로그인하실 수 있습니다.')
            return redirect(url_for('auth.login'))
        else:
            flash('인증번호가 잘못되었거나 만료되었습니다.')
    
    return render_template('verify_email.html', email=user.email)

@auth.route('/resend-verification', methods=['POST'])
def resend_verification():
    """인증 이메일 재발송"""
    user_id = session.get('unverified_user_id')
    if not user_id:
        return jsonify({'success': False, 'message': '잘못된 접근입니다.'})
    
    from models.user import User
    from models.database import db
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': '사용자를 찾을 수 없습니다.'})
    
    try:
        from utils.email_service import EmailService
        verification_code = EmailService.send_verification_email(user)
        db.session.commit()
        return jsonify({'success': True, 'message': '인증 이메일이 재발송되었습니다.'})
    except Exception as e:
        return jsonify({'success': False, 'message': '이메일 발송에 실패했습니다.'})

@auth.route('/find-id', methods=['GET', 'POST'])
def find_id():
    """아이디 찾기"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        
        if not email:
            flash('이메일을 입력해주세요.')
            return render_template('find_id.html')
        
        from models.user import User
        user = User.query.filter_by(email=email).first()
        
        if user:
            try:
                from utils.email_service import EmailService
                masked_username = EmailService.send_id_recovery_email(user)
                flash(f'입력하신 이메일로 아이디 정보를 발송했습니다. (아이디: {masked_username})')
            except Exception as e:
                flash('이메일 발송에 실패했습니다. 다시 시도해주세요.')
        else:
            flash('등록되지 않은 이메일입니다.')
    
    return render_template('find_id.html')

@auth.route('/find-password', methods=['GET', 'POST'])
def find_password():
    """비밀번호 찾기"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        
        if not username or not email:
            flash('아이디와 이메일을 모두 입력해주세요.')
            return render_template('find_password.html')
        
        from models.user import User
        from models.database import db
        
        user = User.query.filter_by(username=username, email=email).first()
        
        if user:
            try:
                from utils.email_service import EmailService
                reset_token = EmailService.send_password_reset_email(user)
                db.session.commit()
                flash('비밀번호 재설정 링크가 이메일로 발송되었습니다.')
                return redirect(url_for('auth.login'))
            except Exception as e:
                flash('이메일 발송에 실패했습니다. 다시 시도해주세요.')
        else:
            flash('입력하신 정보와 일치하는 계정이 없습니다.')
    
    return render_template('find_password.html')

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """비밀번호 재설정"""
    from models.user import User
    from models.database import db
    
    user = User.query.filter_by(reset_token=token).first()
    
    if not user or not user.is_reset_token_valid(token):
        flash('유효하지 않거나 만료된 링크입니다.')
        return redirect(url_for('auth.find_password'))
    
    if request.method == 'POST':
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        from utils.validators import Validators
        password_errors = Validators.validate_password(new_password)
        if password_errors:
            for error in password_errors:
                flash(error)
            return render_template('reset_password.html', token=token)
        
        if new_password != confirm_password:
            flash('비밀번호가 일치하지 않습니다.')
            return render_template('reset_password.html', token=token)
        
        user.set_password(new_password)
        user.clear_reset_token()
        db.session.commit()
        
        flash('비밀번호가 성공적으로 변경되었습니다.')
        return redirect(url_for('auth.login'))
    
    return render_template('reset_password.html', token=token)

@auth.route('/logout')
@login_required
def logout():
    """로그아웃 처리"""
    logout_user()
    #flash('로그아웃되었습니다.')
    return redirect(url_for('auth.login'))