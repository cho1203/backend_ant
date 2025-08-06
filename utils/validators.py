import re

def get_user_model():
    from models.user import User
    return User

class Validators:
    @staticmethod
    def validate_username(username):
        """아이디 유효성 검사"""
        errors = []
        
        if not username:
            errors.append("아이디를 입력해주세요.")
        elif len(username) < 4:
            errors.append("아이디는 4자 이상이어야 합니다.")
        elif len(username) > 20:
            errors.append("아이디는 20자 이하여야 합니다.")
        elif not re.match(r'^[a-zA-Z0-9_]+$', username):
            errors.append("아이디는 영문, 숫자, 언더스코어(_)만 사용 가능합니다.")
        else:
            User = get_user_model()
            if User.query.filter_by(username=username).first():
                errors.append("이미 사용 중인 아이디입니다.")
        
        return errors
    
    @staticmethod
    def validate_password(password):
        """비밀번호 유효성 검사"""
        errors = []
        
        if not password:
            errors.append("비밀번호를 입력해주세요.")
        elif len(password) < 8:
            errors.append("비밀번호는 8자 이상이어야 합니다.")
        elif len(password) > 50:
            errors.append("비밀번호는 50자 이하여야 합니다.")
        elif not re.search(r'[A-Za-z]', password):
            errors.append("비밀번호에 영문자가 포함되어야 합니다.")
        elif not re.search(r'\d', password):
            errors.append("비밀번호에 숫자가 포함되어야 합니다.")
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("비밀번호에 특수문자가 포함되어야 합니다.")
        
        return errors
    
    @staticmethod
    def validate_email(email):
        """이메일 유효성 검사"""
        errors = []
        
        if not email:
            errors.append("이메일을 입력해주세요.")
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append("올바른 이메일 형식이 아닙니다.")
        else:
            User = get_user_model()
            if User.query.filter_by(email=email).first():
                errors.append("이미 가입된 이메일입니다.")
        
        return errors
    
    @staticmethod
    def validate_phone(phone):
        """전화번호 유효성 검사"""
        errors = []
        
        if not phone:
            errors.append("전화번호를 입력해주세요.")
        elif not re.match(r'^01[0-9]-\d{4}-\d{4}$', phone):
            errors.append("전화번호는 010-0000-0000 형식으로 입력해주세요.")
        
        return errors
    
    @staticmethod
    def validate_signup_data(data):
        """회원가입 데이터 전체 유효성 검사"""
        all_errors = []
        
        all_errors.extend(Validators.validate_username(data.get('username', '')))
        all_errors.extend(Validators.validate_password(data.get('password', '')))
        all_errors.extend(Validators.validate_email(data.get('email', '')))
        all_errors.extend(Validators.validate_phone(data.get('phone', '')))
        
        if not data.get('gender') or data.get('gender') not in ['M', 'F']:
            all_errors.append("성별을 선택해주세요.")
        
        # 비밀번호 확인
        if data.get('password') != data.get('password_confirm'):
            all_errors.append("비밀번호가 일치하지 않습니다.")
        
        return all_errors