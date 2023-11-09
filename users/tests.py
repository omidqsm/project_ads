from django.db import IntegrityError
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase, APIClient
from django.core import exceptions

from users.models import User


LOGIN_URL = reverse('knox_login')
SIGNUP_URL = reverse('signup')
CURRENT_USER_URL = reverse('user_me')
LOGOUT_URL = reverse('knox_logout')


def token_login(client: APIClient, **credentials):
    """logs in the client object and associate it with an authorization header"""
    response: Response = client.post(LOGIN_URL, data=credentials)
    client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])
    return response


class UsersTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        User.objects.create_user(username='omid@gmail.com', password='1234@ABZ')

    def test_signup(self):
        """ensure we can create a user"""
        data = {
            'username': 'ali@gmail.com',
            'password': '5678@$AFD',
            're_password': '5678@$AFD',
        }
        response: Response = self.client.post(SIGNUP_URL, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get(username='ali@gmail.com').username, data['username'])

    def test_login(self):
        """test token based authentication"""
        response: Response = token_login(self.client, username='omid@gmail.com', password='1234@ABZ')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['token'])
        self.assertEqual(response.data['user']['username'], 'omid@gmail.com')

    def test_authenticated_access(self):
        """test if after login we can access authenticated url"""

        # test unauthenticated access
        response = self.client.get(CURRENT_USER_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # test authenticated access
        token_login(self.client, username='omid@gmail.com', password='1234@ABZ')
        response = self.client.get(CURRENT_USER_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'omid@gmail.com')

    def test_logout(self):
        """test if we can log out after authentication"""
        token_login(self.client, username='omid@gmail.com', password='1234@ABZ')

        # test logout
        response = self.client.post(LOGOUT_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # test an endpoint by invalid token
        response = self.client.get(CURRENT_USER_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_email_uniqueness(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username='omid@gmail.com', password='olmsa@dls')
