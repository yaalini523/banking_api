import os

SQLALCHEMY_DATABASE_URI = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:yaalini@db:5432/bankdb"  # fallback
)
SQLALCHEMY_TRACK_MODIFICATIONS = False #It consumes extra memory.