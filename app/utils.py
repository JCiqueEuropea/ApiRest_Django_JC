import logging
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError as DRFValidationError

from app.errors import (
    EntityNotFoundError,
    BusinessRuleError,
    AuthenticationError,
    ExternalAPIError
)

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    if isinstance(exc, DjangoValidationError):
        if hasattr(exc, 'message_dict'):
            exc = DRFValidationError(detail=exc.message_dict)
        elif hasattr(exc, 'message'):
            exc = DRFValidationError(detail=exc.message)
        elif hasattr(exc, 'messages'):
            exc = DRFValidationError(detail=exc.messages)

    response = exception_handler(exc, context)

    if isinstance(exc, EntityNotFoundError):
        return Response(
            {"error": "Not Found", "message": exc.message},
            status=status.HTTP_404_NOT_FOUND
        )

    if isinstance(exc, BusinessRuleError):
        return Response(
            {"error": "Business Rule Violation", "message": exc.message},
            status=status.HTTP_409_CONFLICT
        )

    if isinstance(exc, AuthenticationError):
        return Response(
            {"error": "Unauthorized", "message": exc.message},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if isinstance(exc, ExternalAPIError):
        logger.error(f"External API Error: {exc.message}")
        return Response(
            {"error": "External Service Error", "message": exc.message},
            status=status.HTTP_502_BAD_GATEWAY
        )

    if response is not None and response.status_code == 400:
        return Response(
            {"error": "Validation Error", "details": response.data},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    return response
