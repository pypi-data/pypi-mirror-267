from src.storage.models import BaseDynamodbModel


class GeoRelatedValues(BaseDynamodbModel):
    IL: str | float | int | None = None
