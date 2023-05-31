from enum import Enum, IntEnum


class FinancialsType(str, Enum):
    ANNUAL = "A"  # Annual
    QUARTERLY = "Q"  # Quarterly


class RequestStatus(IntEnum):
    PRICE = 1  # PRICE
    DM = 2  # DM
    YIELD = 3  # YIELD
    YIELD_XIRR = 4  # YIELD_XIRR
