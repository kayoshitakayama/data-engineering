import boto3
from botocore.exceptions import ClientError

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="admin",
    aws_secret_access_key="password123"
)

BUCKET = "air-quality-weather"

# Создаём bucket
try:
    s3.create_bucket(Bucket=BUCKET)
    print(f"Bucket '{BUCKET}' успешно создан")
except ClientError as e:
    if e.response["Error"]["Code"] == "BucketAlreadyOwnedByYou":
        print(f"Bucket '{BUCKET}' уже существует")
    else:
        print("Ошибка при создании bucket:", e)

# Загружаем файлы
print("\nЗагружаю файлы...")

s3.upload_file(
    "data/reference/cities.csv",
    BUCKET,
    "raw/reference/cities.csv"
)
print("→ raw/reference/cities.csv")

s3.upload_file(
    "data/processed/open_meteo_daily_2023.csv",
    BUCKET,
    "raw/open_meteo/open_meteo_daily_2023.csv"
)
print("→ raw/open_meteo/open_meteo_daily_2023.csv")

s3.upload_file(
    "data/processed/open_meteo_daily_2023.parquet",
    BUCKET,
    "processed/open_meteo/open_meteo_daily_2023.parquet"
)
print("→ processed/open_meteo/open_meteo_daily_2023.parquet")

print("\nВсе файлы успешно загружены!")