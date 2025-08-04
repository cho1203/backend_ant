# create_sample_data.py - 간단한 버전 (아이디 기반)

import sys
import os
from datetime import datetime, date
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app

def create_simple_sample_data():
    print("=== 🎯 간단한 샘플 데이터 생성 시작 ===")
    
    app = create_app()
    
    with app.app_context():
        try:
            from models.database import db
            from models.user import User
            
            # admin001 사용자용 간단한 일정 데이터 (JSON 형태)
            sample_schedules = {
                'admin001': [  # 사용자 ID
                    {
                        'date': '2025-08-06',
                        'title': '🎨 디자인 작업',
                        'time': '09:00',
                        'color': '#2196f3'
                    },
                    {
                        'date': '2025-08-07', 
                        'title': '🤝 클라이언트 미팅',
                        'time': '14:00',
                        'color': '#4caf50'
                    },
                    {
                        'date': '2025-08-08',
                        'title': '📚 스터디 모임',
                        'time': '10:30', 
                        'color': '#ff9800'
                    },
                    {
                        'date': '2025-08-09',
                        'title': '🍗 친구들과 치킨',
                        'time': '19:00',
                        'color': '#f44336'
                    }
                ]
            }
            
            # 사용자 확인
            user = User.query.filter_by(username='admin001').first()
            if user:
                # 사용자의 일정 데이터를 JSON으로 저장 (간단한 방법)
                # 실제로는 별도 테이블이나 JSON 필드에 저장할 수 있음
                print(f"✅ 사용자 {user.username}의 일정 데이터:")
                
                for schedule in sample_schedules['admin001']:
                    print(f"   - {schedule['date']}: {schedule['title']} ({schedule['time']})")
                
                # 여기서 실제 데이터베이스에 저장하거나
                # JSON 파일로 저장할 수 있음
                import json
                with open('sample_schedules.json', 'w', encoding='utf-8') as f:
                    json.dump(sample_schedules, f, ensure_ascii=False, indent=2)
                
                print("✅ sample_schedules.json 파일로 저장 완료!")
                
            else:
                print("❌ admin001 사용자를 찾을 수 없습니다.")
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    create_simple_sample_data()