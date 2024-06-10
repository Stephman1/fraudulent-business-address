from django.http import JsonResponse
from rest_framework.response import Response
from django.views.decorators.http import require_GET
from . import models, serializers
from companies_house.retrieval.companies_house_api import ChAPI
from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers

# Create your views here.
class AddressViewSet(viewsets.ModelViewSet):
  queryset = models.Address.objects.all()
  serializer_class = serializers.AddressSerializer

@require_GET
def get_company_data(request):
    query = request.GET.get('query') 
    size = request.GET.get('size', 25) 
    print(f"Received query: {query}")  # Debugging
    print(f"Received size: {size}") 
    url = 'https://api.company-information.service.gov.uk/advanced-search/companies'
    api_key = ChAPI.getApiKey()
    params = {
        "location": query,
        "size": size
    }

    if not query:
        return JsonResponse({'error': 'Address is not provided'}, status=400)
       
    try:
        data = ChAPI.getChData(url=url, api_key=api_key, params=params)
        response = JsonResponse(data)
        response['Content-Type'] = 'application/json'
        return response
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)