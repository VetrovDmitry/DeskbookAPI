from sqlalchemy import ForeignKey, String, Table, Column
from sqlalchemy.orm import relationship, Mapped, mapped_column, backref
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.dialects.postgresql import ARRAY
from shapely import wkb

from geoalchemy2 import Geometry, WKBElement

from .database import Base, int_pk, str_pk


class Building(Base):
    __tablename__ = 'buildings'

    id: Mapped[int_pk]
    city: Mapped[str]
    street: Mapped[str]
    number: Mapped[str]
    geo_location: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type='POINT', srid=4326, spatial_index=True)
    )

    organizations: Mapped[list["Organization"]] = relationship('Organization', back_populates='building', lazy='selectin')

    def __repr__(self):
        return f"building: {self.id}"

    @property
    def address(self) -> str:
        return f"{self.city}, {self.street}, {self.number}"

    @property
    def prepared_geo(self) -> tuple:
        point = wkb.loads(bytes(self.geo_location.data))
        return point.x, point.y

    @property
    def info(self) -> dict:
        return {
            'id': self.id,
            'address': self.address,
            'geo_location': self.prepared_geo,
            'time_created': self.time_created.isoformat(),
            'time_updated': self.time_updated.isoformat()
        }


organization_workings = Table(
    'organization_workings',
    Base.metadata,
    Column('working_id', ForeignKey('workings.id'), primary_key=True),
    Column('organization_id', ForeignKey('organizations.id'), primary_key=True)
)


class Working(Base):
    __tablename__ = 'workings'

    id: Mapped[str_pk]
    parent_id: Mapped[str] = mapped_column(ForeignKey('workings.id'), nullable=True)
    details: Mapped[str]

    children: Mapped[list["Working"]] = relationship('Working', backref=backref('parent', remote_side='Working.id'),
                                                     lazy='selectin')
    organizations: Mapped[list["Organization"]] = relationship('Organization', secondary=organization_workings,
                                                               back_populates='workings', lazy='subquery')

    def __repr__(self):
        return f"working: {self.id}"


class Organization(Base):
    __tablename__ = 'organizations'

    id: Mapped[int_pk]
    title: Mapped[str]
    building_id: Mapped[int] = mapped_column(ForeignKey('buildings.id'), nullable=False)
    phones: Mapped[list[str]] = mapped_column(MutableList.as_mutable(ARRAY(String)), default=list)

    building: Mapped["Building"] = relationship('Building', back_populates='organizations', lazy='joined')
    workings: Mapped[list['Working']] = relationship('Working', secondary=organization_workings,
                                                     back_populates='organizations', lazy='subquery')

    def __repr__(self):
        return f"organization: {self.id}"

    @property
    def prepared_workings(self) -> list[dict]:

        workings = list()

        for working in self.workings:

            ws = working.id

            if working.parent_id:
                ws = working.parent_id + "/" + ws
                if working.parent.parent_id:
                    ws = working.parent.parent_id + "/" + ws

            workings.append(ws)

        return workings

    @property
    def info(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'address': self.building.address,
            'workings': self.prepared_workings,
            'phones': self.phones,
            'time_created': self.time_created.isoformat(),
            'time_updated': self.time_updated.isoformat()
        }
