# Parsing models
from pydantic import BaseModel, EmailStr, Field

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
    webmoney_dollar: float = Field(..., alias="wmz")
    dollar: float = Field(..., alias="usd")
    euro: float = Field(..., alias="eur")
    bitcoin: float = Field(..., alias="btc")
    litecoin: float = Field(..., alias="ltc")
    dash: float = Field(..., alias="dash")
    zcash: float = Field(..., alias="zec")


class RatesOut(BaseModel):
    webmoney_dollar: float = Field(..., alias="wmz")
    hryvnia: float = Field(..., alias="uah")


class Rates(BaseModel):
    incomes: RatesIn = Field(..., alias="in")
    outcomes: RatesOut = Field(..., alias="out")


class Commissions(BaseModel):
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


class Payment(BaseModel):
    transaction_id: int
    pay_id: int
    status: PaymentStatus
    method: PaymentMethod
    amount: float
    profit: float
    email: EmailStr
    desc: str
    date: str
    pay_date: str


class Payout(BaseModel):
    transaction_id: int
    payout_id: int
    payout_type: PayoutType
    status: PayoutStatus
    amount: float
    commission: float
    commission_type: PayoutCommissionType
    rate: float
    wallet: str
    balance: float
    date: str
    complete_date: str
