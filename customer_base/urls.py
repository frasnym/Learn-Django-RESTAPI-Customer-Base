from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from core.views import CustomerViewSet, ProfessionViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'professions', ProfessionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
