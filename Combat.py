import Pokemon, random, json

type_table = 'type_chart.json'

class Combat():
    def __init__(self, pokemon1, pokemon2):
        self.pokemon_1 = pokemon1
        self.pokemon_2 = pokemon2
        self.type_table = type_table
    def type_multiplicator(self):
        multiplicator = self.type_table[self.pokemon_1.type][self.pokemon_2.type]
        return multiplicator
    def random_multiplicator(self):
        random = random.randint(217,255)
        return random
    def power_calculator(self):
        power = 1
    def dmg_calculator(self):
        self.pokemon_1.attack * self.type_multiplicator() * self.random_multiplicator()