from src.models.products.relations import GeoRelatedValues
from src.storage.models import BaseDynamodbModel, UNSET


class ProductGroup(BaseDynamodbModel):
    name: str | UNSET = "UNSET"
    brands: list[str] | UNSET = "UNSET"
    base_margins: GeoRelatedValues | UNSET = "UNSET"
