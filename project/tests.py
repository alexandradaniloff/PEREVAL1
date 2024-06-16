from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .serializers import PerevalSerializer
from .models import *
from django.urls import reverse
import json


class PerevalTest(APITestCase):
    def setUp(self):
        self.pereval_1 = Pereval.objects.create(
            status='',
            beauty_title='Test1',
            title='Test1',
            other_titles='Test1',
            connect='',

            tourist_id=Users.objects.create(
                email='test1@mail.ru',
                last_name='Test1',
                first_name='Test1',
                patronymic='Test1',
                phone='79998837756'
            ),
            coord_id=Coords.objects.create(
                latitude=56.000000,
                longitude=65.000000,
                height=2655
            ),
            level=Level.objects.create(
                winter_lev='4A',
                summer_lev='',
                autumn_lev='',
                spring_lev=''
            ),
        )
        self.image_1 = Images.objects.create(
            image="",
            title="Test1",
            pereval_id=self.pereval_1
        )

        self.pereval_2 = Pereval.objects.create(
            status='',
            beauty_title='Test2',
            title='Test2',
            other_titles='Test2',
            connect='',

            tourist_id=Users.objects.create(
                email='test2@mail.ru',
                last_name='Test2',
                first_name='Test2',
                patronymic='Test2',
                phone='79998837752'
            ),
            coord_id=Coords.objects.create(
                latitude=56.000002,
                longitude=65.000002,
                height=2652
            ),
            level=Level.objects.create(
                winter_lev='4A',
                summer_lev='3A',
                autumn_lev='',
                spring_lev=''
            ),
        )
        self.image_2 = Images.objects.create(
            image="",
            title="Test2",
            pereval_id=self.pereval_2
        )
        # проверяем получение всех записей о перевалах
    def test_get_list(self):
        url = reverse('perevals-list')
        response = self.client.get(url)
        serializer_data = PerevalSerializer([self.pereval_1, self.pereval_2], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(len(serializer_data), 2)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    #проверяем получение записи о втором перевале
    def test_perevall_detail(self):
        response = self.client.get(reverse('perevals-detail', kwargs={'pk': self.pereval_2.id}))
        serializer_data = PerevalSerializer(self.pereval_2).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_valid_create_and_user_reuse(self):
        data = {
        "beauty_title": "title_9",
        "title": "title_1",
        "other_titles": "title_1",
        "connect": "title_1",
        "tourist_id": {

            "email": "test1@mail.ru",
            "last_name": "Test1",
            "first_name": "Test1",
            "patronymic": "Test1",
            "phone": "79998837756"
        },
        "coord_id": {

            "latitude": "54.87690019",
            "longitude": "43.36759009",
            "height": 1244
        },
        "level": {

            "winter_lev": "4A",
            "spring_lev": "2A",
            "summer_lev": "1A",
            "autumn_lev": "3A"
        },
        "images": []
    }

        response = self.client.post(reverse('perevals-list'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Pereval.objects.all().count(), 3)
        self.assertEqual(Users.objects.all().count(), 2)

    def test_invalid_create(self):
        data = {
        "beauty_title": "",
        "title": "",
        "other_titles": "",
        "connect": "",
        "tourist_id": {

            "email": "",
            "last_name": "",
            "first_name": "",
            "patronymic": "Иванович",
            "phone": "2222222223"
        },
        "coord_id": {

            "latitude": "54.87690019",
            "longitude": "43.36759009",
            "height": 1244
        },
        "level": {

            "winter_lev": "4A",
            "spring_lev": "2A",
            "summer_lev": "1A",
            "autumn_lev": "3A"
        },
        "images": []
    }

        json_data = json.dumps(data)
        response = self.client.post(reverse('perevals-list'), data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Pereval.objects.all().count(), 2)

# проверяем отсутствие обновления разрешенных данных, если статус не new
    def test_invalid_update_if_status_is_not_new(self):
        data = {
        "status": "PN",
        "beauty_title": "title_10",
        "title": "title_1",
        "other_titles": "title_1",
        "connect": "",
        "tourist_id": {

            "email": "ivanov@gmail.ru",
            "last_name": "Иванов",
            "first_name": "Иван",
            "patronymic": "Иванович",
            "phone": "2222222223"
        },
        "coord_id": {

            "latitude": "54.87690019",
            "longitude": "43.36759009",
            "height": 1244
        },
        "level": {

            "winter_lev": "4A",
            "spring_lev": "2A",
            "summer_lev": "1A",
            "autumn_lev": "3A"
        },
        "images": []
    }

        json_data = json.dumps(data)
        response = self.client.patch(reverse('perevals-detail', kwargs={'pk': self.pereval_2.id}),
            data=json_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pereval_2.refresh_from_db()
        self.assertEqual('', self.pereval_2.connect)