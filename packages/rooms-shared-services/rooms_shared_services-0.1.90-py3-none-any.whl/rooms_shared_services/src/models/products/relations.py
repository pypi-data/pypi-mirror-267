from src.storage.models import BaseDynamodbModel
from typing import Literal


CurrencyCode = Literal["EUR", "ILS", "USD", "RUB"]


class GeoRelatedValues(BaseDynamodbModel):
    IL: str | float | int | None = None
