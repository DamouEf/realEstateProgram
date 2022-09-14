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
        program_x: Program = Program.objects.create(name="Program XXX")
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
        program_x: Program = Program.objects.create(name="Program XXX")

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


    def test_get_appartements_with_actif_program(self):
        """
        In this test we will :
            * create appartement A related to an actif program 
            * create appartement B related to not actif program
            * call the function get_appartements_with_actif_program()
        expected : 
            * only the appartement A will be returned 
        """
        
        # initial data
        program_actif: Program = Program.objects.create(name="Program actif",activate=True)
        program_not_actif: Program = Program.objects.create(name="Program not actif",activate=False)

        appartement_a = Appartement.objects.create(
            surface=58,
            price=300, 
            room_count=3,
            program=program_actif,
            characteristics=["proche station ski", "piscine"]
        )
        appartement_b = Appartement.objects.create(
            surface=58,
            price=300, 
            room_count=3,
            program=program_not_actif,
            characteristics=["proche station ski", "piscine"]
        )

        self.assertEquals(Appartement.objects.all().count(), 2)
        appartements = Appartement.get_appartements_with_actif_program()
        self.assertEquals(appartements.count(), 1)
        self.assertEquals(appartements.first().id , appartement_a.id)

    def test_get_appartements_with_price_range(self):
        """
        In this test we will :
            * create appartement A with price in range ( 100 - 180) | example : 150
            * create appartement B not in the price range ( 100 - 180 ) | example 300
            * call the function get_appartements_with_price_range()
        expected : 
            * only the appartement A will be returned 
        """
        
        # initial data
        program_xx: Program = Program.objects.create(name="Program xx",activate=True)
        program_yy: Program = Program.objects.create(name="Program yy",activate=True)

        appartement_a = Appartement.objects.create(
            surface=58,
            price=150, 
            room_count=3,
            program=program_xx,
            characteristics=["proche station ski", "piscine"]
        )
        appartement_b = Appartement.objects.create(
            surface=58,
            price=300, 
            room_count=3,
            program=program_yy,
            characteristics=["proche station ski", "piscine"]
        )

        self.assertEquals(Appartement.objects.all().count(), 2)
        appartements = Appartement.get_appartements_with_price_range(min_price=100, max_price=180)
        self.assertEquals(appartements.count(), 1)
        self.assertEquals(appartements.first().id , appartement_a.id)


    def test_get_program_with_appartement_contains_specific_criteria(self):
        """
        In this test we will :
            * create appartement A with characteristics contains "picine" 
            * create appartement B without characteristics
            * call the function get_program_with_appartement_contains_specific_criteria() and pass "picine" in params
        expected : 
            * only the appartement A will be returned 
        """
        # initial data
        program_xx: Program = Program.objects.create(name="Program xx",activate=True)
        program_yy: Program = Program.objects.create(name="Program yy",activate=True)

        appartement_a = Appartement.objects.create(
            surface=58,
            price=150, 
            room_count=3,
            program=program_xx,
            characteristics=["proche station ski", "piscine"]
        )
        appartement_b = Appartement.objects.create(
            surface=58,
            price=300, 
            room_count=3,
            program=program_yy,
            characteristics=[]
        )

        self.assertEquals(Program.objects.all().count(), 2)
        programs = Program.get_program_with_appartement_contains_specific_criteria(criteria="piscine")
        self.assertEquals(programs.count(), 1)
        self.assertEquals(programs.first().id , program_xx.id)
