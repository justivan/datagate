from decimal import *

getcontext().prec = 2


def safe_div(numerator, denominator):
    if denominator == 0:
        return 0
    return numerator/denominator * 100
