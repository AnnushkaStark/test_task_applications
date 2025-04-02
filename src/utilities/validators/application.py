from constants.application import (
    MAX_APPLICATION_NAME_LENGTH,
    MAX_APPLICATION_TEXT_LENGTH,
    MIN_APPLICATION_NAME_LENGTH,
    MIN_APPLICATION_TEXT_LENGTH,
)
from schemas.application import ApplicationUpdate


async def valid_name(schema: ApplicationUpdate) -> None:
    if schema.name:
        if (
            MIN_APPLICATION_NAME_LENGTH
            > schema.name
            > MAX_APPLICATION_NAME_LENGTH
        ):
            raise Exception(
                "The application name must be between two and one hundred characters long."  # noqa: E501
            )


async def valid_description(schema: ApplicationUpdate) -> None:
    if schema.description:
        if (
            MIN_APPLICATION_TEXT_LENGTH
            > schema.description
            > MAX_APPLICATION_TEXT_LENGTH
        ):
            raise Exception(
                "The application description must be between two and a thousand characters long."  # noqa: E501
            )


async def valid_schema(schema: ApplicationUpdate) -> None:
    try:
        await valid_name(schema=schema)
        await valid_description(schema=schema)
    except Exception as e:
        raise Exception(str(e))
