from rest_framework.permissions import BasePermission
from django.conf import settings
from app.errors import AuthenticationError

class HasAPIKey(BasePermission):

    def has_permission(self, request, view):

        api_key = request.headers.get('x-api-key')

        if api_key == settings.SECRET_KEY:
            return True

        raise AuthenticationError("Invalid or missing API Key credentials")