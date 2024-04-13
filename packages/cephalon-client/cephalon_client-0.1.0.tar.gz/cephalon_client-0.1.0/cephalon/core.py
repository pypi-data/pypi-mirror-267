from __future__ import annotations
from pydantic import BaseModel
from typing import Any, Optional
from loguru import logger
from pathlib import Path
from cephalon import utils
from cephalon import path
from cephalon.api import module
from cephalon.credentials import Credentials
from cephalon.meta import __version__


class Config(BaseModel):
    cache: bool = True
    endpoint: str = "https://api.cephalon.io"
    headers: dict[str, Any] = dict({"user-agent": f"cephalon-client@{__version__}"})

    def save(self, path: Path = path.config) -> None:
        utils.save_toml(self.model_dump(), path)

    @staticmethod
    def load(path: Path = path.config) -> Config:
        config_data = utils.load_toml(path)
        return Config.model_validate(config_data)


class Client:
    def __init__(
        self,
        config: Config,
        state: dict | Any,
        creds: Optional[Credentials] = None,
        logs: bool = False,
    ) -> None:
        """
        Client instance.

        Args:
            headers (dict): Custom headers for API endpoint.
            state (Any): State to store session data in.
            logs (bool): Whether to show loguru logs.
        """
        self.state = state
        self.state.update(config.model_dump())
        self.logging(show=logs)
        self.__init_subclasses()

    def __repr__(self) -> str:
        raise NotImplementedError()

    def logging(self, show: bool) -> None:
        """Enable or disable showing the loguru logs."""
        if show:
            logger.enable(__package__)
        else:
            logger.disable(__package__)

    def __init_subclasses(self) -> None:
        self.auth = module.auth.Auth(self.state)


def client(
    config: Optional[Config] = None,
    state: Optional[Any] = None,
    creds: Optional[Credentials] = None,
    logs: bool = False,
) -> Client:
    if config is None:
        if path.config.exists():
            config = Config.load()
        else:
            config = Config()
    if state is None:
        state = dict()
    return Client(
        config=config,
        state=state,
        logs=logs,
    )
