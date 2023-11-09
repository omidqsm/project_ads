from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from advertisements.models import Advertisement, Comment
from users.models import User
from users.tests import token_login

# url for listing and creating entities
ADVERTISEMENT_LIST_URL = reverse('advertisement-list')
ADVERTISEMENT_DETAIL_URL = reverse('advertisement-list')
COMMENT_LIST_URL = reverse('comment-list')


class AdvertisementsTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        omid = User.objects.create_user(username='omid@gmail.com', password='omid@1234')
        gholi = User.objects.create_user(username='gholi@gmail.com', password='gholi@1234')

        ali = User.objects.create_user(username='ali@gmail.com', password='ali@1234')
        ad1 = Advertisement(text='Xiaomi is amazing!', owner=ali)
        ad1.save()
        ad2 = Advertisement(text='Sony can make your dreams come true!', owner=ali)
        ad2.save()
        comment1 = Comment(owner=omid, text='Oh no it cannot, you liar!', advertisement=ad2)
        comment1.save()
        comment2 = Comment(owner=gholi, text='I tested it, it really made my dreams come true',
                           advertisement=ad2)
        comment2.save()
        ad2.comments.set([comment1, comment2])

    def test_anonymous_user_can_see_all_advertisements(self):
        response = self.client.get(ADVERTISEMENT_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_advertisement(self):
        token_login(self.client, username='omid@gmail.com', password='omid@1234')
        data = {
            'text': 'Apple is good, buy it!'
        }
        response = self.client.post(ADVERTISEMENT_LIST_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_comment_only_once_for_an_advertisement(self):
        ali = User.objects.get(username='ali@gmail.com')
        ad = ali.advertisements.first()
        gholi = User.objects.get(username='gholi@gmail.com')
        comment = Comment(text='this ad is crazy!', owner=gholi, advertisement=ad)
        comment.save()
        with self.assertRaises(IntegrityError):
            comment = Comment(text='awsome ad!', owner=gholi, advertisement=ad)
            comment.save()

    def test_only_owner_can_edit_or_delete_advertisement(self):
        ali = User.objects.get(username='ali@gmail.com')
        ad = Advertisement(text='Sony is unbelievable!', owner=ali)
        ad.save()
        url = f'{ADVERTISEMENT_DETAIL_URL}{ad.id}/'

        # edit/delete as an anonymous user
        response = self.client.put(url, data={'text': 'anonymous text!'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # edit/delete as a non-owner user
        token_login(self.client, username='omid@gmail.com', password='omid@1234')
        response = self.client.put(url, data={'text': 'non owner text!'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # edit/delete as owner
        token_login(self.client, username='ali@gmail.com', password='ali@1234')
        modified_text = 'owner text!'
        response = self.client.put(url, data={'text': modified_text})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(modified_text, response.data.get('text'))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(ObjectDoesNotExist):
            Advertisement.objects.get(pk=ad.id)
