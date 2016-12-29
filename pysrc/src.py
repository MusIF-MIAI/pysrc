import time

WEEKDAY_WEIGHT = [4, 2, 1]
DAY_WEIGHT = [20, 10, 8, 4, 2, 1]
MONTH_WEIGHT = [10, 8, 4, 2, 1]
YEAR_WEIGHT = [80, 40, 20, 10, 8, 4, 2, 1]
HOUR_WEIGHT = [20, 10, 8, 4, 2, 1]
MINUTE_WEIGHT = [40, 20, 10, 8, 4, 2, 1]


def generate_bit(value, weights):
    bits = ""
    for weight in weights:
        bits += str(value/weight)
        value %= weight
    return bits


def generate_weekday_bit(weekday):
    weekday += 1
    return generate_bit(weekday, WEEKDAY_WEIGHT)


def generate_day_bit(day):
    return generate_bit(day, DAY_WEIGHT)


def generate_month_bit(month):
    return generate_bit(month, MONTH_WEIGHT)


def generate_year_bit(year):
    year = int(str(year)[:2])
    return generate_bit(year, YEAR_WEIGHT)


def generate_hour_bit(hour):
    return generate_bit(hour, HOUR_WEIGHT)


def generate_minute_bit(minute):
    return generate_bit(minute, MINUTE_WEIGHT)


def is_dst(date):
    dst = time.localtime(time.mktime(date.timetuple())).tm_isdst
    return "0" if dst == 0 else "1"


def generate_first_segment(date):
    first_segment = "01"
    first_segment += generate_hour_bit(date.hour)
    first_segment += generate_minute_bit(date.minute)
    first_segment += is_dst(date)
    #P1: parity odd
    first_segment +=  str((sum([int(b) for b in first_segment]) +1) % 2)

    first_segment += generate_month_bit(date.month)
    first_segment += generate_day_bit(date.day)
    first_segment += generate_weekday_bit(date.weekday())
    #P2: parity odd
    first_segment +=  str((sum([int(b) for b in first_segment[17:]]) +1) % 2)
    return first_segment


def generate_second_segment(date):
    second_segment = "10"
    second_segment += generate_year_bit(date.year)
    second_segment += "111"  #FIXME: SE: dst change
    second_segment += "00"  #FIXME: SI: Secondo Intercalare
    #P: parity odd
    second_segment +=  str((sum([int(b) for b in second_segment]) +1) % 2)
    return second_segment


def generate_packet(date):
    first_segment = generate_first_segment(date)
    second_segment = generate_second_segment(date)
    return first_segment, second_segment
