import requests
import pandas as pd
from pathlib import Path

# Читаем справочник городов
cities = pd.read_csv("data/reference/cities.csv")

START_DATE = "2023-01-01"
END_DATE   = "2023-12-31"

all_data = []

for _, city in cities.iterrows():
    print(f"Загружаю данные для {city['city_name']}...")

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "start_date": START_DATE,
        "end_date": END_DATE,
        "daily": [
            "temperature_2m_mean",
            "relative_humidity_2m_mean",
            "precipitation_sum",
            "wind_speed_10m_mean",
            "surface_pressure_mean",
            "cloud_cover_mean"
        ],
        "timezone": city["timezone"]
    }

    response = requests.get(url, params=params, timeout=60)
    response.raise_for_status()
    data = response.json()

    df = pd.DataFrame({
        "date": data["daily"]["time"],
        "temperature": data["daily"]["temperature_2m_mean"],
        "humidity": data["daily"]["relative_humidity_2m_mean"],
        "precipitation": data["daily"]["precipitation_sum"],
        "wind_speed": data["daily"]["wind_speed_10m_mean"],
        "pressure": data["daily"]["surface_pressure_mean"],
        "cloud_cover": data["daily"]["cloud_cover_mean"],
    })

    df["city_id"] = city["city_id"]
    df["city_name"] = city["city_name"]
    df["country_code"] = city["country_code"]

    all_data.append(df)

# Объединяем все города
weather = pd.concat(all_data, ignore_index=True)

# Создаём папку, если её нет
Path("data/processed").mkdir(parents=True, exist_ok=True)

# Сохраняем
weather.to_csv("data/processed/open_meteo_daily_2023.csv", index=False)
weather.to_parquet("data/processed/open_meteo_daily_2023.parquet", index=False)

print("\nГотово!")
print(f"Всего строк: {len(weather)}")
print(weather.head())