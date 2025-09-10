from django.contrib import admin
from rest_framework_api_key.admin import APIKeyModelAdmin
from rest_framework_api_key.models import APIKey

from .models import UserAPIKey

# Remove the stock APIKey from the admin
admin.site.unregister(APIKey)


# Register your custom one
@admin.register(UserAPIKey)
class UserAPIKeyModelAdmin(APIKeyModelAdmin):
    pass
