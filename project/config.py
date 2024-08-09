import os
from environs import Env
import pathlib


class BaseConfig:
    """Base configuration."""
    BASE_DIR = pathlib.Path(__file__).parent.resolve()
    BCRYPT_LOG_ROUNDS = 4
    USER_TABLE_NAME = 'user'
    BLACKLIST_TOKEN_TABLE_NAME = 'blacklist_token'


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    BASE_DIR = BaseConfig.BASE_DIR
    BCRYPT_LOG_ROUNDS = BaseConfig.BCRYPT_LOG_ROUNDS
    USER_TABLE_NAME = BaseConfig.USER_TABLE_NAME
    BLACKLIST_TOKEN_TABLE_NAME = BaseConfig.BLACKLIST_TOKEN_TABLE_NAME

    env = Env()
    env.read_env(path=os.path.join(BASE_DIR.parent.resolve(), 'docker/env/.env.dev'))
    SECRET_KEY = env('SECRET_KEY')
    DEBUG = env('DEBUG')
    DB_NAME = env('DB_NAME')
    DB_USER = env('DB_USER')
    DB_PASSWORD = env('DB_PASSWORD')
    DB_HOST = env('DB_HOST')
    DB_PORT = env('DB_PORT')


class TestingConfig(BaseConfig):
    """Testing configuration."""
    BASE_DIR = BaseConfig.BASE_DIR
    BCRYPT_LOG_ROUNDS = BaseConfig.BCRYPT_LOG_ROUNDS
    USER_TABLE_NAME = BaseConfig.USER_TABLE_NAME + '_test'
    BLACKLIST_TOKEN_TABLE_NAME = BaseConfig.BLACKLIST_TOKEN_TABLE_NAME + '_test'

    env = Env()
    env.read_env(path=os.path.join(BASE_DIR.parent.resolve(), 'docker/env/.env.dev'))
    SECRET_KEY = env('SECRET_KEY')
    DEBUG = env('DEBUG')
    DB_NAME = env('DB_NAME') + '_test'
    DB_USER = env('DB_USER')
    DB_PASSWORD = env('DB_PASSWORD')
    DB_HOST = env('DB_HOST')
    DB_PORT = env('DB_PORT')


class ProductionConfig(BaseConfig):
    """Production configuration."""
    BASE_DIR = BaseConfig.BASE_DIR
    BCRYPT_LOG_ROUNDS = 13
    USER_TABLE_NAME = BaseConfig.USER_TABLE_NAME
    BLACKLIST_TOKEN_TABLE_NAME = BaseConfig.BLACKLIST_TOKEN_TABLE_NAME

    env = Env()
    env.read_env(path=os.path.join(BASE_DIR.parent.resolve(), 'docker/env/.env.prod'))
    SECRET_KEY = env('SECRET_KEY')
    DEBUG = env('DEBUG')
    DB_NAME = env('DB_NAME')
    DB_USER = env('DB_USER')
    DB_PASSWORD = env('DB_PASSWORD')
    DB_HOST = env('DB_HOST')
    DB_PORT = env('DB_PORT')
