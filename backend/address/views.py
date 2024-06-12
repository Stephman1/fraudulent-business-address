from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets, status

from companies_house.retrieval.companies_house_api import ChAPI
from . import models, serializers
from . import models
from . import serializers


# Create your views here.
class AddressViewSet(viewsets.ModelViewSet):
  queryset = models.Address.objects.all()
  serializer_class = serializers.AddressSerializer


@api_view(['GET'])
def get_company_data(request):
    query = request.GET.get('query') 
    size = request.GET.get('size', 25) 
    url = 'https://api.company-information.service.gov.uk/advanced-search/companies'
    api_key = ChAPI.getApiKey()
    print(api_key)
    params = {
        "location": query,
        "size": size
    }

    if not query:
        return Response({'error': 'Address is not provided'}, status=status.HTTP_400_BAD_REQUEST)
       
    try:
        data = ChAPI.getChData(url=url, api_key=api_key, params=params)
        return Response(data, content_type='application/json')
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    