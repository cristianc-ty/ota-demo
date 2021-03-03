from typing import Optional, List

from pydantic import BaseModel, ValidationError, root_validator, confloat


class SearchRequest(BaseModel):
    categories: Optional[List[str]]
    trip_type: Optional[str]
    hotel_types: Optional[List[str]]
    min_rating: Optional[int]
    city: Optional[str]
    country: Optional[str]
    lat: Optional[float]
    long: Optional[float]
    radius: Optional[confloat(ge=0, le=10000)]
    language: Optional[str]
    scale: Optional[int] = 100
    page: Optional[int] = 1
    page_size: Optional[int] = 50

    @root_validator
    def check_require_city_or_map_box(cls, values):
        if not cls.is_valid_city_country_request(values) and not cls.is_valid_map_box_request(values):
            raise ValueError('(city, country) or (lat, long, radius) should be included')

        if cls.is_valid_city_country_request(values) and cls.is_valid_map_box_request(values):
            raise ValueError('Only (city, country) or (lat, long, radius) should be included')

        if values.get("scale") not in [5, 100]:
            raise ValueError('Only (5, 100) are supported values for scale')

        return values

    @classmethod
    def is_valid_map_box_request(cls, values):
        return values.get("lat") \
            and values.get("long") \
            and values.get("radius")

    @classmethod
    def is_valid_city_country_request(cls, values):
        return values.get("city") and values.get("country")