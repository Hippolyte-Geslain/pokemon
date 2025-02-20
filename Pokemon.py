def some_function():
    from pokemon_manager import PokemonManager  # Moved inside function
    manager = PokemonManager()

class Pokemon():
    def __init__(self, id, nom, types, base, description, image, evolution=None):
        self.id = id
        self.nom = nom
        self.types = types
        self.base = base
        self.description = description
        self.image = image
        self.evolution = evolution  # Add evolution data
        self.ko = False
        self.pokedex = False
        self.hp_max = base['HP']
        self.hp = self.hp_max
        self.lvl = 5
        self.xp = 0
    
    def __str__(self):
        return self.nom

    def take_dmg(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.is_ko()

    def heal_hp(self, amount):
        self.hp += amount
        if self.hp > self.hp_max:
            self.hp = self.hp_max

    def is_ko(self):
        self.ko = True

    def mark_as_seen(self):
        self.pokedex = True
    
    def xp_to_lvl(self):
        while self.xp > 100:
            self.xp -= 100
            self.lvl += 1
            self.check_evolution()  # Check for evolution on level up

    def check_evolution(self):
        if self.evolution and self.lvl >= self.evolution['niveau_requis']:
            self.evolve()
            return True

    def evolve(self):
        # Assuming we have a function get_pokemon_by_id to fetch Pokémon data by ID
        evolved_pokemon_data = some_function.get_pokemon(self.evolution['id'])
        self.id = evolved_pokemon_data['id']
        self.nom = evolved_pokemon_data['nom']
        self.types = evolved_pokemon_data['types']
        self.base = evolved_pokemon_data['base']
        self.description = evolved_pokemon_data['description']
        self.image = evolved_pokemon_data['image']
        self.hp_max = self.base['HP']
        self.hp = self.hp_max
        self.evolution = evolved_pokemon_data.get('evolution', None)