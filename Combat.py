import json
import random
from selectors import SelectorKey
from pokemon_manager import PokemonManager

class Combat:
    def __init__(self, pokemon1, pokemon2):
        self.pokemon_1 = pokemon1
        self.pokemon_2 = pokemon2
        self._load_type_chart()

    def _load_type_chart(self):
        with open('type_chart.json', 'r', encoding='utf-8') as f:
            self.type_chart = json.load(f)

    def calculate_type_multiplier(self, attacker_types, defender_types):
        multiplier = 1.0
        for atk_type in attacker_types:
            for def_type in defender_types:
                atk_name = atk_type['nom'].lower()
                def_name = def_type['nom'].lower()
                if atk_name in self.type_chart and def_name in self.type_chart[atk_name]:
                    multiplier *= self.type_chart[atk_name][def_name]
        return multiplier

    def calculate_damage(self, attacker, defender, move_power=50):
        #Miss Factor
        accuracy = attacker.base.get('Speed',60)
        evasion = defender.base.get('Speed',60)
        ecart = (accuracy - evasion)/300
        base_accuracy = 0.9
        probability_hit = base_accuracy + ecart
        if random.random() < probability_hit:
            # Random factor (87.5% to 100%)
            random_factor = random.randint(217, 255) / 255

            # Type effectiveness
            type_multiplier = self.calculate_type_multiplier(
                attacker.types,
                defender.types
            )

            # Basic damage formula
            # (2 * Level + 10) / 250 * Attack/Defense * Move Power + 2
            level = 50  # Assuming level 50 for this example
            attack = attacker.base.get('Attack', 50)
            defense = defender.base.get('Defense', 50)

            damage = ((2 * level + 10) / 250) * (attack/defense) * move_power + 2
            damage *= random_factor * type_multiplier

            return int(damage)
        else:
            return f'The attack missed'

    def execute_turn(self, attacker, defender):
        damage = self.calculate_damage(attacker, defender)
        print(f"{attacker} is attacking {defender}")
        if isinstance(damage, int):
            defender.take_dmg(damage)
            return f"{attacker.nom} dealt {damage} damage to {defender.nom}\n{defender.nom} has {defender.hp} HP remaining"
        else:
            return damage

    def game_loop(self):
        while not self.pokemon_1.ko and not self.pokemon_2.ko:
            print(self.execute_turn(self.pokemon_1, self.pokemon_2))
            if self.pokemon_2.ko:
                break
            print(self.execute_turn(self.pokemon_2, self.pokemon_1))
            if self.pokemon_1.ko:
                break
        if self.pokemon_1.ko:
            print(f'{self.pokemon_1.nom} is KO, {self.pokemon_2.nom} won the fight!')
        else:
            print(f'{self.pokemon_2.nom} is KO, {self.pokemon_1.nom} won the fight!')

def game():
    

    pm = PokemonManager()
    pikachu = pm.get_pokemon(25)
    staross = pm.get_pokemon(121)
    print()
    # Create battle as random_battle = Combat(pokemon_1,pokemon_2)
    battle = Combat(pikachu, staross)
    #Execute the fight
    battle.game_loop()


game()