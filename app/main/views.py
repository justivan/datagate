from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from datetime import datetime
from app.main import main
from app import db


@main.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@main.route('/')
@main.route('/index')
def index():
    return render_template('layout.html')

@main.route('/booking')
@login_required
def booking():
    return render_template('grid/bookings.html')
