# HTTP
from aiohttp import ClientSession

# JSON
try:
    from ujson import loads
except ModuleNotFoundError:
    from json import loads

# Hash
from hashlib import sha256, md5

# Convert string to IP addresses
from ipaddress import IPv4Address

# Convert URL to string
from yarl import URL

# Check for enum
from enum import Enum

# Typing
from typing import Any, List, Mapping, Optional, Union

# Constants
from .const import *

# Enums
from .enums import *

# Models
from .models import *


__all__ = ("AnyPay",)


class AnyPay:
    """Class to interact with AnyPay API: https://anypay.io/doc/api."""

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

    def _sign(self, method: str, sign: Optional[str] = None) -> str:
        """
        Create sign for request with SHA-256.

        Parameters
        ----------
        method : str
            Method of the API.
        sign : str
            Sign without method, API_ID and API_KEY to be encoded.
            Each full sign contains the same method as the request,
            has ID and key, so we don't have to write them every time.
            If the argument is None, there is nothing between ID and key.

        Returns
        -------
        str
            Sign.
        """
        if sign is None:
            sign = ""

        return sha256(bytes(f"{method}{self.id}{sign}{self.key}".encode())).hexdigest()

    async def _request(
        self,
        method: str,
        params: Optional[Mapping[str, Any]] = None,
        sign: Optional[str] = None,
    ) -> Union[bool, dict, int, list, str, None]:
        """
        Make request to AnyPay API.

        Parameters
        ----------
        method : str
            API method, in the URL it is next after https://anypay.io/api/.
        params : Optional[Mapping[str, Any]]
            Parameters for query string.
        sign : Optional[str]
            Sign without method, API_ID and API_KEY.

        Returns
        -------
        dict
            Response.
        """
        params_valid = dict()
        for k, v in params.items():
            if v is not None:
                if isinstance(v, float):
                    v = str(v)
                elif isinstance(v, Enum):
                    v = v.value
                elif isinstance(v, URL):
                    v = v.human_repr()

                params_valid[k] = v

        params_valid["sign"] = self._sign(sign)

        async with await self._session.get(
            f"{ANYPAY_API_URL}/{method}/{self.id}", params=params
        ) as response:
            # The signature of the loads function from json doesn't match the signature from UJSON.
            # noinspection PyTypeChecker
            response = await response.json(loads=loads)

            return response["result"]

    async def balance(self) -> float:
        """
        Get profile balance.
        https://anypay.io/doc/api.

        Returns
        -------
        float
            Balance in rubles.
        """
        response = await self._request("balance")

        return response

    async def rates(self) -> Rates:
        """
        Get currency rates.
        https://anypay.io/doc/api/rates.

        Returns
        -------
        Commissions
            pydantic model of currency rates.
        """
        response = await self._request("rates")

        return Rates(**response)

    async def commissions(self) -> Commissions:
        """
        Get commissions for project.
        https://anypay.io/doc/api/commissions.

        Returns
        -------
        Commissions
            pydantic model of commissions.
        """
        parameters = {"project_id": self.project_id}

        response = await self._request("commissions", parameters, self.project_id)

        return Commissions(**response)

    async def payments(
        self,
        trans_id: Optional[int] = None,
        pay_id: Optional[int] = None,
        offset: Optional[int] = 0,
    ) -> List[Payment]:
        """
        Get payments.
        https://anypay.io/doc/api/payments.

        Parameters
        ----------
        trans_id : int, optional
            Unique payment ID in AnyPay system.
        pay_id : int, optional
            Unique payment ID in seller's system.
        offset : int, optional
            Offset required to select a specific subset of payments (default - 0).

        Returns
        -------
        List[Payment]
            List of payments as a pydantic models.
        """
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
        currency: Union[PayoutCurrency, str, None] = PayoutCurrency.RUBLE,
        commission_type: Union[
            PayoutCommissionType, str, None
        ] = PayoutCommissionType.PAYMENT,
        status_url: Union[URL, str, None] = None,
    ) -> Payout:
        """
        Create payout.
        https://anypay.io/doc/api/create-payout.

        Parameters
        ----------
        payout_id : int, optional
            Unique payout ID in seller's system.
        payout_type : Union[PayoutType, str], optional
            Payment system.
        amount : float
            Amount of payout in rubles.
        wallet : str
            Recipient wallet/mobile phone/card number.
        currency : Union[PayoutCurrency, str], optional
            The recipient's currency (bank cards).
        commission_type : Union[PayoutCommissionType, str], optional
            From what take the commission.
        status_url : Union[URL, str], optional
            URL to which GET-request will be sent when the payment
            moves to final status.

        Returns
        -------
        Payout
            Created payout.
        """
        # Need to get the value right here because it will be used in sign.
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
        """
        Get payouts.
        https://anypay.io/doc/api/payouts.

        Parameters
        ----------
        trans_id : int, optional
            Unique payout ID in AnyPay system.
        payout_id : int, optional
            Unique payout ID in seller's system.
        offset : int, optional
            Offset required to select a specific subset of payouts (default - 0).

        Returns
        -------
        List[Payment]
            List of payouts as a pydantic models.
        """
        parameters = {"trans_id": trans_id, "payout_id": payout_id, "offset": offset}

        response = await self._request("payouts", parameters)
        payouts = response["payouts"].values()

        return [Payout(**payout) for payout in payouts]

    async def ip_addresses(self) -> List[IPv4Address]:
        """
        Get IP addresses of current trusted servers.
        https://anypay.io/doc/api/ip.

        Returns
        -------
        List[IPv4Address]
            List of IPv4 addresses as ipaddress.IPv4Address.
        """
        response = await self._request("ip-notification")
        ip_addresses = response["ip"]

        return [IPv4Address(ip_address) for ip_address in ip_addresses]

    def create_link(
        self,
        pay_id: int,
        amount: float,
        currency: Union[PaymentCurrency, str, None] = PaymentCurrency.RUBLE,
        desc: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        method: Union[PaymentMethod, str, None] = None,
        lang: Union[PaymentPageLanguage, str, None] = PaymentPageLanguage.RUSSIAN,
        **params,
    ) -> URL:
        """
        Initialize payment and create link.
        https://anypay.io/doc/sci.

        Parameters
        ----------
        pay_id : int
            Unique payment ID in seller's system.
        amount : float
            Amount in rubles.
        currency : Union[PaymentCurrency, str], optional
            Currency: RUB, USD, EUR (according to ISO 4217 standard).
        desc : int, optional
            Description (up to 150 symbols).
        email : str, optional
            Customer's email address.
        phone : int, optional
            Customer's phone number.
        method : Union[PaymentMethod, str], optional
            Payment system, https://anypay.io/doc/sci/method-list.
        lang : Union[PaymentPageLanguage, str], optional
            Interface language of payment page.
        **params : Union[str, int, Enum], optional
            Additional seller's parameters, will be transfered to notification.

        Returns
        -------
        URL
            Payment link as yarl.URL.
        """
        if isinstance(currency, Enum):
            currency = currency.value

        params.update(
            {
                "merchant_id": self.project_id,
                "pay_id": pay_id,
                "amount": str(amount),
                "currency": currency,
                "desc": desc,
                "email": email,
                "phone": phone,
                "method": method,
                "lang": lang,
            }
        )

        params_valid = dict()
        for k, v in params.items():
            if v is not None:
                if isinstance(v, Enum):
                    v = v.value

                params_valid[k] = v

        params_valid["sign"] = md5(
            f"{currency}:{amount}:{self.secret}:{self.project_id}:{pay_id}".encode()
        ).hexdigest()

        return URL(ANYPAY_MERCHANT_URL) % params_valid

    async def close(self):
        await self._session.close()
