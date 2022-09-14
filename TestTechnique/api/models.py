from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField
from django.db.models import Q, F, Value
from django.db.models.functions import Concat


# Constants
DEFAUL_CHAR_LENGTH = 255


class Program(models.Model):
    name = models.CharField(max_length=DEFAUL_CHAR_LENGTH, null=True, help_text="this field represents the name of the program")
    activate = models.BooleanField(default=True, help_text="this field indicate if the program is activate or not")

    @classmethod
    def get_program_with_appartement_contains_specific_criteria(cls, criteria: str):
        """
        this function return a querryset that contains program that the appartements are related at least has the criteria passed in the params
        params : 
            * criteria : string | the specific creteria of the appartement 
        return : 
            * querryset
        """
        return Program.objects.filter(appartement__characteristics__contains=[criteria])



class Appartement(models.Model):
    surface = models.IntegerField(help_text="this field represents the surface of the appartement")
    price = models.IntegerField(validators=[MinValueValidator(1)],help_text="this field represents the price of the appartement | ex : 80k")
    room_count = models.IntegerField(help_text="this field represents Number of room in the appartement")
    program = models.ForeignKey(Program, on_delete=models.CASCADE ,null=True, help_text="this field represents program that related tio this appartement")
    characteristics = ArrayField(models.CharField(max_length=DEFAUL_CHAR_LENGTH), default=list, help_text="this field represents the list of the appartement's characteristics | ex : [piscine]")


    @classmethod
    def get_appartements_with_actif_program(cls):
        """
        this function return a querryset that contains only appartement related to actif program

        return : 
            * querryset
        """
        return Appartement.objects.filter(program__activate=True).all()

    @classmethod
    def get_appartements_with_price_range(cls, min_price: int, max_price: int):
        """
        This function return a querryset that contains only appartement has price between the given min price and the max price
        params : 
            * min_price : integer | the minimum price  
            * max_price : integer | the maximum price 
        return : 
            * querryset
        """
        return Appartement.objects.filter(Q(price__lt=max_price) & Q(price__gt=min_price)).all()

    @classmethod
    def special_offers(cls, offre_code: str):
        """
        This function return a querryset that after a special offre

        # offre_code = PERE NOEL:
            * price minus 5%
            * "PROMO SPECIALE" will be added to the name of the related program
        params : 
            * offre_code : string | code of the offre   
        return : 
            * querryset
        """
        if offre_code == "PERE NOEL":
            return Appartement.objects.annotate(
                price_offre=(F('price') * 0.95),
                libelle_program=Concat(F('program__name'), Value(' PROMO SPECIALE'))
            )
        return Appartement.objects.all()

    