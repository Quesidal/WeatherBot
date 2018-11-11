import pyowm

from keys import OWM_TOKEN

owm = pyowm.OWM(OWM_TOKEN)  # You MUST provide a valid API key

city = "Zaporizhzhya, UA"

weather = {'speed': 1,
           'deg': 1,
           'clouds': 1,
           'humidity': 1,
           'temp': 1}

MONTH = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def datetime_to_date(in_datetime):
    """преобразовует формат датавремя в дату"""
    return in_datetime[8:10] + ' ' + MONTH[int(in_datetime[5:7])]


def weather_now():
    observation = owm.weather_at_place(city)
    w = observation.get_weather()

    weather['speed'] = w.get_wind()['speed']
    weather['deg'] = w.get_wind()['deg']
    weather['clouds'] = w.get_clouds()
    weather['humidity'] = w.get_humidity()
    weather['temp'] = w.get_temperature('celsius')['temp']

    return weather


def weather_five():
    out_forecast = []

    forecasts = owm.daily_forecast(city, limit=5)
    f = forecasts.get_forecast()
    la_weather_five = f.get_weathers()

    for day in la_weather_five:
        out_forecast.append({'day': datetime_to_date(day.get_reference_time('iso')),
                             'speed': day.get_wind()['speed'],
                             'deg': day.get_wind()['deg'],
                             'clouds': day.get_clouds(),
                             'humidity': day.get_humidity(),
                             'temp': day.get_temperature('celsius')['day']
                             })

    return out_forecast  # возвращает список дней, каждый день словарь с погодой


def ref_forcast(forecast):
    out: str = ""

    out = out + "Температура " + str(forecast['temp']) + "°C" + '\n'
    out = out + "Влажность " + str(forecast['humidity']) + "%" + '\n'
    out = out + "Облака " + str(forecast['clouds']) + "%" + '\n'
    out = out + "Скорость ветра " + str(forecast['speed']) + " м/с " + '\n'
    out = out + "Направление ветра " + str(forecast['deg']) + "°" + '\n'
    return out
