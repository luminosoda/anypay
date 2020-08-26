# Enums
from enum import Enum


__all__ = (
    "PaymentMethod",
    "PaymentStatus",
    "PayoutType",
    "PayoutStatus",
    "PayoutCommissionType",
    "PayoutCurrency",
    "PaymentCurrency",
    "PaymentPageLanguage",
)


class PaymentStatus(Enum):
    PAID = "paid"  # Successful payment.
    WAITING = "waiting"  # Waiting for payment.
    REFUND = "refund"  # Refund to the customer.
    CANCELED = "canceled"  # The payment is cancelled.
    EXPIRED = "expired"  # Bill has expired.
    ERROR = "error"  # payment error.


class PaymentMethod(Enum):
    """https://anypay.io/doc/sci/method-list"""

    CARD = "card"  # Visa/Mastercard/Mir.
    APPLE_PAY = "applepay"  # Apple Pay.
    GOOGLE_PAY = "googlepay"  # Google Pay.
    SAMSUNG_PAY = "samsungpay"  # Samsung Pay.
    QIWI = "qiwi"  # Qiwi Wallet.
    YANDEX_MONEY = "ym"  # Yandex.Money.
    WEBMONEY = "wm"  # Webmoney.
    PAYEER = "payeer"  # Payeer.
    BITCOIN = "btc"  # Bitcoin.
    LITECOIN = "ltc"  # Litecoin.
    DASH = "dash"  # Dash.
    ZCASH = "zec"  # Zcash.
    PERFECT_MONEY = "pm"  # Perfect Money.
    ADVCASH = "advcash"  # AdvCash.
    EXMO = "exmo"  # Exmo.
    MTS = "mts"  # MTS.
    BEELINE = "beeline"  # Beeline.
    MEGAFON = "megafon"  # MegaFon.
    TELE2 = "tele2"  # Tele2.
    QIWI_TERMINALS = "term"  # Qiwi terminals.
    BANK = "bank"  # Bank transfer.
    CONTACT = "contact"  # CONTACT.
    UNISTREAM = "unistream"  # Unistream.


class PayoutType(Enum):
    QIWI = "qiwi"  # Qiwi Wallet.
    YANDEX_MONEY = "ym"  # Yandex.Money.
    WEBMONEY_DOLLAR = "wm"  # Webmoney (WMZ).
    MOBILE = "mc"  # Mobile pay.
    CARD = "card"  # Visa/Mastercard/Mir.


class PayoutStatus(Enum):
    PAID = "paid"  # Successful payout.
    IN_PROCESS = (
        "in_process"  # Payout has been sent to the payment system (temporary status).
    )
    CANCELED = "canceled"  # Payout is cancelled by the payment system, funds are returned to the balance.
    BLOCKED = "blocked"  # Payout is blocked by the monitoring system.


class PayoutCommissionType(Enum):
    PAYMENT = "payment"  # From the payment amount.
    BALANCE = "balance"  # From balance.


class PayoutCurrency(Enum):
    RUBLE = "rub"  # Ruble.
    HRYVNIA = "uah"  # Hryvnia.


class PaymentCurrency(Enum):
    RUBLE = "rub"  # Ruble.
    DOLLAR = "usd"  # Hryvnia.
    EURO = "eur"  # Euro.


class PaymentPageLanguage(Enum):
    RUSSIAN = "ru"  # Russian.
    ENGLISH = "en"  # English.
