# Enums
from enum import Enum


__all__ = (
    "AnyPayPaymentMethod",
    "AnyPayPaymentStatus",
    "AnyPayPayoutType",
    "AnyPayPayoutStatus",
    "AnyPayPayoutCommissionType",
    "AnyPayPayoutCurrency",
)


class AnyPayPaymentStatus(Enum):
    PAID = "paid"
    WAITING = "waiting"
    REFUND = "refund"
    CANCELED = "canceled"
    EXPIRED = "expired"
    ERROR = "error"


class AnyPayPaymentMethod(Enum):
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


class AnyPayPayoutType(Enum):
    QIWI = "qiwi"
    YANDEX_MONEY = "ym"
    WEBMONEY_DOLLAR = "wm"
    MOBILE = "mc"
    CARD = "card"


class AnyPayPayoutStatus(Enum):
    PAID = "paid"
    IN_PROCESS = "in_process"
    CANCELED = "canceled"
    BLOCKED = "blocked"


class AnyPayPayoutCommissionType(Enum):
    PAYMENT = "payment"
    BALANCE = "balance"


class AnyPayPayoutCurrency(Enum):
    Ruble = "rub"
    Hryvnia = "uah"
