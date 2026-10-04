import pandas as pd

storage_options = {
    "key": "admin",
    "secret": "password123",
    "client_kwargs": {
        "endpoint_url": "http://localhost:9000"
    }
}

df = pd.read_parquet(
    "s3://air-quality-weather/processed/open_meteo/open_meteo_daily_2023.parquet",
    storage_options=storage_options
)

print("Данные успешно прочитаны из MinIO")
print(f"Размер: {df.shape}")
print("\nПервые 5 строк:")
print(df.head())
print("\nТипы данных:")
print(df.dtypes)