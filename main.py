import requests
import json
from loguru import logger
import os

# Безопасное хранение API-ключа
API_KEY = os.getenv('WEATHER_API_KEY', 'c3b010247ec84f1b9bf120135252108')
BASE_URL = "https://api.weatherapi.com/v1/current.json"

try:
    # Выполняем GET-запрос
    response = requests.get(
        BASE_URL,
        params={
            'key': API_KEY,
            'q': 'Orenburg',
            'aqi': 'no'
        }
    )

    # Проверяем успешность запроса
    if response.status_code == 200:
        data = response.json()
        
        # Корректная обработка данных
        location_data = data.get('location', {})
        current_data = data.get('current', {})
        
        filtered_data = {
            'location': {
                'name': location_data.get('name', 'N/A'),
                'region': location_data.get('region', 'N/A'),
                'tz_id': location_data.get('tz_id', 'N/A'),
                'country': location_data.get('country', 'N/A')
            },
            'current': {
                'temperature_c': current_data.get('temp_c', 'N/A'),
                'wind_kph': current_data.get('wind_kph', 'N/A')
            }
        }

        # Сохраняем результат в JSON-файл
        with open('weather_data.json', 'w', encoding='utf-8') as json_file:
            json.dump(filtered_data, json_file, ensure_ascii=False, indent=4, sort_keys=True)
            
        logger.info("Данные успешно сохранены в файл weather_data.json")
    else:
        logger.error(f"Ошибка при запросе: {response.status_code}")
        
except requests.exceptions.RequestException as e:
    logger.error(f"Произошла ошибка при выполнении запроса: {e}")
