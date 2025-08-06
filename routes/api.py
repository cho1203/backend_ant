from flask import Blueprint, request, jsonify, session
from flask_login import login_required, current_user
from models.database import db
from dotenv import load_dotenv
from datetime import datetime, date, time
import logging
import os

# Blueprint 생성
api = Blueprint('api', __name__, url_prefix='/api')

# 🆕 SimpleSchedule 모델 정의 (app.py에서 임포트하므로 여기 정의)
class SimpleSchedule(db.Model):
    __tablename__ = 'simple_schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False, index=True)
    schedule_date = db.Column(db.Date, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    schedule_time = db.Column(db.Time, nullable=True)
    color = db.Column(db.String(7), default='#2196f3')
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.schedule_date.strftime('%Y-%m-%d'),
            'title': self.title,
            'time': self.schedule_time.strftime('%H:%M') if self.schedule_time else '',
            'color': self.color,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# 🆕 현재 사용자 정보 API
@api.route('/current-user', methods=['GET'])
@login_required
def get_current_user():
    """현재 로그인한 사용자 정보 반환"""
    try:
        return jsonify({
            'success': True,
            'username': current_user.username,
            'email': current_user.email,
            'phone_number': current_user.phone_number
        })
    except Exception as e:
        logging.error(f"사용자 정보 조회 오류: {e}")
        return jsonify({'success': False, 'error': '사용자 정보를 가져올 수 없습니다.'}), 500

# 🆕 사용자 일정 목록 조회 API
@api.route('/schedules/<user_id>', methods=['GET'])
@login_required
def get_user_schedules(user_id):
    """특정 사용자의 모든 일정 조회"""
    try:
        # 현재 사용자만 자신의 일정을 볼 수 있도록 권한 체크
        if current_user.username != user_id:
            return jsonify({'success': False, 'error': '권한이 없습니다.'}), 403
        
        # 사용자의 모든 일정 조회
        schedules = SimpleSchedule.query.filter_by(user_id=user_id).order_by(
            SimpleSchedule.schedule_date.asc(),
            SimpleSchedule.schedule_time.asc()
        ).all()
        
        # JSON으로 변환
        schedule_list = [schedule.to_dict() for schedule in schedules]
        
        logging.info(f"✅ 사용자 {user_id}의 일정 {len(schedule_list)}개 조회 완료")
        return jsonify(schedule_list)
        
    except Exception as e:
        logging.error(f"일정 조회 오류 (사용자: {user_id}): {e}")
        return jsonify({'success': False, 'error': '일정을 불러올 수 없습니다.'}), 500

# 🆕 새 일정 추가 API
@api.route('/schedules', methods=['POST'])
@login_required
def create_schedule():
    """새로운 일정 생성"""
    try:
        data = request.get_json()
        
        # 필수 데이터 검증
        if not data:
            return jsonify({'success': False, 'error': '데이터가 없습니다.'}), 400
        
        title = data.get('title', '').strip()
        date_str = data.get('date', '').strip()
        
        if not title:
            return jsonify({'success': False, 'error': '일정 제목은 필수입니다.'}), 400
        
        if not date_str:
            return jsonify({'success': False, 'error': '날짜는 필수입니다.'}), 400
        
        # 날짜 파싱
        try:
            schedule_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'success': False, 'error': '올바른 날짜 형식이 아닙니다. (YYYY-MM-DD)'}), 400
        
        # 시간 파싱 (선택사항)
        schedule_time = None
        time_str = data.get('time', '').strip()
        if time_str:
            try:
                schedule_time = datetime.strptime(time_str, '%H:%M').time()
            except ValueError:
                return jsonify({'success': False, 'error': '올바른 시간 형식이 아닙니다. (HH:MM)'}), 400
        
        # 새 일정 생성
        new_schedule = SimpleSchedule(
            user_id=current_user.username,
            schedule_date=schedule_date,
            title=title,
            schedule_time=schedule_time,
            color=data.get('color', '#2196f3'),
            description=data.get('description', '').strip()
        )
        
        # 데이터베이스에 저장
        db.session.add(new_schedule)
        db.session.commit()
        
        logging.info(f"✅ 새 일정 생성 완료: {title} ({date_str}) - 사용자: {current_user.username}")
        
        return jsonify({
            'success': True,
            'message': '일정이 저장되었습니다.',
            'schedule': new_schedule.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"일정 생성 오류: {e}")
        return jsonify({'success': False, 'error': f'일정을 저장할 수 없습니다: {str(e)}'}), 500

# 🆕 일정 수정 API
@api.route('/schedules/<int:schedule_id>', methods=['PUT'])
@login_required
def update_schedule(schedule_id):
    """기존 일정 수정"""
    try:
        # 일정 조회
        schedule = SimpleSchedule.query.get(schedule_id)
        if not schedule:
            return jsonify({'success': False, 'error': '일정을 찾을 수 없습니다.'}), 404
        
        # 권한 체크
        if schedule.user_id != current_user.username:
            return jsonify({'success': False, 'error': '권한이 없습니다.'}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': '데이터가 없습니다.'}), 400
        
        # 데이터 업데이트
        if 'title' in data:
            schedule.title = data['title'].strip()
        if 'date' in data:
            try:
                schedule.schedule_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'success': False, 'error': '올바른 날짜 형식이 아닙니다.'}), 400
        if 'time' in data:
            if data['time']:
                try:
                    schedule.schedule_time = datetime.strptime(data['time'], '%H:%M').time()
                except ValueError:
                    return jsonify({'success': False, 'error': '올바른 시간 형식이 아닙니다.'}), 400
            else:
                schedule.schedule_time = None
        if 'color' in data:
            schedule.color = data['color']
        if 'description' in data:
            schedule.description = data['description'].strip()
        
        db.session.commit()
        
        logging.info(f"✅ 일정 수정 완료: ID {schedule_id} - 사용자: {current_user.username}")
        
        return jsonify({
            'success': True,
            'message': '일정이 수정되었습니다.',
            'schedule': schedule.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"일정 수정 오류 (ID: {schedule_id}): {e}")
        return jsonify({'success': False, 'error': '일정을 수정할 수 없습니다.'}), 500

# 🆕 일정 삭제 API
@api.route('/schedules/<int:schedule_id>', methods=['DELETE'])
@login_required
def delete_schedule(schedule_id):
    """일정 삭제"""
    try:
        # 일정 조회
        schedule = SimpleSchedule.query.get(schedule_id)
        if not schedule:
            return jsonify({'success': False, 'error': '일정을 찾을 수 없습니다.'}), 404
        
        # 권한 체크
        if schedule.user_id != current_user.username:
            return jsonify({'success': False, 'error': '권한이 없습니다.'}), 403
        
        # 삭제 실행
        db.session.delete(schedule)
        db.session.commit()
        
        logging.info(f"✅ 일정 삭제 완료: ID {schedule_id} - 사용자: {current_user.username}")
        
        return jsonify({
            'success': True,
            'message': '일정이 삭제되었습니다.'
        })
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"일정 삭제 오류 (ID: {schedule_id}): {e}")
        return jsonify({'success': False, 'error': '일정을 삭제할 수 없습니다.'}), 500

# 🆕 날짜별 일정 조회 API
@api.route('/schedules/<user_id>/<date_str>', methods=['GET'])
@login_required
def get_schedules_by_date(user_id, date_str):
    """특정 날짜의 일정 조회"""
    try:
        # 권한 체크
        if current_user.username != user_id:
            return jsonify({'success': False, 'error': '권한이 없습니다.'}), 403
        
        # 날짜 파싱
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'success': False, 'error': '올바른 날짜 형식이 아닙니다.'}), 400
        
        # 해당 날짜의 일정 조회
        schedules = SimpleSchedule.query.filter_by(
            user_id=user_id,
            schedule_date=target_date
        ).order_by(SimpleSchedule.schedule_time.asc()).all()
        
        schedule_list = [schedule.to_dict() for schedule in schedules]
        
        return jsonify({
            'success': True,
            'date': date_str,
            'schedules': schedule_list
        })
        
    except Exception as e:
        logging.error(f"날짜별 일정 조회 오류 ({user_id}, {date_str}): {e}")
        return jsonify({'success': False, 'error': '일정을 불러올 수 없습니다.'}), 500

# 🆕 에러 핸들러들
@api.errorhandler(404)
def api_not_found(error):
    return jsonify({'success': False, 'error': 'API 엔드포인트를 찾을 수 없습니다.'}), 404

@api.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'success': False, 'error': '허용되지 않는 HTTP 메서드입니다.'}), 405

@api.errorhandler(500)
def api_internal_error(error):
    db.session.rollback()
    return jsonify({'success': False, 'error': '서버 내부 오류가 발생했습니다.'}), 500
