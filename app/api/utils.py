from datetime import datetime, timedelta, date
from decimal import Decimal, getcontext

getcontext().prec = 2


def build_filter(filter_model, object):
    filter = []
    for attr, item in filter_model.items():
        col = getattr(object, attr)

        if item['filterType'] == 'date':
            if item['type'] == 'inRange':
                col = col.between(item['dateFrom'], item['dateTo'])
            elif item['type'] == 'lessThan':
                col = col.__lt__(item['dateFrom'])
            elif item['type'] == 'greaterThan':
                col = col.__gt__(item['dateFrom'])
            else:
                col = col.__eq__(item['dateFrom'])
        elif item['filterType'] == 'number':
            if item['type'] == 'notEqual':
                col = col.__ne__(item['filter'])
            elif item['type'] == 'lessThan':
                col = col.__lt__(item['filter'])
            elif item['type'] == 'lessThanOrEqual':
                col = col.__l3__(item['filter'])
            elif item['type'] == 'greaterThan':
                col = col.__gt__(item['filter'])
            elif item['type'] == 'greaterThanOrEqual':
                col = col.__ge__(item['filter'])
            elif item['type'] == 'inRange':
                col = col.between(item['filter'], item['filterTo'])
            else:
                col = col.__eq__(item['filter'])
        else:
            col = col.in_(item['values'])

        filter.append(col)

    return filter


def get_dates(start_date, end_date):
    return (start_date + timedelta(days=i) for i in range((end_date - start_date).days))


def set_discount(query, field, data):

    if type(data[field]) == bool:
        if data[field]:
            rate_field = field.replace('_discount', '')
            rate = Decimal(getattr(query, rate_field))
        print('discount')
    else:
        print('not discount')
