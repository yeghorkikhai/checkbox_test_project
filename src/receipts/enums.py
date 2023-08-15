from enum import StrEnum


class PaymentType(StrEnum):
    CASH: str = "CASH"
    CASHLESS: str = "CASHLESS"
