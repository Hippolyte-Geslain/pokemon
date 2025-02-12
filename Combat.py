import json
from random import randint

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
                # Convert type names to lowercase for matching with type_chart
                atk_name = atk_type['nom'].lower()
                def_name = def_type['nom'].lower()
                if atk_name in self.type_chart and def_name in self.type_chart[atk_name]:
                    multiplier *= self.type_chart[atk_name][def_name]
        return multiplier

    def calculate_damage(self, attacker, defender, move_power=50):
        # Random factor (87.5% to 100%)
        random_factor = randint(217, 255) / 255

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

    def execute_turn(self, attacker, defender):
        """Execute one turn of combat"""
        damage = self.calculate_damage(attacker, defender)
        defender.take_dmg(damage)
        
        return {
            'attacker': attacker.nom,
            'defender': defender.nom,
            'damage': damage,
            'defender_hp': defender.hp
        }

# Example usage
def battle_example():
    from pokemon_manager import PokemonManager

    # Initialize
    pm = PokemonManager()
    pikachu = pm.get_pokemon(25)  # Pikachu
    staross = pm.get_pokemon(121)  # staross
    print()
    # Create battle
    battle = Combat(pikachu, staross)

    # Execute one turn
    result = battle.execute_turn(pikachu, staross)
    print(f"{result['attacker']} dealt {result['damage']} damage to {result['defender']}")
    print(f"{result['defender']} has {result['defender_hp']} HP remaining")
    result = battle.execute_turn(staross,pikachu)
    print(f"{result['attacker']} dealt {result['damage']} damage to {result['defender']}")
    print(f"{result['defender']} has {result['defender_hp']} HP remaining")

battle_example()