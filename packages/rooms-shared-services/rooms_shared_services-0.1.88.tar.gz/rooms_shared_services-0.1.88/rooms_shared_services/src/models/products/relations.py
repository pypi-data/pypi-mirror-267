from pydantic import BaseModel





class GeoRelatedValues(BaseModel):
    IL: str | float | int | None = None