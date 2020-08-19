# AIOHTTP
from aiohttp import ClientSession

# JSON
try:
    from ujson import loads
except ModuleNotFoundError:
    from json import loads

# SHA-256
from hashlib import sha256

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

    async def rates(self) -> AnyPayRates:
        parameters = {"sign": self._sign(f"rates{self.id}{self.key}")}

        response = await self._request("rates", parameters)
        rates = response["result"]

        return AnyPayRates(**rates)

    async def commissions(self) -> AnyPayCommissions:
        parameters = {
            "project_id": self.project_id,
            "sign": self._sign(f"commissions{self.id}{self.project_id}{self.key}"),
        }

        response = await self._request("commissions", parameters)
        commissions = response["result"]

        return AnyPayCommissions(**commissions)

    async def payments(
        self,
        trans_id: Optional[int] = None,
        pay_id: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[AnyPayPayment]:
        parameters = {
            "project_id": self.project_id,
            "trans_id": trans_id,
            "pay_id": pay_id,
            "offset": offset,
            "sign": self._sign(f"payments{self.id}{self.project_id}{self.key}"),
        }

        response = await self._request("payments", params=parameters)
        payments = response["result"]["payments"].values()

        return [AnyPayPayment(**payment) for payment in payments]

    async def create_payout(
        self,
        payout_id: int,
        payout_type: Union[AnyPayPayoutType, str],
        amount: float,
        wallet: str,
        commission_type: Union[AnyPayPayoutCommissionType, str, None] = AnyPayPayoutCommissionType.PAYMENT,
        currency: Union[AnyPayPayoutCurrency, str, None] = AnyPayPayoutCurrency.Ruble,
        status_url: Union[URL, str, None] = None,
    ) -> AnyPayPayout:
        if isinstance(payout_type, Enum):
            payout_type = payout_type.value

        sign = self._sign(
            f"create-payout{self.id}{payout_id}{payout_type}{amount}{wallet}{self.key}"
        )

        parameters = {
            "payout_id": payout_id,
            "payout_type": payout_type,
            "amount": amount,
            "wallet": wallet,
            "commission_type": commission_type,
            "currency": currency,
            "sign": sign,
            "status_url": status_url,
        }

        response = await self._request("create-payout", params=parameters)
        payout = response["result"]

        return AnyPayPayout(**payout)

    async def payouts(
        self,
        trans_id: Optional[int] = None,
        payout_id: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[AnyPayPayout]:
        parameters = {
            "trans_id": trans_id,
            "payout_id": payout_id,
            "offset": offset,
            "sign": self._sign(f"payouts{self.id}{self.key}"),
        }

        response = await self._request("payouts", params=parameters)
        payouts = response["result"]["payouts"].values()

        return [AnyPayPayout(**payout) for payout in payouts]
