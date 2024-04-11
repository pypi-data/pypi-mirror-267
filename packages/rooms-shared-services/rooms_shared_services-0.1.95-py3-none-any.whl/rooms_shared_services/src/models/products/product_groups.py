from uuid import UUID

from rooms_shared_services.src.models.relations import GeoRelatedValues
from rooms_shared_services.src.storage.models import UNSET, BaseDynamodbModel


class ProductGroup(BaseDynamodbModel):
    id: UUID | UNSET = "UNSET"
    name: str | UNSET = "UNSET"
    brands: list[str] | UNSET = "UNSET"
    base_margins: GeoRelatedValues | UNSET = "UNSET"
