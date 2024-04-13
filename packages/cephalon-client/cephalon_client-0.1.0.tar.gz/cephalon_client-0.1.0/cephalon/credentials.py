from __future__ import annotations
import os
from typing import Optional
from pydantic import BaseModel
from cephalon import path, utils


class Credentials(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    secret: Optional[str] = None

    def save(self) -> None:
        utils.save_toml(self.model_dump(), path.credentials)

    @staticmethod
    def load() -> Credentials:
        data = utils.load_toml(path.credentials)
        return Credentials.model_validate(data)

    @staticmethod
    def exists() -> bool:
        return path.credentials.exists()

    @staticmethod
    def clear() -> None:
        if Credentials.exists():
            os.remove(path.credentials)
