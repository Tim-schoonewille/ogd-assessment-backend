from functools import lru_cache
import os
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

    REDIS_HOST: str = get_env('REDIS_HOST')
    REDIS_PASSWORD: str = get_env('REDIS_PASSWORD')


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
