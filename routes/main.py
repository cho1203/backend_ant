from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

main = Blueprint('main_routes', __name__)

@main.route('/calendar')
@login_required
def calendar():
    """캘린더 메인 페이지"""
    return render_template('main_calendar.html', user=current_user)

@main.route('/profile')
@login_required
def profile():
    """사용자 프로필 페이지"""
    return render_template('profile.html', user=current_user)

@main.route('/chat')
@login_required
def chat():
    """AI 채팅 페이지"""
    return render_template('chat_engine.html', user=current_user)

@main.route('/community')
@login_required
def community():
    """커뮤니티 페이지"""
    return render_template('ccommunity.html', user=current_user)

# 🆕 비밀게시판 라우트 추가
@main.route('/community/secret')
@login_required
def community_secret():
    """비밀게시판 페이지"""
    return render_template('community_list.html', 
                         board_name='비밀게시판',
                         user=current_user)

# 🆕 다른 게시판들도 필요하면 추가
@main.route('/community/free')
@login_required
def community_free():
    """자유게시판 페이지"""
    return render_template('community_list.html', 
                         board_name='자유게시판',
                         user=current_user)

@main.route('/community/politics')
@login_required
def community_politics():
    """정치게시판 페이지"""
    return render_template('community_list.html', 
                         board_name='정치게시판',
                         user=current_user)

@main.route('/community/restaurant')
@login_required
def community_restaurant():
    """맛집게시판 페이지"""
    return render_template('community_list.html', 
                         board_name='맛집게시판',
                         user=current_user)

@main.route('/community/<board_type>/post/<int:post_id>')
@login_required
def community_post_detail(board_type, post_id):
    """게시글 상세보기 페이지"""
    # 게시판 타입에 따른 이름 매핑
    board_names = {
        'secret': '비밀게시판',
        'free': '자유게시판', 
        'politics': '정치게시판',
        'restaurant': '맛집게시판'
    }
    
    board_name = board_names.get(board_type, '게시판')
    
    return render_template('community_public.html', 
                         board_name=board_name,
                         board_type=board_type,
                         post_id=post_id,
                         user=current_user)