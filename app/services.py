from sqlalchemy.future import select
from geoalchemy2.functions import ST_DWithin, ST_GeogFromText, ST_Within, ST_GeomFromText
from pydantic import BaseModel
from .database import connection
from .models import Organization, Building, Working


class OrganizationDAO:

    @classmethod
    @connection
    async def find_organizations_by_address(
            cls, address_filter: BaseModel, session) -> list[dict]:

        query = select(Building)

        if address_filter.city:
            query = query.filter(Building.city.ilike(f"%{address_filter.city}%"))
        if address_filter.street:
            query = query.filter(Building.street.ilike(f"%{address_filter.street}%"))
        if address_filter.number:
            query = query.filter(Building.number.ilike(f"%{address_filter.number}%"))

        buildings = await session.execute(query)

        organizations = list()

        for building in buildings.unique().scalars():
            for organization in building.organizations:
                organizations.append(await organization.awaitable_attrs.info)

        return organizations

    @classmethod
    @connection
    async def find_organizations_by_working(
            cls, working_filter: BaseModel, session) -> list[dict]:

        query = select(Working)

        if working_filter.working:
            query = query.filter(Working.id.ilike(f"%{working_filter.working}%"))

        workings = await session.execute(query)

        organizations = list()

        for working in workings.unique().scalars():
            for organization in working.organizations:
                org_info = await organization.awaitable_attrs.info
                if org_info not in organizations:
                    organizations.append(org_info)

        return organizations

    @classmethod
    @connection
    async def find_organizations_by_workings(
            cls, working_filter: BaseModel, session) -> list[dict]:

        query = select(Working)

        if working_filter.working:
            query = query.filter(Working.id.ilike(f"%{working_filter.working}%"))

        workings = await session.execute(query)

        organizations = list()

        for working in workings.unique().scalars():

            for organization in working.organizations:
                organization_info = await organization.awaitable_attrs.info
                if organization_info not in organizations:
                    organizations.append(organization_info)

            children = await working.awaitable_attrs.children
            for child in children:
                for organization in child.organizations:
                    organization_info = await organization.awaitable_attrs.info
                    if organization_info not in organizations:
                        organizations.append(organization_info)

                post_children = await child.awaitable_attrs.children
                for post_child in post_children:
                    for organization in post_child.organizations:
                        organization_info = await organization.awaitable_attrs.info
                        if organization_info not in organizations:
                            organizations.append(organization_info)

        return organizations

    @classmethod
    @connection
    async def find_orgs_and_builds_by_radius(
            cls, geo_filter: BaseModel, session) -> dict[list[dict], list[dict]]:

        result = {'organizations': [], 'buildings': []}

        target_radius = ST_GeogFromText(
            f"POINT({geo_filter.radius_latitude} {geo_filter.radius_longitude})", srid=4326
        )

        query = select(Building).where(
            ST_DWithin(Building.geo_location, target_radius, 1000 * geo_filter.km_within)
        )

        buildings = await session.execute(query)

        for building in buildings.scalars().all():
            result['buildings'].append(building.info)
            for org in building.organizations:
                organization = org.info
                result['organizations'].append(organization)

        return result

    @classmethod
    @connection
    async def find_orgs_and_builds_by_rect(
            cls, geo_filter: BaseModel, session) -> dict[list[dict], list[dict]]:

        result = {'organizations': [], 'buildings': []}

        target_rect = "POLYGON (({0} {1}, {2} {1}, {2} {3}, {0} {3}, {0} {1}))".format(
            geo_filter.a_latitude, geo_filter.a_longitude, geo_filter.b_longitude, geo_filter.b_longitude
        )
        target_rect = ST_GeomFromText(target_rect, 4326)

        query = select(Building).filter(
            ST_Within(Building.geo_location, target_rect)
        )

        buildings = await session.execute(query)

        for building in buildings.scalars().all():
            result['buildings'].append(building.info)
            for org in building.organizations:
                organization = org.info
                result['organizations'].append(organization)

        return result

    @classmethod
    async def find_orgs_and_builds(
            cls, geo_filter: BaseModel) -> dict[list[dict], list[dict]]:

        orgs_and_builds = {}

        if geo_filter.type.value == 'radius':
            orgs_and_builds = await cls.find_orgs_and_builds_by_radius(geo_filter)

        if geo_filter.type.value == 'rectangle':
            orgs_and_builds = await cls.find_orgs_and_builds_by_rect(geo_filter)

        return orgs_and_builds

    @classmethod
    @connection
    async def get_organization(cls, organization_id: int, session):

        query = select(Organization).filter_by(id=organization_id)

        organization = await session.execute(query)
        organization = organization.scalar()

        return await organization.awaitable_attrs.info if organization else None

    @classmethod
    @connection
    async def find_organizations_by_name(cls, title_filter: BaseModel, session):

        query = select(Organization)

        if title_filter.title:
            query = query.filter(Organization.title.ilike(f"%{title_filter.title}%"))

        organizations = await session.execute(query)

        return [await organization.awaitable_attrs.info for organization in organizations.unique().scalars()]
