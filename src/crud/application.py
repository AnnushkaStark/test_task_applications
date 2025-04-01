from models import Application
from schemas.application import ApplicationUpdate, AppllicationCreate

from .async_crud import BaseAsyncCRUD


class ApplicationCRUD(
    BaseAsyncCRUD[Application, AppllicationCreate, ApplicationUpdate]
):
    ...


application_crud = ApplicationCRUD(Application)
