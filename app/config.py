import os
from functools import lru_cache
from typing import Annotated, TypeAlias

from fastapi import Depends
from pydantic import BaseModel


def get_env(variable: str) -> str:
    """Custom env variable getter with a default string."""
    return os.environ.get(variable, default='Could not read from environment.')


class ConfigBase(BaseModel):
    """
    Base class for configurations.
    These values are equal on every different environment.
    """

    ENV: str = get_env('ENVIRONMENT')
    APP_TITLE: str = get_env('APP_TITLE')
    API_VERSION: str = get_env('API_VERSION')

    CACHE_EXPIRATION: int = 60 * 60 * 24

    REDIS_HOST: str = get_env('REDIS_HOST')
    REDIS_PASSWORD: str = get_env('REDIS_PASSWORD')

    OMDB_API_KEY: str = get_env('OMDB_API_KEY')
    OMDB_API_URL: str = 'http://www.omdbapi.com/'

    # YOUTUBE_API_KEY: str = get_env('YOUTUBE_API_KEY')  # main
    # YOUTUBE_API_KEY: str = 'AIzaSyCp-B06iZx_zGazh1ftZRe4wKcFr6CExm4'  # backup 1
    YOUTUBE_API_KEY: str = 'AIzaSyDN-1E5w3lyRMINPeMmcJ5_IVy58dEH2uk'  # backup 2
    YOUTUBE_API_URL: str = 'https://www.googleapis.com/youtube/v3/search'

    VIMEO_API_KEY: str = '52ebb294f46e635ebec7be58d2723b5c'


class DevConfig(ConfigBase):
    """Config for the development environment."""

    pass


class TestConfig(ConfigBase):
    """Config for the testing environment."""

    pass


class ProdConfig(ConfigBase):
    """Config for the production environment."""

    pass


@lru_cache
def get_config() -> ConfigBase:
    """Factory for creating configuration object based on the environemnt."""
    configurations = {'dev': DevConfig, 'test': TestConfig, 'prod': ProdConfig}

    env = os.environ.get('ENVIRONMENT', default='dev')

    config = configurations[env]()

    return config


GetConfig: TypeAlias = Annotated[ConfigBase, Depends(get_config)]
