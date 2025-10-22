from typing import Annotated
from fastapi import APIRouter, Query, HTTPException, status
from app.schemas import (ErrorSchema, OrganizationResponse, BuildingFilter, WorkingFilter,
                         GeoFilter, TitleFilter, OrganizationsAndBuildingsResponse)
from app.services import OrganizationDAO


tags = ['Organizations']


router = APIRouter(
    prefix='/organizations'
)


@router.get('/building', tags=tags, status_code=status.HTTP_200_OK,
            summary='Cписок всех организаций находящихся в конкретном здании',
            responses={403: {'model': ErrorSchema}, 404: {'model': ErrorSchema}})
async def get_all_organizations_by_building(
        filter_query: Annotated[BuildingFilter, Query()]) -> list[OrganizationResponse]:

    organizations = await OrganizationDAO.find_organizations_by_address(filter_query)

    if not organizations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Организации по заданному адресу не найдены')

    return organizations


@router.get('/working', tags=tags, status_code=status.HTTP_200_OK,
            summary='Список всех организаций, которые относятся к указанному виду деятельности',
            responses={403: {'model': ErrorSchema}, 404: {'model': ErrorSchema}})
async def get_all_organizations_by_working(
        filter_query: Annotated[WorkingFilter, Query()]) -> list[OrganizationResponse]:

    organizations = await OrganizationDAO.find_organizations_by_working(filter_query)

    if not organizations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Организации по заданному виду деятельности не найдены')

    return organizations


@router.get('/workings', tags=tags, status_code=status.HTTP_200_OK,
            summary="Полный поиск организаций по виду деятельности вглубь каталога",
            responses={403: {'model': ErrorSchema}, 404: {'model': ErrorSchema}})
async def get_all_organizations_by_workings(
        filter_query: Annotated[WorkingFilter, Query()]):

    organizations = await OrganizationDAO.find_organizations_by_workings(filter_query)

    if not organizations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Организации по виду деятельности не найдены')

    return organizations


@router.get('-buildings', tags=tags, status_code=status.HTTP_200_OK,
            summary="""Cписок организаций, которые находятся в заданном 
                радиусе/прямоугольной области относительно указанной 
                точки на карте. Cписок зданий""",
            responses={403: {'model': ErrorSchema}, 404: {'model': ErrorSchema}})
async def get_all_organizations_and_building_by_coord(
        filter_query: Annotated[GeoFilter, Query()]) -> OrganizationsAndBuildingsResponse:

    organizations_and_buildings = await OrganizationDAO.find_orgs_and_builds(filter_query)

    if not organizations_and_buildings['buildings']:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Здания по заданным координатам не найдены')

    return organizations_and_buildings


@router.get('/title', tags=tags, status_code=status.HTTP_200_OK,
            summary='Поиск организации по названию',
            responses={403: {'model': ErrorSchema}, 404: {'model': ErrorSchema}})
async def get_all_organizations_by_title(
        filter_query: Annotated[TitleFilter, Query()]) -> list[OrganizationResponse]:
    organizations = await OrganizationDAO.find_organizations_by_name(filter_query)

    if not organizations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Организации с таким названием не найдены')

    return organizations


@router.get('/{organization_id}', tags=tags, status_code=status.HTTP_200_OK,
            summary='Вывод информации об организации по её идентификатору',
            responses={403: {'model': ErrorSchema}, 404: {'model': ErrorSchema}})
async def get_organization_by_id(organization_id: int):

    organization = await OrganizationDAO.get_organization(organization_id)

    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Организация по заданному Id не найдена')

    return organization
