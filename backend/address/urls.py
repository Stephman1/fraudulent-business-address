
from rest_framework import routers
from django.urls import path, include
from .views import AddressViewSet, UserDataViewSet, get_company_data, add_user_data

router = routers.DefaultRouter()
router.register(r"address", AddressViewSet, basename="address")
router.register(r"all-user-data", UserDataViewSet, basename="user-data")


urlpatterns = [
    path('search-address/', get_company_data, name='get_company_data'),
    path('add-user-data/', add_user_data, name='add_user_data'),
    path('', include(router.urls)),
]
