import json
import random
from api.models import Chambre, Intervenant, Controle

# clean database
Controle.objects.all().delete()
Chambre.objects.all().delete()
Intervenant.objects.all().delete()

with open("scripts/data_set/data.json", 'r') as input_file:
    data = json.loads(input_file.read())

for room in data.get("chambres", []):
    Chambre.objects.create(**room)

for inter in data.get("intervenants", []):
    Intervenant.objects.create(**inter)

intervs = list(Intervenant.objects.all())
for contr in data.get("controles", []):
    contr["chambre"] = Chambre.objects.all().first()
    c = Controle.objects.create(**contr)
    for i in range(0, (random.randint(0, 3))):
        random_itervenant = random.choice(intervs)
        c.intervenants.add(random_itervenant)