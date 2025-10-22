from fastapi import Security, HTTPException, status, Request
from fastapi.security import APIKeyHeader
from .config import settings


api_key = APIKeyHeader(name='x-api-key')


async def handle_api_key(key: str = Security(api_key)):

    if key != settings.app_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid API-key'
        )

    yield key
