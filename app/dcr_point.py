from pydantic import BaseModel, validator, ValidationError
from haversine import haversine
from typing import Generator


class Direction(BaseModel):
    address: str
    city: str
    country: str

    def __str__(self) -> str:
        return f"{self.address}, {self.city}, {self.country}"


class Point(BaseModel):
    lat: float
    lng: float

    @validator('lat')
    def validate_lat(cls, lat: float) -> float:
        if lat < -90 or lat > 90:
            raise ValueError('Latitude must be in the range (-90, 90)')
        return lat

    @validator('lng')
    def validate_lng(cls, lng: float) -> float:
        if lng < -180 or lng > 180:
            raise ValueError('Longitude must be in the range (180, -180)')
        return lng

    def to_tuple(self) -> tuple:
        return self.lat, self.lng


class DCRPoint(BaseModel):
    point: Point

    def nearby_points(self) -> Generator:
        """
        generates a centroid from the integer values of point,
        returns a circle of available points if said points are valid, and the point itself
        :return: generator, nearby integer points
        """
        lat_int = round(self.point.lat, 0)
        lng_int = round(self.point.lng, 0)
        for lat in (lat_int - 1, lat_int, lat_int + 1):
            for lng in (lng_int - 1, lng_int, lng_int + 1):
                try:
                    p = Point(lat=lat, lng=lng)
                except ValidationError:
                    continue
                yield p
        yield self.point

    def calculate_distance(self, point: Point, metric='km') -> float:
        """
        Since the earth is not flat (sorry flat earthers) we cannot use the euclidean distance
        hence the haversine calculation
        https://en.wikipedia.org/wiki/Haversine_formula
        :param point: the point to compare against for measuring the distance
        :param metric: kilometers, hardcoded for now
        :return: the distance, we round it to make it more pretty on the view, though,
                 that should be handled there, but is done here due to time constraints for the project.
        """
        return round(haversine(self.point.to_tuple(), point.to_tuple(), unit=metric), 2)
