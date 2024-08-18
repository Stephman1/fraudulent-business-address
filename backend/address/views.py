from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status

from . import models, serializers
from . import models
from .models import  UserData, UserAttribute
from companies_house.companies_house_api import ChAPI

class UserDataViewSet(viewsets.ModelViewSet):
  queryset = models.UserData.objects.all()
  serializer_class = serializers.UserDataSerializer


@api_view(['GET'])
def get_company_data(request):
    query = request.GET.get('query') 
    size = request.GET.get('size', 1000)
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
        email = request.data.get('email')
        streetNo = request.data.get('streetNo')
        streetName = request.data.get('streetName')
        postcode = request.data.get('postcode')
        existingBusinesses = request.data.get('existingBusinesses', 0)
        additionalAddress = request.data.get('additionalAddress', False)
        
        try:
            user = UserData.objects.get(email=email)
        except UserData.DoesNotExist:
            user = None
        
        if user:
            # Check if attributes already exist
            existing_attributes = UserAttribute.objects.filter(
                email=user,
                streetNo=streetNo,
                streetName=streetName,
                postcode=postcode,
            )
            
            if existing_attributes.exists():
                return Response({'error': 'User email and address already exist!'}, status=status.HTTP_400_BAD_REQUEST)
            
            if additionalAddress:
                # Add new attributes
                new_attribute = UserAttribute(
                    email=user,
                    streetNo=streetNo,
                    streetName=streetName,
                    postcode=postcode,
                    existingBusinesses=existingBusinesses,
                )
                new_attribute.save()
            else:
                # Overwrite existing attributes
                UserAttribute.objects.filter(email=user).delete()
                new_attribute = UserAttribute(
                    email=user,
                    streetNo=streetNo,
                    streetName=streetName,
                    postcode=postcode,
                    existingBusinesses=existingBusinesses,
                )
                new_attribute.save()
        else:
            # Create new user and attributes
            user = UserData(email=email)
            user.save()
            new_attribute = UserAttribute(
                email=user,
                streetNo=streetNo,
                streetName=streetName,
                postcode=postcode,
                existingBusinesses=existingBusinesses,
            )
            new_attribute.save()

        return Response({'message': f'New user {email} has been created successfully!'}, status=status.HTTP_201_CREATED)