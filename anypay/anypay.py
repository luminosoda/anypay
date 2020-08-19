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

    @staticmethod
    def _sign(string: str):
        return sha256(bytes(string.encode())).hexdigest()

    async def _request(
        self,
        section: str,
        params: Optional[Mapping[str, Any]] = None,
        sign: Optional[str] = None,
    ) -> Union[bool, dict, int, list, str, None]:
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

        params_clear[sign] = self._sign(f"{section}{self.id}{sign}{self.key}")

        async with await self._session.get(
            f"{ANYPAY_API_URL}/{section}/{self.id}", params=params
        ) as response:
            # The signature of the loads function from json doesn't match the signature from UJSON
            # noinspection PyTypeChecker
            response = await response.json(loads=loads)

            return response["result"]

    async def balance(self) -> Union[float, int]:
        response = await self._request("balance")

        return response

    async def rates(self) -> Rates:
        response = await self._request("rates")

        return Rates(**response)

    async def commissions(self) -> Commissions:
        parameters = {"project_id": self.project_id}

        response = await self._request("commissions", parameters, self.project_id)

        return Commissions(**response)

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
        }

        response = await self._request("payments", parameters, self.project_id)
        payments = response["payments"].values()

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
        }
        sign = f"{payout_id}{payout_type}{amount}{wallet}"

        response = await self._request("create-payout", parameters, sign)

        return Payout(**response)

    async def payouts(
        self,
        trans_id: Optional[int] = None,
        payout_id: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Payout]:
        parameters = {"trans_id": trans_id, "payout_id": payout_id, "offset": offset}

        response = await self._request("payouts", parameters)
        payouts = response["payouts"].values()

        return [Payout(**payout) for payout in payouts]

    async def ip_addresses(self) -> List[IPv4Address]:
        response = await self._request("ip-notification")
        ip_addresses = response["ip"]

        return [IPv4Address(ip_address) for ip_address in ip_addresses]
