import datetime
from enum import Enum
from pydantic import BaseModel, model_validator, Field, PositiveInt
from pydantic_extra_types.coordinate import Latitude, Longitude


class MessageSchema(BaseModel):
    message: str


class ErrorSchema(BaseModel):
    detail: str


class OrganizationResponse(BaseModel):
    id: int
    title: str
    address: str
    workings: list[str] = []
    phones: list[str] = []
    time_created: datetime.datetime
    time_updated: datetime.datetime


class BuildingResponse(BaseModel):
    id: int
    address: str
    geo_location: tuple[Latitude, Longitude]
    time_created: datetime.datetime
    time_updated: datetime.datetime


class OrganizationsAndBuildingsResponse(BaseModel):
    organizations: list[OrganizationResponse] = []
    buildings: list[BuildingResponse]


class BuildingFilter(BaseModel):
    city: str = Field(default=None, description='Населенный пункт')
    street: str = Field(default=None, description='Улица, переулок, бульвар и тд.')
    number: str = Field(default=None, description='Дом, офис и тд.')


class WorkingFilter(BaseModel):
    working: str = Field(default=None, description='Вид деятельности')


class GeoSearchType(Enum):
    RECT = 'rectangle'
    RADIUS = 'radius'


class GeoFilter(BaseModel):
    type: GeoSearchType = Field(description='Тип поиска')
    km_within: PositiveInt = Field(default=None, description='Радиус окружности поиска')
    radius_latitude: Latitude = Field(default=None, description='Широта центра окружности')
    radius_longitude: Longitude = Field(default=None, description='Долгота центра окружности')
    a_latitude: Latitude = Field(default=None, description='Широта А-точки прямоугольника')
    a_longitude: Longitude = Field(default=None, description='Долгота А-точки прямоугольника')
    b_latitude: Latitude = Field(default=None, description='Широта B-точки прямоугольника')
    b_longitude: Longitude = Field(default=None, description='Долгота B-точки прямоугольника')

    @model_validator(mode='before')
    @classmethod
    def check_geo_search_logic(cls, data):
        if isinstance(data, dict):

            required_fields = list()

            if data['type'] == 'radius':
                required_fields = ['km_within', 'radius_latitude', 'radius_longitude']

            if data['type'] == 'rectangle':
                required_fields = ['a_latitude', 'a_longitude', 'b_latitude', 'b_longitude']

            for f in required_fields:
                if f not in data:
                    raise ValueError(f"{required_fields} должны быть заполнены")

        return data


class TitleFilter(BaseModel):
    title: str = Field(default=None, description='Название организации')
