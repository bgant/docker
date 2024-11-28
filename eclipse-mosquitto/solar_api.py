# Source: https://sunrisesunset.io/api/

### Setup
# python3 -m venv .venv
# source .venv/bin/activate
# pip list
# pip install --upgrade pip
# pip install requests

### Usage
# from datetime import datetime
# import solar_api
# dusk = solar_api.phase('dusk')
# datetime.now() > dusk
#   False


import requests
from datetime import datetime

def request():
    # Sidney, IL
    lat =  40.0224345 # Required field
    lng = -88.0787767 # Required field
    timezone = 'CST'  # (Optional) defaults to lat and lng timezone / can also use America/Chicago
    date = 'today'    # (Optional) defaults to today / tomorrow or YYYY-MM-DD are other options
    
    url = f'https://api.sunrisesunset.io/json?lat={lat}&lng={lng}'
    data = requests.get(url).json()
    return data
    
def phase(query='dusk'):
    data = request()
    meridiem = data['results'][query].split(' ')[1]
    data_tuple_str = data['results'][query].split(' ')[0].split(':')
    data_tuple_int = [int(data_tuple_str[0])+12 if meridiem == 'PM' and int(data_tuple_str[0]) < 12 else int(data_tuple_str[0]), 
                      int(data_tuple_str[1]), 
                      int(data_tuple_str[2])]
    data_datetime = datetime.now().replace(hour = data_tuple_int[0], minute = data_tuple_int[1], second = 0)
    if datetime.now().day == data_datetime.day:
        return data_datetime 
    else:
        print('ERROR: Something is wrong with the API data... Exiting')
        exit()

if __name__ == '__main__':
    data = request()
    solar_phases = list(data['results'].keys())
    solar_phases.remove('day_length')
    solar_phases.remove('timezone')
    print('API Solar Phases: ' + ', '.join(solar_phases))
    phase_input = input('Which Phase? ')
    if phase_input.lower() in solar_phases:
        print(phase(phase_input.lower()).strftime('%a %Y-%m-%d %H:%M:%S'))
    else:
        print(f'ERROR: {phase_input.lower()} is not a valid Solar Phase')


'''
>>> data
{'results': 
  {'sunrise':     '6:57:30 AM', 
   'sunset':      '5:17:54 PM', 
   'first_light': '5:25:21 AM', 
   'last_light':  '6:50:03 PM', 
   'dawn':        '6:29:11 AM', 
   'dusk':        '5:46:14 PM', 
   'solar_noon': '12:07:42 PM', 
   'golden_hour': '4:39:06 PM', 
   'day_length': '10:20:24', 
   'timezone': 'CST'}, 
'status': 'OK'}
'''

