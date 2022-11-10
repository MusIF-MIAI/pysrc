# -*- coding: cp1252 -*-
import time
from datetime import datetime
import calendar

WEEKDAY_WEIGHT = [4, 2, 1]
DAY_WEIGHT = [20, 10, 8, 4, 2, 1]
MONTH_WEIGHT = [10, 8, 4, 2, 1]
YEAR_WEIGHT = [80, 40, 20, 10, 8, 4, 2, 1]
HOUR_WEIGHT = [20, 10, 8, 4, 2, 1]
MINUTE_WEIGHT = [40, 20, 10, 8, 4, 2, 1]

global leap_second_warning
leap_second_warning = "00"

def generate_bit(value, weights):
    bits = ""
    for weight in weights:
        if int(value/weight) == 1:
            bits = bits + "1"
            value=value-weight
        else:
            bits=bits+"0"
    return bits


def generate_weekday_bit(weekday):
    weekday += 1
    return generate_bit(weekday, WEEKDAY_WEIGHT)


def generate_day_bit(day):
    return generate_bit(day, DAY_WEIGHT)


def generate_month_bit(month):
    return generate_bit(month, MONTH_WEIGHT)


def generate_year_bit(year):
    year = int(str(year)[2:])
    return generate_bit(year, YEAR_WEIGHT)


def generate_hour_bit(hour):
    return generate_bit(hour, HOUR_WEIGHT)


def generate_minute_bit(minute):
    return generate_bit(minute, MINUTE_WEIGHT)


def is_dst(date):
    dst = time.localtime(time.mktime(date.timetuple())).tm_isdst
    return "0" if dst == 0 else "1"


def generate_first_segment(date):
    first_segment = "01" #Identification bits of the first segment. DO NOT MODIFY!
    first_segment += generate_hour_bit(date.hour) #Hour bits
    first_segment += generate_minute_bit(date.minute) #Minutes bits
    first_segment += is_dst(date) #Time bits (0=Standard time, 1=Summer time)
    first_segment += str((sum([int(b) for b in first_segment]) +1) % 2) #P1: First parity bit of the first segment
    first_segment += generate_month_bit(date.month) #Month bits
    first_segment += generate_day_bit(date.day) #Day bits
    first_segment += generate_weekday_bit(date.weekday()) #Bits for the day of the week
    first_segment += str((sum([int(b) for b in first_segment[17:]]) +1) % 2) #P2: Second parity bit of the first segment
    return first_segment #Return of the first segment


def generate_second_segment(date):
    second_segment = "10" #Identification bits of the second segment. DO NOT MODIFY!
    second_segment += generate_year_bit(date.year) #Year bits

    year=date.year
    day_number_in_month=date.day
    hours=date.hour
    month=date.month


    change_bits = "111"

    if(month==3 or month==10):

        #Calculation of the day of the time change

        temp = calendar.monthcalendar(year, 10)
        october_change_day = max(temp[-1][calendar.SUNDAY], temp[-2][calendar.SUNDAY])
        temp = calendar.monthcalendar(year, 3)
        march_change_day = max(temp[-1][calendar.SUNDAY], temp[-2][calendar.SUNDAY])

        if((day_number_in_month==march_change_day - 6 and month==3) or (day_number_in_month==october_change_day - 6 and month==10)):
            change_bits = "110"
        elif((day_number_in_month==march_change_day - 5 and month==3) or (day_number_in_month==october_change_day - 5 and month==10)):
            change_bits = "101"
        elif((day_number_in_month==march_change_day - 4 and month==3) or (day_number_in_month==october_change_day - 4 and month==10)):
            change_bits = "100"
        elif((day_number_in_month==march_change_day - 3 and month==3) or (day_number_in_month==october_change_day - 3 and month==10)):
            change_bits = "011"
        elif((day_number_in_month==march_change_day - 2 and month==3) or (day_number_in_month==october_change_day - 2 and month==10)):
            change_bits = "010"
        elif((day_number_in_month==march_change_day - 1 and month==3) or (day_number_in_month==october_change_day - 1 and month==10)):
            change_bits = "001"
        elif((day_number_in_month == march_change_day and month==3 and is_dst(date)==0) or (day_number_in_month == october_change_day and month==10 and is_dst(date)==1)):
            change_bits = "000"

    second_segment += change_bits                                               #SE: Time change bits (See note at the bottom)

    global leap_second_warning

    if(leap_second_warning != "00"):                                            #The leap second can be inserted only on the 1st of January or July. The bits are resetted if the month is not correct
        if((month != 1) and (month != 6) and (month != 7) and (month != 12)):
            leap_second_warning = "00"
        elif(month == 1 and day_number_in_month >= 1 and hours > 0):
            leap_second_warning = "00"
        elif(month == 7 and day_number_in_month >= 1 and hours > 1):
            leap_second_warning = "00"



    second_segment += leap_second_warning                                       #SI: Leap second warning bits
    second_segment +=  str((sum([int(b) for b in second_segment]) +1) % 2)      #PA: Parity bit of the second segment
    return second_segment                                                       #Return of the second segment


def generate_packet(date):
    first_segment = generate_first_segment(date)
    second_segment = generate_second_segment(date)

    return first_segment, second_segment, leap_second_warning


# Meaning of the bits for time change

# 111 = No time change expected in the next 7 days
# 110 = The time change is expected within 6 days
# 101 = The time change is expected within 5 days
# 100 = The time change is expected within 4 days
# 011 = The time change is expected within 3 days
# 010 = The time change is expected within 2 days
# 001 = The time change is expected within 1 day
# 000 = At ​​02:00 o'clock summer time begins or at 03:00 o'clock standard time begins



# Meaning of the bits of the leap second warning. THESE BITS HAVE TO BE SET MANUALLY!!! CAUTION!!!

# 00 = No leap second within the month
# 10 = Delay of 1 second at the end of the month
# 11 = Advance of 1 second at the end of the month

#To change the value of these bits within the signals to be generated, change the bits from "00" to "10" or "11". These year bits have to be manually reset to 00 after the addition / subtraction of the leap second.

#For more information on the subject visit this site: https://www.ietf.org/timezones/data/leap-seconds.list
