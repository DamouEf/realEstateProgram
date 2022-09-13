from unicodedata import name
from api.models import Appartement, Program
from django.test import TestCase
from api.views import *
from rest_framework.test import APIClient, RequestsClient, APIRequestFactory
from collections import OrderedDict

class TestApi(TestCase):
    def setUp(self) :

        # Config client
        self.client = APIClient()
        self.factory = APIRequestFactory()

        # URLs
        self.appartement_url = "/api/v1/appartements/"

        # Views
        self.appartement_view = AppartementViews.as_view(actions={'get': 'list'})
        self.appartement_create_view = AppartementViews.as_view(actions={'post': 'create'})


    def test_Appartement_GET(self):
        """
        in this test , we will create a Program object that associated with List of Appartements objects.
        then we will call appartements/ API
        expected result : 
            * status code 200
            * response format : 
            {
                "id": 1,
                "program": {
                    "id": 1,
                    "name": "kilgrdzrxk",
                    "activate": false
                },
                "surface": 25,
                "price": 292,
                "room_count": 1,
                "characteristics": [
                    "asseceur",
                    "parking"
                ]
            } 
        """

        # inital data
        program_x = Program.objects.create(name="Program XXX")
        appartement_1 = Appartement.objects.create(
            surface=58,
            price=300, 
            room_count=3,
            program=program_x,
            characteristics=["proche station ski", "piscine"]
        )

        # test 
        self.assertEquals(Program.objects.all().count(), 1)

        request = self.factory.get(self.appartement_url, format='json')
        response = self.appartement_view(request)
        response.render()

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEquals(response.data[0].get('id'), appartement_1.id)
        self.assertIn("program" , dict(response.data[0]))

        program_object = response.data[0].get("program")
        self.assertEquals(type(program_object), OrderedDict)
        self.assertIn("name", program_object)
        self.assertIn("id", program_object)


    def test_create_appartement_API(self):
        """
        in this test we will create an appartement object through the API appartements/
        expected result :
            * status code : 201
        """

        # initial data
        program_x = Program.objects.create(name="Program XXX")

        payload: dict = {
            "surface": 58,
            "price": 80,
            "room_count": 3,
            "characteristics": [
                "asseceur",
                "parking"
            ],
            "program": program_x.id 
        }

        request = self.factory.post(self.appartement_url, payload, format='json')
        response = self.appartement_create_view(request)
        response.render()

        # test 
        self.assertEquals(response.status_code , 201)
        self.assertEquals(Appartement.objects.all().count(), 1)

        created_appartement = Appartement.objects.all().first()
        self.assertEquals(created_appartement.program.id, program_x.id)


