import requests
import pyowm

owm = pyowm.OWM('4d9d39bf5022f48a29205b0c5b7a5205')
url = 'https://random-city-api.vercel.app/api/random-city'

def get_weather(city):
    try:
        location = owm.weather_manager().weather_at_place(city)
        weather = location.weather
        temperature = weather.temperature('celsius')['temp']
        status = weather.detailed_status
        detailed_status = weather.detailed_status
        wind_speed = weather.wind()['speed']
        humidity = weather.humidity
        return f"O clima em {city} é de {temperature:.1f}°C com {status}. A velocidade do vento é de {wind_speed} m/s e a umidade é de {humidity}%."
    except pyowm.commons.exceptions.NotFoundError:
        return f"Não foi possível encontrar dados de clima para {city}."