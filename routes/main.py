from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

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