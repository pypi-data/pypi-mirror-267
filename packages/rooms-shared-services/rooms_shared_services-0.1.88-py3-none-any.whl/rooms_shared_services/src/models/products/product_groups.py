from src.models.products.relations import GeoRelatedValues
from src.storage.models import BaseDynamodbModel


class ProductGroup(BaseDynamodbModel):
    name: str
    brands: list[str]
    base_margins: GeoRelatedValues
    