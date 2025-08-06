-- database_setup.sql - 간단한 버전 (아이디 기반)

-- admin001 사용자의 간단한 일정 데이터
-- JSON 형태로 저장하거나 간단한 테이블 구조 사용

-- 방법 1: 간단한 일정 테이블 (추천)
CREATE TABLE IF NOT EXISTS simple_schedules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    schedule_date DATE NOT NULL,
    title VARCHAR(200) NOT NULL,
    schedule_time TIME,
    color VARCHAR(7) DEFAULT '#2196f3',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_date (user_id, schedule_date)
);

-- admin001 사용자의 샘플 일정 삽입
INSERT INTO simple_schedules (user_id, schedule_date, title, schedule_time, color) VALUES
('admin001', '2025-08-06', '🎨 디자인 작업', '09:00:00', '#2196f3'),
('admin001', '2025-08-07', '🤝 클라이언트 미팅', '14:00:00', '#4caf50'),
('admin001', '2025-08-08', '📚 스터디 모임', '10:30:00', '#ff9800'),
('admin001', '2025-08-09', '🍗 친구들과 치킨', '19:00:00', '#f44336'),
('admin001', '2025-08-10', '💪 헬스장 운동', '07:00:00', '#9c27b0'),
('admin001', '2025-08-11', '🔧 프로토타입 제작', '15:00:00', '#2196f3');

-- 방법 2: JSON 필드 사용 (선택사항)
-- ALTER TABLE users ADD COLUMN schedule_data JSON;
-- UPDATE users SET schedule_data = '[
--   {"date":"2025-08-06","title":"🎨 디자인 작업","time":"09:00","color":"#2196f3"},
--   {"date":"2025-08-07","title":"🤝 클라이언트 미팅","time":"14:00","color":"#4caf50"}
-- ]' WHERE username = 'admin001';

-- 결과 확인
SELECT '=== admin001 사용자 일정 확인 ===' as message;
SELECT * FROM simple_schedules WHERE user_id = 'admin001' ORDER BY schedule_date, schedule_time;