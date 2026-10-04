import pandas as pd

storage_options = {
    "key": "admin",
    "secret": "password123",
    "client_kwargs": {
        "endpoint_url": "http://localhost:9000"
    }
}

# Читаем данные
df = pd.read_parquet(
    "s3://air-quality-weather/processed/open_meteo/open_meteo_daily_2023.parquet",
    storage_options=storage_options
)

# Анализ: средние показатели по городам
result = (
    df.groupby("city_name")
      .agg(
          avg_temperature=("temperature", "mean"),
          avg_humidity=("humidity", "mean"),
          avg_wind_speed=("wind_speed", "mean"),
          total_precipitation=("precipitation", "sum"),
          observations=("date", "count")
      )
      .reset_index()
      .round(2)
)

print("Результаты анализа:")
print(result)

# Сохраняем аналитическую витрину обратно в MinIO
result.to_parquet(
    "s3://air-quality-weather/analytics/city_weather_stats_2023.parquet",
    storage_options=storage_options,
    index=False
)

print("\nАналитическая витрина сохранена в analytics/city_weather_stats_2023.parquet")