from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status

from . import models, serializers
from . import models

from companies_house.retrieval.companies_house_api import ChAPI

# Create your views here.
class AddressViewSet(viewsets.ModelViewSet):
  queryset = models.Address.objects.all()
  serializer_class = serializers.AddressSerializer

class UserDataViewSet(viewsets.ModelViewSet):
  queryset = models.UserData.objects.all()
  serializer_class = serializers.UserDataSerializer


@api_view(['GET'])
def get_company_data(request):
    query = request.GET.get('query') 
    size = request.GET.get('size', 25) 
    url = 'https://api.company-information.service.gov.uk/advanced-search/companies'
    api_key = ChAPI.getApiKey()
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
    

@api_view(['POST'])
def add_user_data(request):
    if request.method == 'POST':
        print(request.data)
        serializer = serializers.UserDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)