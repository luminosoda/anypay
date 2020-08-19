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
    webmoney_dollar: float = Field(..., alias="wmz")  # Webmoney (WMZ).
    dollar: float = Field(..., alias="usd")  # Dollar.
    euro: float = Field(..., alias="eur")  # Euro.
    bitcoin: float = Field(..., alias="btc")  # Bitcoin.
    litecoin: float = Field(..., alias="ltc")  # Litecoin.
    dash: float = Field(..., alias="dash")  # Dash.
    zcash: float = Field(..., alias="zec")  # Zcash.


class RatesOut(BaseModel):
    webmoney_dollar: float = Field(..., alias="wmz")  # Webmoney (WMZ).
    hryvnia: float = Field(..., alias="uah")  # Hryvnia.


class Rates(BaseModel):
    incomes: RatesIn = Field(..., alias="in")  # For payments.
    outcomes: RatesOut = Field(..., alias="out")  # For payouts.


class Commissions(BaseModel):
    """https://anypay.io/doc/sci/method-list"""

    card: float = Field(..., alias="card")  # Visa/Mastercard/Mir.
    apple_pay: float = Field(..., alias="applepay")  # Apple Pay.
    google_pay: float = Field(..., alias="googlepay")  # Google Pay.
    samsung_pay: float = Field(..., alias="samsungpay")  # Samsung Pay.
    qiwi: float = Field(..., alias="qiwi")  # Qiwi Wallet.
    yandex_money: float = Field(..., alias="ym")  # Yandex.Money.
    webmoney: float = Field(..., alias="wm")  # Webmoney.
    payeer: float = Field(..., alias="payeer")  # Payeer.
    bitcoin: float = Field(..., alias="btc")  # Bitcoin.
    litecoin: float = Field(..., alias="ltc")  # Litecoin.
    dash: float = Field(..., alias="dash")  # Dash.
    zcash: float = Field(..., alias="zec")  # Zcash.
    perfect_money: float = Field(..., alias="pm")  # Perfect Money.
    advcash: float = Field(..., alias="advcash")  # AdvCash.
    exmo: float = Field(..., alias="exmo")  # Exmo.
    mts: float = Field(..., alias="mts")  # MTS.
    beeline: float = Field(..., alias="beeline")  # Beeline.
    megafon: float = Field(..., alias="megafon")  # MegaFon.
    tele2: float = Field(..., alias="tele2")  # Tele2.
    qiwi_terminals: float = Field(..., alias="term")  # Qiwi terminals.
    bank: float = Field(..., alias="bank")  # Bank transfer.
    contact: float = Field(..., alias="contact")  # CONTACT.
    unistream: float = Field(..., alias="unistream")  # Unistream.


class Payment(BaseModel):
    transaction_id: int  # Unique payment ID in AnyPay system.
    pay_id: int  # Unique payment ID in seller's system.
    status: PaymentStatus  # Payment status.
    method: PaymentMethod  # Payment system https://anypay.io/doc/sci/method-list.
    amount: float  # Payment amount in rubles.
    profit: float  # Amount to enrollment in rubles.
    email: EmailStr  # Customer's mailbox.
    desc: str  # Payment description.
    date: str  # Datetime of payment creation.
    pay_date: str  # Datetime of payment completion.


class Payout(BaseModel):
    transaction_id: int  # Unique payout ID in AnyPay system.
    payout_id: int  # Unique payout ID in seller's system.
    payout_type: PayoutType  # Payment system.
    status: PayoutStatus  # Status.
    amount: float  # Payout amount in rubles.
    commission: float  # Payout commission in rubles.
    commission_type: PayoutCommissionType  # Payout commission type.
    rate: float  # Conversion rate.
    wallet: str  # Recipient wallet/mobile phone/card number.
    date: str  # Datetime of payment creation.
    complete_date: str  # Completion date of payment.
