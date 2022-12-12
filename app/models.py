from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime
from sqlalchemy import text
from app import db, login
from app.utils import safe_div


class utcnow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, server_default=utcnow())

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gwg_ref_id = db.Column(db.Integer, index=True, unique=True, nullable=False)
    gwg_res_id = db.Column(db.Integer, index=True, nullable=False)
    bkg_ref = db.Column(db.String(50), index=True, nullable=False)
    operator_code = db.Column(db.String(10), nullable=False)
    guest_name = db.Column(db.String(100), nullable=False)
    import_date = db.Column(db.DateTime, index=True, nullable=False)
    sales_date = db.Column(db.DateTime, index=True, nullable=False)
    in_date = db.Column(db.DateTime, index=True, nullable=False)
    out_date = db.Column(db.DateTime, index=True, nullable=False)
    room = db.Column(db.String(100), nullable=False)
    meal = db.Column(db.String(24), nullable=False)
    days = db.Column(db.SmallInteger, nullable=False)
    adult = db.Column(db.SmallInteger, nullable=False)
    child = db.Column(db.SmallInteger, nullable=False)
    statu4 = db.Column(db.String(10), nullable=False)
    purchase = db.Column(db.Float(), nullable=False)
    sales = db.Column(db.Float(), nullable=False)
    operator_price = db.Column(
        db.Float(), server_default=text('0'), nullable=False)
    gwg_purchase_id = db.Column(db.Integer, nullable=False)
    gwg_purchase_name = db.Column(db.String(225), nullable=False)
    gwg_purchase_code = db.Column(db.String(225), nullable=False)
    gwg_sales_id = db.Column(db.Integer, nullable=False)
    gwg_sales_name = db.Column(db.String(225), nullable=False)
    gwg_sales_code = db.Column(db.String(225), nullable=False)
    created_at = db.Column(db.DateTime, server_default=utcnow())
    updated_at = db.Column(
        db.DateTime, server_default=utcnow(), onupdate=utcnow())
    updated_by = db.Column(db.Integer, db.ForeignKey(
        'user.id'), server_default=text('1'))
    operator_id = db.Column(db.Integer, db.ForeignKey(
        'operator.id'), nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey(
        'status.id'), server_default=text('1'))
    rates = db.relationship('BookingRate', backref='booking')

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'gwg_ref_id': self.gwg_ref_id,
            'gwg_res_id': self.gwg_res_id,
            'bkg_ref': self.bkg_ref,
            'operator_code': self.operator_code,
            'guest_name': self.guest_name,
            'import_date': self.import_date,
            'sales_date': self.sales_date,
            'in_date': self.in_date,
            'out_date': self.out_date,
            'room': self.room,
            'meal': self.meal,
            'days': self.days,
            'adult': self.adult,
            'child': self.child,
            'statu4': self.statu4,
            'purchase': self.purchase,
            'sales': self.sales,
            'operator_price': self.operator_price,
            'gwg_purchase_id': self.gwg_purchase_id,
            'gwg_purchase_name': self.gwg_purchase_name,
            'gwg_purchase_code': self.gwg_purchase_code,
            'gwg_sales_id': self.gwg_sales_id,
            'gwg_sales_name': self.gwg_sales_name,
            'gwg_sales_code': self.gwg_sales_code,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'updated_by': self.updated_by,
            'operator_id': self.operator_id,
            'hotel_id': self.hotel_id,
            'status_id': self.status_id,
            'rates': [
                x.to_dict for x in BookingRate.query.filter(BookingRate.reserv_id == self.id).order_by(BookingRate.e_date)
            ]
        }


class BookingRate(db.Model):
    reserv_id = db.Column(db.Integer, db.ForeignKey(
        'booking.id'), primary_key=True)
    e_date = db.Column(db.DateTime, primary_key=True)
    base_rate = db.Column(db.Float(), server_default=text("0"))
    adult_supp = db.Column(db.Float(), server_default=text("0"))
    child_supp = db.Column(db.Float(), server_default=text("0"))
    adult_meal = db.Column(db.Float(), server_default=text("0"))
    child_meal = db.Column(db.Float(), server_default=text("0"))
    peak_supp = db.Column(db.Float(), server_default=text("0"))
    extras = db.Column(db.Float(), server_default=text("0"))
    base_rate_disc = db.Column(db.Float(), server_default=text("0"))
    adult_supp_disc = db.Column(db.Float(), server_default=text("0"))
    child_supp_disc = db.Column(db.Float(), server_default=text("0"))
    meal_disc = db.Column(db.Float(), server_default=text("0"))
    peak_supp_disc = db.Column(db.Float(), server_default=text("0"))
    extras_disc = db.Column(db.Float(), server_default=text("0"))
    mark_up = db.Column(db.Float(), server_default=text("0"))
    gwg_purchase_id = db.Column(db.Integer, server_default=text("0"))
    gwg_purchase_code = db.Column(db.String(225))
    gwg_sales_id = db.Column(db.Integer, server_default=text("0"))
    gwg_sales_code = db.Column(db.String(225))

    @property
    def to_dict(self):
        return {
            'reserv_id': self.reserv_id,
            'e_date': self.e_date,
            'base_rate': self.base_rate,
            'adult_supp': self.adult_supp,
            'child_supp': self.child_supp,
            'adult_meal': self.adult_meal,
            'child_meal': self.child_meal,
            'peak_supp': self.peak_supp,
            'extras': self.extras,
            'base_rate_disc': f'{(safe_div(self.base_rate_disc, self.base_rate) / 100):.0%}',
            'adult_supp_disc': f'{(safe_div(self.adult_supp_disc, self.adult_supp) / 100):.0%}',
            'child_supp_disc': f'{(safe_div(self.child_supp_disc, self.child_supp) / 100):.0%}',
            'meal_disc': f'{(safe_div(self.meal_disc, (self.adult_meal + self.child_meal)) / 100):.0%}',
            'peak_supp_disc': f'{(safe_div(self.peak_supp_disc, self.peak_supp) / 100):.0%}',
            'extras_disc': f'{(safe_div(self.extras_disc, self.extras) / 100):.0%}',
            'mark_up': self.mark_up,
            'gwg_purchase_id': self.gwg_purchase_id,
            'gwg_purchase_code': self.gwg_purchase_code,
            'gwg_sales_id': self.gwg_sales_id,
            'gwg_sales_code': self.gwg_sales_code
        }


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    bookings = db.relationship('Booking', backref='status', lazy=True)

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Operator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    short_name = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(2), nullable=False)
    bookings = db.relationship('Booking', backref='operator', lazy=True)

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.short_name
        }


class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    country = db.Column(db.String(2), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    purchase_manager_id = db.Column(
        db.String(2), db.ForeignKey('purchase_manager.id'))
    bookings = db.relationship('Booking', backref='hotel', lazy=True)
    mapping = db.relationship('HotelMapping', backref='hotel', lazy=True)

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class HotelMapping(db.Model):
    hotel_id = db.Column(db.Integer, db.ForeignKey(
        'hotel.id'), primary_key=True)
    gwg_hotel_id = db.Column(db.Integer, primary_key=True)
    gwg_hotel_name = db.Column(db.String(120), nullable=False)


class PurchaseManager(db.Model):
    id = db.Column(db.String(2), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    hotels = db.relationship('Hotel', backref='manager', lazy=True)
