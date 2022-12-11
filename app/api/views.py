from flask import request, abort
from app.models import User, Booking, Hotel, Operator, Status, BookingRate
from app.api import api
from app import db
from app.api.utils import build_filter, get_dates


@api.post('/booking')
def api_booking():
    query = Booking.query.join(Hotel)

    # filter
    filter_model = request.get_json()['filterModel']
    if filter_model:
        filter = build_filter(filter_model, Booking)
        query = query.filter(db.and_(*filter))

    total_rows = query.count()

    query = query.order_by(Hotel.name, Booking.in_date, Booking.gwg_ref_id)

    # infinite scroll
    if 'startRow' in request.get_json():
        start = request.get_json()['startRow']
        length = request.get_json()['endRow']

        query = query.limit(length - start).offset(start)

    return {
        'data': [bkg.to_dict for bkg in query],
        'total_rows': total_rows,
    }


@api.route('/booking/rate', methods=['GET', 'POST'])
def api_rate():
    id = request.get_json()['id']

    if not id:
        abort(400)

    query = Booking.query.get(id)

    for dt in get_dates(query.in_date, query.out_date):
        db.session.add(BookingRate(reserv_id=id, e_date=dt))

    db.session.commit()

    data = BookingRate.query.filter_by(reserv_id=id)
    return {
        'data': [x.to_dict for x in data],
    }


@api.route('/hotel', methods=['GET', 'POST'])
def api_hotel():

    return {
        'data': [x.to_dict for x in Hotel.query]
    }


@api.route('/operator', methods=['GET', 'POST'])
def api_operator():

    return {
        'data': [x.to_dict for x in Operator.query]
    }


@api.route('/status', methods=['GET', 'POST'])
def api_status():

    return {
        'data': [x.to_dict for x in Status.query]
    }
