# Parsing models
from pydantic import BaseModel, EmailStr, Field, validator

# Parsing datetime
from datetime import datetime

# Typing
from typing import Optional

# Constants
from .const import ANYPAY_DATETIME_FORMAT

# Enums
from .enums import *


__all__ = (
    "RatesIn",
    "RatesOut",
    "Rates",
    "Commissions",
    "Payment",
    "Payout",
)


class RatesIn(BaseModel):
    """
    Income currency rates.
    https://anypay.io/doc/api/rates.
    """
    webmoney_dollar: float = Field(..., alias="wmz")  # Webmoney (WMZ).
    dollar: float = Field(..., alias="usd")  # Dollar.
    euro: float = Field(..., alias="eur")  # Euro.
    bitcoin: float = Field(..., alias="btc")  # Bitcoin.
    litecoin: float = Field(..., alias="ltc")  # Litecoin.
    dash: float  # Dash.
    zcash: float = Field(..., alias="zec")  # Zcash.


class RatesOut(BaseModel):
    """
    Outcome currency rates.
    https://anypay.io/doc/api/rates.
    """
    webmoney_dollar: float = Field(..., alias="wmz")  # Webmoney (WMZ).
    hryvnia: float = Field(..., alias="uah")  # Hryvnia.


class Rates(BaseModel):
    """
    Currency rates.
    https://anypay.io/doc/api/rates.
    """
    incomes: RatesIn = Field(..., alias="in")  # For payments.
    outcomes: RatesOut = Field(..., alias="out")  # For payouts.


class Commissions(BaseModel):
    """
    Payment system commission.
    https://anypay.io/doc/sci/method-list.
    """

    card: float  # Visa/Mastercard/Mir.
    apple_pay: float = Field(..., alias="applepay")  # Apple Pay.
    google_pay: float = Field(..., alias="googlepay")  # Google Pay.
    samsung_pay: float = Field(..., alias="samsungpay")  # Samsung Pay.
    qiwi: float  # Qiwi Wallet.
    yandex_money: float = Field(..., alias="ym")  # Yandex.Money.
    webmoney: float = Field(..., alias="wm")  # Webmoney.
    payeer: float  # Payeer.
    bitcoin: float = Field(..., alias="btc")  # Bitcoin.
    litecoin: float = Field(..., alias="ltc")  # Litecoin.
    dash: float  # Dash.
    zcash: float = Field(..., alias="zec")  # Zcash.
    perfect_money: float = Field(..., alias="pm")  # Perfect Money.
    advcash: float  # AdvCash.
    exmo: float  # Exmo.
    mts: float  # MTS.
    beeline: float  # Beeline.
    megafon: float  # MegaFon.
    tele2: float  # Tele2.
    qiwi_terminals: float = Field(..., alias="term")  # Qiwi terminals.
    bank: float  # Bank transfer.
    contact: float  # CONTACT.
    unistream: float  # Unistream.


class Payment(BaseModel):
    """
    Payment model.
    https://anypay.io/doc/api/payments.
    """
    id: int = Field(..., alias="pay_id")  # Unique payment ID in seller's system.
    anypay_id: int = Field(..., alias="transaction_id")  # Unique payment ID in AnyPay system.
    status: PaymentStatus  # Status.
    method: PaymentMethod  # Payment method https://anypay.io/doc/sci/method-list.
    amount: float  # Amount in rubles.
    profit: float  # Amount to enrollment in rubles.
    email: EmailStr  # Customer's email.
    desc: str  # Description.
    date: datetime  # Datetime of payment creation.
    pay_date: Optional[datetime] = None  # Datetime of payment completion.

    # pydantic problems.
    # noinspection PyMethodParameters
    @validator("date", "pay_date", pre=True)
    def _str_to_datetime(cls, v: str) -> datetime:
        return datetime.strptime(v, ANYPAY_DATETIME_FORMAT)


class Payout(BaseModel):
    """
    Payout model.

    https://anypay.io/doc/api/payments.
    """
    id: int = Field(..., alias="payout_id")  # Unique payout ID in seller's system.
    anypay_id: int = Field(..., alias="transaction_id")  # Unique payout ID in AnyPay system.
    method: PayoutMethod  # Payout method.
    status: PayoutStatus  # Status.
    amount: float  # Amount in rubles.
    commission: float  # Commission in rubles.
    commission_type: CommissionType  # Commission type.
    rate: float  # Conversion rate.
    wallet: str  # Recipient wallet/mobile phone/card number.
    date: datetime  # Datetime of payout creation.
    complete_date: Optional[datetime] = None  # Completion date of payout.

    # pydantic problems.
    # noinspection PyMethodParameters
    @validator("date", "complete_date", pre=True)
    def _str_to_datetime(cls, v: str) -> datetime:
        return datetime.strptime(v, ANYPAY_DATETIME_FORMAT)
