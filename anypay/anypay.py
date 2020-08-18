# AIOHTTP
from aiohttp import ClientSession

# JSON
try:
    from ujson import loads
except ModuleNotFoundError:
    from json import loads

# SHA-256
from hashlib import sha256

# Typing
from typing import Mapping, Optional, Union

# Constants
from .const import *


__all__ = ("AnyPayAPI",)


class AnyPayAPI:
    def __init__(
        self,
        id_: str,
        key: str,
        project_id: Optional[str] = None,
        secret: Optional[str] = None,
    ):
        self.id = id_
        self.key = key
        self.project_id = project_id
        self.secret = secret

        self._session = ClientSession(headers={"Accept": "application/json"})

    async def _request(self, section: str, params: Mapping[str, str]) -> dict:
        params_clear = dict()
        for k, v in params.items():
            if v is not None:
                if v is float:
                    v = str(v)

                params_clear[k] = v

        async with await self._session.get(
            f"{ANYPAY_API_URL}/{section}/{self.id}", params=params
        ) as response:
            # The signature of the loads function from json doesn't match the signature from UJSON
            # noinspection PyTypeChecker
            return await response.json(loads=loads)

    @staticmethod
    def _sign(string: str):
        return sha256(bytes(string.encode())).hexdigest()

    async def balance(self) -> Union[float, int]:
        parameters = {"sign": self._sign(f"balance{self.id}{self.key}")}

        response = await self._request("balance", parameters)
        balance = response["result"]["balance"]

        return balance
