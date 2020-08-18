# Parsing models
from pydantic import BaseModel, Field


__all__ = (
    "AnyPayRatesIn",
    "AnyPayRatesOut",
    "AnyPayRates"
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
