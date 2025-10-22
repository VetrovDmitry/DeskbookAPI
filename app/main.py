from fastapi import FastAPI, Depends, status
from .routers import organizations

from .auth import handle_api_key
from .config import settings
from .schemas import MessageSchema, ErrorSchema


api_version = '/api'

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    dependencies=[
        Depends(handle_api_key)
    ]
)


@app.get(api_version, tags=['Main'], status_code=status.HTTP_200_OK,
         responses={403: {'model': ErrorSchema}})
def root() -> MessageSchema:
    return {'message': f"{settings.app_name}, v{settings.app_version}"}


app.include_router(organizations.router, prefix=api_version)
