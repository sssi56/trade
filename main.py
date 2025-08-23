import requests
import json
from loguru import logger
from config.database import API_KEY, BASE_URL
import os


try:
    SPISOK_PATH = os.path.join(os.path.dirname(__file__), 'config', 'spisok.json')

    with open(SPISOK_PATH, 'r', encoding='utf-8') as f:
        cities_data = json.load(f)
        cities = cities_data.get('spisok', [])

    for city in cities:
        try:
            response = requests.get(
                BASE_URL,
                params={
                    'key': API_KEY,
                    'q': city,
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
                        'wind_kph': current_data.get('wind_kph', 'N/A'),
                        'last_updated': current_data.get('last_updated', 'N/A')
                    }
                }

                output_path = f'log/{city}.json'
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                # Сохраняем результат в JSON-файл
                with open(output_path, 'w', encoding='utf-8') as json_file:
                    json.dump(filtered_data, json_file, ensure_ascii=False, indent=4, sort_keys=True)

                logger.info("Данные успешно сохранены в файл data.json")
            else:
                logger.error(f"Ошибка при запросе: {response.status_code}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Произошла ошибка при выполнении запроса: {e}")

except Exception as e:
    logger.error(f"Произошла ошибка: {e}")
