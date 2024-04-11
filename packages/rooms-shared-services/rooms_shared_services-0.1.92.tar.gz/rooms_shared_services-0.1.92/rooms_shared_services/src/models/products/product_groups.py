from src.models.products.relations import GeoRelatedValues
from src.storage.models import BaseDynamodbModel, UNSET
from uuid import UUID


class ProductGroup(BaseDynamodbModel):
    id: UUID | UNSET = "UNSET"    
    name: str | UNSET = "UNSET"
    brands: list[str] | UNSET = "UNSET"
    base_margins: GeoRelatedValues | UNSET = "UNSET"