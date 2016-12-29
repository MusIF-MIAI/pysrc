import requests

#URI_LEAP_LIST = 'https://www.ietf.org/timezones/data/leap-seconds.list'
URI_LEAP_LIST = 'https://hpiers.obspm.fr/iers/bul/bulc/ntp/leap-seconds.list'

def parse_leap_list(leap_file):
    leap = {}
    for line in leap_file.split('\n'):
        l = filter(None, line.split('#')[0].split(' '))
        if l and len(l) == 2:
            leap[int(l[0])] = int(l[1])
    return leap

def get_leap_list(uri=URI_LEAP_LIST):
    r_leap = requests.get(uri)
    if r_leap.status_code == 200:
        return parse_leap_list(r_leap.text)

def get_month_leap_second(date):
    get_leap_list()

def convert_timestamp(ntp_time)
    return ntp_time - 2208988800
