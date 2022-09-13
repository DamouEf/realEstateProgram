from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField

# Constants
DEFAUL_CHAR_LENGTH = 255


class Program(models.Model):
    name = models.CharField(max_length=DEFAUL_CHAR_LENGTH, null=True, help_text="this field represents the name of the program")
    activate = models.BooleanField(default=True, help_text="this field indicate if the program is activate or not")

class Appartement(models.Model):
    surface = models.IntegerField(help_text="this field represents the surface of the appartement")
    price = models.IntegerField(validators=[MinValueValidator(1)],help_text="this field represents the price of the appartement | ex : 80k")
    room_count = models.IntegerField(help_text="this field represents Number of room in the appartement")
    program = models.ForeignKey(Program, on_delete=models.CASCADE ,null=True, help_text="this field represents program that related tio this appartement")
    characteristics = ArrayField(models.CharField(max_length=DEFAUL_CHAR_LENGTH), default=list, help_text="this field represents the list of the appartement's characteristics | ex : [piscine]")

