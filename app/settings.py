import os

class Config:

    DB_PORT = os.environ.get('DB_PORT')
    POSTGRES_USER = os.environ.get('POSTGRES_USER')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    POSTGRES_DB = os.environ.get('POSTGRES_DB')
    DB_HOST = os.environ.get('DB_HOST')

    BACKEND_HOST = os.environ.get('BACKEND_HOST')
    BACKEND_PORT = os.environ.get('BACKEND_PORT')

    FRONTEND_HOST = os.environ.get('FRONTEND_HOST')
    FRONTEND_PORT = os.environ.get('FRONTEND_PORT')