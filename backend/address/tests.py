from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from rest_framework import status
from address.models import UserData, UserAttribute

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.get_company_data_url = reverse('get_company_data')
        self.add_user_data_url = reverse('add_user_data')
        self.say_hello_url = reverse('say_hello')

    @patch('companies_house.companies_house_api.ChAPI.getChData')
    def test_get_company_data_no_query(self, mock_getChData):
        response = self.client.get(self.get_company_data_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error': 'Address is not provided'})

    @patch('companies_house.companies_house_api.ChAPI.getChData')
    def test_get_company_data_success(self, mock_getChData):
        mock_getChData.return_value = {'data': 'some data'}
        response = self.client.get(self.get_company_data_url, {'query': 'London'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'data': 'some data'})

    @patch('companies_house.companies_house_api.ChAPI.getChData')
    def test_get_company_data_failure(self, mock_getChData):
        mock_getChData.side_effect = Exception('API error')
        response = self.client.get(self.get_company_data_url, {'query': 'London'})
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {'error': 'API error'})

    def test_add_user_data_create_new_user(self):
        data = {
            'email': 'test@example.com',
            'streetNo': '123',
            'streetName': 'Test Street',
            'postcode': '12345',
            'existingBusinesses': 0,
            'additionalAddress': False
        }
        response = self.client.post(self.add_user_data_url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {'message': 'New user test@example.com has been created successfully!'})

    def test_add_user_data_existing_user_attributes_exist(self):
        user = UserData.objects.create(email='test@example.com')
        UserAttribute.objects.create(email=user, streetNo='123', streetName='Test Street', postcode='12345')
        data = {
            'email': 'test@example.com',
            'streetNo': '123',
            'streetName': 'Test Street',
            'postcode': '12345',
            'existingBusinesses': 0,
            'additionalAddress': False
        }
        response = self.client.post(self.add_user_data_url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error': 'User email and address already exist!'})

    def test_add_user_data_existing_user_additional_address(self):
        user = UserData.objects.create(email='test@example.com')
        data = {
            'email': 'test@example.com',
            'streetNo': '123',
            'streetName': 'Test Street',
            'postcode': '12345',
            'existingBusinesses': 0,
            'additionalAddress': True
        }
        response = self.client.post(self.add_user_data_url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_user_data_existing_user_overwrite_attributes(self):
        user = UserData.objects.create(email='test@example.com')
        UserAttribute.objects.create(email=user, streetNo='123', streetName='Test Street', postcode='12345')
        data = {
            'email': 'test@example.com',
            'streetNo': '456',
            'streetName': 'New Street',
            'postcode': '67890',
            'existingBusinesses': 1,
            'additionalAddress': False
        }
        response = self.client.post(self.add_user_data_url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_say_hello(self):
        response = self.client.get(self.say_hello_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'hello.html')
        self.assertContains(response, 'Kevin')
