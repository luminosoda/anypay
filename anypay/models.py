# Parsing models
from pydantic import BaseModel, EmailStr, Field

# Enums
from .enums import *


__all__ = (
    "AnyPayRatesIn",
    "AnyPayRatesOut",
    "AnyPayRates",
    "AnyPayCommissions",
    "AnyPayPayment",
)


class AnyPayRatesIn(BaseModel):
    webmoney_dollar: float = Field(..., alias="wmz")
    dollar: float = Field(..., alias="usd")
    euro: float = Field(..., alias="eur")
    bitcoin: float = Field(..., alias="btc")
    litecoin: float = Field(..., alias="ltc")
    dash: float = Field(..., alias="dash")
    zcash: float = Field(..., alias="zec")


class AnyPayRatesOut(BaseModel):
    webmoney_dollar: float = Field(..., alias="wmz")
    hryvnia: float = Field(..., alias="uah")


class AnyPayRates(BaseModel):
    incomes: AnyPayRatesIn = Field(..., alias="in")
    outcomes: AnyPayRatesOut = Field(..., alias="out")


class AnyPayCommissions(BaseModel):
    card: float = Field(..., alias="card")
    apple_pay: float = Field(..., alias="applepay")
    google_pay: float = Field(..., alias="googlepay")
    samsung_pay: float = Field(..., alias="samsungpay")
    qiwi: float = Field(..., alias="qiwi")
    yandex_money: float = Field(..., alias="ym")
    webmoney: float = Field(..., alias="wm")
    payeer: float = Field(..., alias="payeer")
    bitcoin: float = Field(..., alias="btc")
    litecoin: float = Field(..., alias="ltc")
    dash: float = Field(..., alias="dash")
    zcash: float = Field(..., alias="zec")
    perfect_money: float = Field(..., alias="pm")
    advcash: float = Field(..., alias="advcash")
    exmo: float = Field(..., alias="exmo")
    mts: float = Field(..., alias="mts")
    beeline: float = Field(..., alias="beeline")
    megafon: float = Field(..., alias="megafon")
    tele2: float = Field(..., alias="tele2")
    qiwi_terminals: float = Field(..., alias="term")
    bank: float = Field(..., alias="bank")
    contact: float = Field(..., alias="contact")
    unistream: float = Field(..., alias="unistream")


class AnyPayPayment(BaseModel):
    transaction_id: int
    pay_id: int
    status: AnyPayPaymentStatus
    method: AnyPayPaymentMethod
    amount: float
    profit: float
    email: EmailStr
    desc: str
    date: str
    pay_date: str
