from flask_mail import Message
from flask import current_app, url_for, render_template_string

class EmailService:
    @staticmethod
    def send_verification_email(user):
        """이메일 인증 코드 발송"""
        try:
            from models.database import mail
            
            verification_code = user.generate_verification_code()
            
            msg = Message(
                subject='ANT TOGETHER - 이메일 인증',
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[user.email]
            )
            
            # HTML 이메일 템플릿
            html_template = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body { 
                        font-family: 'Montserrat', Arial, sans-serif; 
                        background-color: #111; 
                        color: #fff; 
                        margin: 0; 
                        padding: 20px; 
                    }
                    .container { 
                        max-width: 600px; 
                        margin: 0 auto; 
                        background: #0E0E0E; 
                        padding: 30px; 
                        border-radius: 30px; 
                        box-shadow: 0 0 20px rgba(255, 255, 255, 0.2); 
                    }
                    .header { 
                        text-align: center; 
                        margin-bottom: 30px; 
                    }
                    .logo { 
                        font-size: 2.3rem; 
                        font-weight: bold; 
                        color: #fff; 
                        line-height: 1.2;
                    }
                    .code { 
                        font-size: 32px; 
                        font-weight: bold; 
                        color: #fff; 
                        text-align: center; 
                        padding: 20px; 
                        background: #333; 
                        border-radius: 25px; 
                        margin: 20px 0; 
                        letter-spacing: 5px;
                    }
                    .footer { 
                        margin-top: 30px; 
                        font-size: 14px; 
                        color: #aaa; 
                        text-align: center; 
                    }
                    p { color: #fff; line-height: 1.6; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <div class="logo">ANT<br>TOGETHER</div>
                        <h2 style="color: #fff;">이메일 인증</h2>
                    </div>
                    <p>안녕하세요, <strong>{{ username }}</strong>님!</p>
                    <p>ANT TOGETHER에 가입해주셔서 감사합니다.</p>
                    <p>아래 인증번호를 입력하여 이메일 인증을 완료해주세요:</p>
                    <div class="code">{{ verification_code }}</div>
                    <p><strong>인증번호는 10분 후 만료됩니다.</strong></p>
                    <div class="footer">
                        <p>본 메일은 발신전용이며, 문의사항은 고객센터를 이용해주세요.</p>
                        <p>&copy; 2025 ANT TOGETHER. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            msg.html = render_template_string(html_template, 
                                            username=user.username,
                                            verification_code=verification_code)
            
            msg.body = f"""
ANT TOGETHER 이메일 인증

안녕하세요, {user.username}님!

가입해주셔서 감사합니다.
아래 인증번호를 입력하여 인증을 완료해주세요:

인증번호: {verification_code}

인증번호는 10분 후 만료됩니다.

ANT TOGETHER 팀 드림
            """
            
            mail.send(msg)
            return verification_code
            
        except Exception as e:
            current_app.logger.error(f"이메일 발송 실패: {str(e)}")
            raise e
    
    @staticmethod
    def send_password_reset_email(user):
        """비밀번호 재설정 이메일 발송"""
        try:
            from models.database import mail
            
            reset_token = user.generate_reset_token()
            reset_url = url_for('auth.reset_password', token=reset_token, _external=True)
            
            msg = Message(
                subject='ANT TOGETHER - 비밀번호 재설정',
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[user.email]
            )
            
            html_template = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body { 
                        font-family: 'Montserrat', Arial, sans-serif; 
                        background-color: #111; 
                        color: #fff; 
                        margin: 0; 
                        padding: 20px; 
                    }
                    .container { 
                        max-width: 600px; 
                        margin: 0 auto; 
                        background: #0E0E0E; 
                        padding: 30px; 
                        border-radius: 30px; 
                        box-shadow: 0 0 20px rgba(255, 255, 255, 0.2); 
                    }
                    .button { 
                        display: inline-block; 
                        padding: 12px 24px; 
                        background-color: #fff; 
                        color: #000; 
                        text-decoration: none; 
                        border-radius: 25px; 
                        margin: 20px 0; 
                        font-weight: bold;
                    }
                    .warning { color: #ff6b6b; font-weight: bold; }
                    h2 { color: #fff; }
                    p { color: #fff; line-height: 1.6; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>비밀번호 재설정</h2>
                    <p>안녕하세요, <strong>{{ username }}</strong>님!</p>
                    <p>비밀번호 재설정을 요청하셨습니다.</p>
                    <p>아래 버튼을 클릭하여 새 비밀번호를 설정해주세요:</p>
                    <a href="{{ reset_url }}" class="button">비밀번호 재설정</a>
                    <p class="warning">이 링크는 1시간 후 만료됩니다.</p>
                    <p>만약 비밀번호 재설정을 요청하지 않으셨다면, 이 메일을 무시해주세요.</p>
                </div>
            </body>
            </html>
            """
            
            msg.html = render_template_string(html_template,
                                            username=user.username,
                                            reset_url=reset_url)
            
            msg.body = f"""
ANT TOGETHER 비밀번호 재설정

안녕하세요, {user.username}님!

비밀번호 재설정을 요청하셨습니다.
아래 링크를 클릭하여 새 비밀번호를 설정해주세요:

{reset_url}

이 링크는 1시간 후 만료됩니다.
요청하지 않으셨다면 이 메일을 무시해주세요.

ANT TOGETHER 팀 드림
            """
            
            mail.send(msg)
            return reset_token
            
        except Exception as e:
            current_app.logger.error(f"비밀번호 재설정 이메일 발송 실패: {str(e)}")
            raise e
    
    @staticmethod
    def send_id_recovery_email(user):
        """아이디 찾기 이메일 발송"""
        try:
            from models.database import mail
            
            msg = Message(
                subject='ANT TOGETHER - 아이디 찾기',
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[user.email]
            )
            
            # 보안을 위해 아이디 일부만 표시
            masked_username = user.username[:2] + '*' * (len(user.username) - 2)
            
            msg.body = f"""
ANT TOGETHER 아이디 찾기

요청하신 계정의 아이디는 다음과 같습니다:

아이디: {masked_username}

전체 아이디를 확인하시려면 고객센터로 문의해주세요.

ANT TOGETHER 팀 드림
            """
            
            mail.send(msg)
            return masked_username
            
        except Exception as e:
            current_app.logger.error(f"아이디 찾기 이메일 발송 실패: {str(e)}")
            raise e