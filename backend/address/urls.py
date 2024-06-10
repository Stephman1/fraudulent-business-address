
from rest_framework import routers
from django.urls import path, include
from .views import AddressViewSet, get_company_data

router = routers.DefaultRouter()
router.register("address", AddressViewSet, basename="address")


urlpatterns = [
    path('company-data/', get_company_data, name='get_company_data'),
    path('', include(router.urls)),
]

urlpatterns += router.urls