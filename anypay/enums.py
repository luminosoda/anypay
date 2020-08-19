# Enums
from enum import Enum


__all__ = (
    "PaymentMethod",
    "PaymentStatus",
    "PayoutType",
    "PayoutStatus",
    "PayoutCommissionType",
    "PayoutCurrency",
)


class PaymentStatus(Enum):
    PAID = "paid"
    WAITING = "waiting"
    REFUND = "refund"
    CANCELED = "canceled"
    EXPIRED = "expired"
    ERROR = "error"


class PaymentMethod(Enum):
    CARD = "card"
    APPLE_PAY = "applepay"
    GOOGLE_PAY = "googlepay"
    SAMSUNG_PAY = "samsungpay"
    QIWI = "qiwi"
    YANDEX_MONEY = "ym"
    WEBMONEY = "wm"
    PAYEER = "payeer"
    BITCOIN = "btc"
    LITECOIN = "ltc"
    DASH = "dash"
    ZCASH = "zec"
    PERFECT_MONEY = "pm"
    ADVCASH = "advcash"
    EXMO = "exmo"
    MTS = "mts"
    BEELINE = "beeline"
    MEGAFON = "megafon"
    TELE2 = "tele2"
    QIWI_TERMINALS = "term"
    BANK = "bank"
    CONTACT = "contact"
    UNISTREAM = "unistream"


class PayoutType(Enum):
    QIWI = "qiwi"
    YANDEX_MONEY = "ym"
    WEBMONEY_DOLLAR = "wm"
    MOBILE = "mc"
    CARD = "card"


class PayoutStatus(Enum):
    PAID = "paid"
    IN_PROCESS = "in_process"
    CANCELED = "canceled"
    BLOCKED = "blocked"


class PayoutCommissionType(Enum):
    PAYMENT = "payment"
    BALANCE = "balance"


class PayoutCurrency(Enum):
    Ruble = "rub"
    Hryvnia = "uah"
