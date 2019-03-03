from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_KEY = os.getenv("ACCESS_KEY")
MINIO_BUCKET = os.getenv("MINIO_BUCKET")
MINIO_IP_ADDRESS = os.getenv("MINIO_IP_ADDRESS")
TEST_BUCKET = os.getenv("TEST_BUCKET")
