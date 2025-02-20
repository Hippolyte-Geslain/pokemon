def some_function():
    from pokemon_manager import PokemonManager
    manager = PokemonManager()
    return manager

class Pokemon():
    def __init__(self, id, nom, types, base, description, image, evolution=None,pm=None):
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
        self.lvl = 15
        self.xp = 99
        self.pm = pm
    
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
            self.level_up()
            self.check_evolution() # Check for evolution on level up

    def level_up(self):
        self.hp_max+=self.hp_max/50
        round(self.hp_max,0)
        self.base['Attack']+=self.base['Attack']/50
        self.base["Attack"]+=self.base["Attack"]/50
        self.base["Defense"]+=self.base["Defense"]/50
        self.base["SpAttack"]+=self.base["SpAttack"]/50
        self.base["SpDefense"]+=self.base["SpDefense"]/50
        self.base["Speed"]+=self.base["Speed"]/50

    def check_evolution(self):
        if self.evolution and self.lvl >= self.evolution['niveau_requis']:
            self.evolve()
            return True

    def evolve(self):
        evolved_pokemon = self.pm.get_pokemon(self.evolution['id'])
        self.id = evolved_pokemon.id
        self.nom = evolved_pokemon.nom
        self.types = evolved_pokemon.types
        self.base = evolved_pokemon.base
        self.description = evolved_pokemon.description
        self.image = evolved_pokemon.image
        self.hp_max = self.base['HP']
        self.hp = self.hp_max
        self.evolution = evolved_pokemon.evolution