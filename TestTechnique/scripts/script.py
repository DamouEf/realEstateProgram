
import random, string, json


# constantes
BOOL: list = [True, False]
CHARACTERISTICS: list = ["proche station ski", "piscine", "jardin", "cave", "parking", "asseceur", "proche station metro"]

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

# create programmes (10) 
result: list = []
id_appartement: int = 1
for id_program in range(1, 11):
    result.append({
        "model": "api.program",
        "pk": id_program,
        "fields": {
            "name": randomword(length=random.randint(5, 10)),
            "activate": random.choice(BOOL)
        }
    })

    for index in range(1, 21):
        # create appartements (20 per program)
        result.append({
            "model": "api.appartement",
            "pk": id_appartement,
            "fields": {
                "surface": random.randint(17, 80),
                "price": random.randint(80, 300),
                "room_count": random.randint(1, 5),
                "program": id_program,
                "characteristics": [random.choice(CHARACTERISTICS), random.choice(CHARACTERISTICS)]
            }
        })
        id_appartement += 1

with open('./data_set/sample.json', 'w') as data_set:
    data_set.write(json.dumps(result))



