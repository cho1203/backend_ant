print("🔥🔥🔥 chat_routes.py 파일 로드됨! 🔥🔥🔥")

from flask import Blueprint, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# 🔧 API 키 디버깅 추가
api_key = os.getenv("OPENAI_API_KEY")
print(f"🔑 API 키 확인: {api_key[:10]}...{api_key[-5:] if api_key else 'None'}")

if not api_key:
    raise ValueError("OPENAI_API_KEY가 .env에 설정되지 않았습니다.")

client = OpenAI(api_key=api_key)
chat_bp = Blueprint("chat_bp", __name__)

@chat_bp.route("/api/messages", methods=["POST"])
def save_message():
    print("🔍 API 요청 받음!")  # 요청 확인 로그
    
    data = request.get_json()
    user_message = data.get("message", "").strip()
    
    print(f"📨 사용자 입력: {user_message}")  # 입력 확인 로그

    if not user_message:
        print("❌ 빈 메시지")
        return jsonify({"error": "메시지가 비어 있습니다."}), 400

    try:
        print("🤖 GPT API 호출 시작...")
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_message}],
            max_tokens=1024,
            temperature=0.7,
        )
        
        print(f"✅ GPT API 응답 받음!")
        
        ai_reply = response.choices[0].message.content if response.choices else "AI 응답이 없습니다."
        
        print(f"💬 GPT 최종 응답: {ai_reply}")
        
        return jsonify({"reply": ai_reply})
        
    except Exception as e:
        print(f"❌ GPT 호출 오류: {e}")
        print(f"🔍 오류 타입: {type(e)}")
        import traceback
        print(f"🔍 상세 오류: {traceback.format_exc()}")
        
        return jsonify({"error": f"GPT 호출 중 오류가 발생했습니다: {str(e)}"}), 500