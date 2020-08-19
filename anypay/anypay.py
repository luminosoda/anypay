# AIOHTTP
from aiohttp import ClientSession

# JSON
try:
    from ujson import loads
except ModuleNotFoundError:
    from json import loads

# SHA-256
from hashlib import sha256

# Convert string to IP addresses
from ipaddress import IPv4Address

# Check for enum
from enum import Enum

# Typing
from typing import Any, List, Mapping, Optional, Union
from yarl import URL

# Constants
from .const import *

# Enums
from .enums import *

# Models
from .models import *


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

    async def _request(self, section: str, params: Mapping[str, Any]) -> dict:
        params_clear = dict()
        for k, v in params.items():
            if v is not None:
                if isinstance(v, float):
                    v = str(v)
                elif isinstance(v, Enum):
                    v = v.value
                elif isinstance(v, URL):
                    v = v.human_repr()

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

    async def rates(self) -> Rates:
        parameters = {"sign": self._sign(f"rates{self.id}{self.key}")}

        response = await self._request("rates", parameters)
        rates = response["result"]

        return Rates(**rates)

    async def commissions(self) -> Commissions:
        parameters = {
            "project_id": self.project_id,
            "sign": self._sign(f"commissions{self.id}{self.project_id}{self.key}"),
        }

        response = await self._request("commissions", parameters)
        commissions = response["result"]

        return Commissions(**commissions)

    async def payments(
        self,
        trans_id: Optional[int] = None,
        pay_id: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Payment]:
        parameters = {
            "project_id": self.project_id,
            "trans_id": trans_id,
            "pay_id": pay_id,
            "offset": offset,
            "sign": self._sign(f"payments{self.id}{self.project_id}{self.key}"),
        }

        response = await self._request("payments", params=parameters)
        payments = response["result"]["payments"].values()

        return [Payment(**payment) for payment in payments]

    async def create_payout(
        self,
        payout_id: int,
        payout_type: Union[PayoutType, str],
        amount: float,
        wallet: str,
        commission_type: Union[
            PayoutCommissionType, str, None
        ] = PayoutCommissionType.PAYMENT,
        currency: Union[PayoutCurrency, str, None] = PayoutCurrency.Ruble,
        status_url: Union[URL, str, None] = None,
    ) -> Payout:
        if isinstance(payout_type, Enum):
            payout_type = payout_type.value

        parameters = {
            "payout_id": payout_id,
            "payout_type": payout_type,
            "amount": amount,
            "wallet": wallet,
            "commission_type": commission_type,
            "currency": currency,
            "status_url": status_url,
            "sign": self._sign(
                f"create-payout{self.id}{payout_id}{payout_type}{amount}{wallet}{self.key}"
            ),
        }

        response = await self._request("create-payout", params=parameters)
        payout = response["result"]

        return Payout(**payout)

    async def payouts(
        self,
        trans_id: Optional[int] = None,
        payout_id: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Payout]:
        parameters = {
            "trans_id": trans_id,
            "payout_id": payout_id,
            "offset": offset,
            "sign": self._sign(f"payouts{self.id}{self.key}"),
        }

        response = await self._request("payouts", params=parameters)
        payouts = response["result"]["payouts"].values()

        return [Payout(**payout) for payout in payouts]

    async def ip_addresses(self) -> List[IPv4Address]:
        parameters = {"sign": self._sign(f"ip-notification{self.id}{self.key}")}

        response = await self._request("ip-notification", params=parameters)
        ip_addresses = response["result"]["ip"]

        return [IPv4Address(ip_address) for ip_address in ip_addresses]
