from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from typing import Literal

from email_validator import EmailNotValidError, validate_email
from pycountry import countries
from shared.domain.enums import RiskLevel


@dataclass(frozen=True)  # frozen=True: immutable + hashable
class Money:
    amount: Decimal
    currency: Literal["EUR", "USD", "GBP"]

    def __post_init__(self) -> None:
        # Validation runs after __init__ — raise here to reject bad data
        if self.amount < Decimal("0"):
            raise ValueError(f"Amount cannot be negative: {self.amount}")

    def __add__(self, other: Money) -> Money:
        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency} and {other.currency}")
        else:
            return Money(self.amount + other.amount, self.currency)

    def rounded(self, places: int = 2) -> Money:
        quantize = Decimal("0." + "0" * places)
        return Money(self.amount.quantize(quantize, rounding=ROUND_HALF_UP), self.currency)

    def __str__(self) -> str:
        return f"{self.amount:.2f} {self.currency}"


@dataclass(frozen=True)
class EmailAddress:
    value: str

    def __post_init__(self) -> None:
        try:
            validated = validate_email(
                self.value.strip(),
                check_deliverability=False,  # no DNS lookup - format only
            )

        except EmailNotValidError as exc:
            raise ValueError(f"Invalid email address: {self.value!r}") from exc

        object.__setattr__(self, "value", validated.normalized)

    def domain(self) -> str:
        return self.value.split("@", 1)[1]


@dataclass(frozen=True)
class ISOCountryCode:
    code: str  # two--letter ISON 3166-1 alpha-2

    def __post_init__(self) -> None:
        normalized_code = self.code.strip().upper()
        if countries.get(alpha_2=normalized_code) is None:
            raise ValueError(f"Invalid ISO Country Code: {normalized_code}")
        object.__setattr__(self, "code", normalized_code)

    def __str__(self) -> str:
        return self.code


@dataclass(frozen=True)
class PercentageScore:
    # Risk score between 0.0 and 1.0
    value: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.value <= 1.0:
            raise ValueError(f"Score must be between 0.0 and 1.0, got {self.value}")

    def as_percent(self) -> float:
        return round(self.value * 100, 2)

    def risk_level(self) -> RiskLevel:
        return RiskLevel.from_score(self.value)
