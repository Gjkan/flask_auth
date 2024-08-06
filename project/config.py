import os
from environs import Env
import pathlib


class BaseConfig:
    """Base configuration."""
    BASE_DIR = pathlib.Path(__file__).parent.resolve()


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    BASE_DIR = pathlib.Path(__file__).parent.resolve()
    env = Env()
    env.read_env(path=os.path.join(BASE_DIR.parent.resolve(), 'docker/env/.env.dev'))
    DEBUG = env('DEBUG')
    DB_NAME = env('DB_NAME')
    DB_USER = env('DB_USER')
    DB_PASSWORD = env('DB_PASSWORD')
    DB_HOST = env('DB_HOST')
    DB_PORT = env('DB_PORT')


class ProductionConfig(BaseConfig):
    """Production configuration."""
    BASE_DIR = pathlib.Path(__file__).parent.resolve()
    env = Env()
    env.read_env(path=os.path.join(BASE_DIR.parent.resolve(), 'docker/env/.env.prod'))
    DEBUG = env('DEBUG')
    DB_NAME = env('DB_NAME')
    DB_USER = env('DB_USER')
    DB_PASSWORD = env('DB_PASSWORD')
    DB_HOST = env('DB_HOST')
    DB_PORT = env('DB_PORT')
