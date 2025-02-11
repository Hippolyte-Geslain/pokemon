import json
from Pokemon import Pokemon

class PokemonManager:
    def __init__(self):
        self.pokemons = {}  # Dictionary with ID as key and Pokemon instance as value
        self._load_pokemons()
    
    def _load_pokemons(self):
        """Load pokemons from JSON file and create Pokemon instances"""
        with open('pokemon_stats.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        for pokemon_data in data['pokemons']:
            pokemon = Pokemon(
                id=pokemon_data['id'],
                nom=pokemon_data['nom'],
                types=pokemon_data['types'],
                base=pokemon_data['base'],
                description=pokemon_data['description'],
                image=pokemon_data['image']
            )
            self.pokemons[pokemon.id] = pokemon
    
    def get_pokemon(self, pokemon_id):
        """Get a pokemon by its ID"""
        return self.pokemons.get(pokemon_id)
    
    def get_all_pokemons(self):
        """Get all pokemon instances"""
        return list(self.pokemons.values())
    
    def get_pokemons_by_type(self, type_name):
        """Get all pokemons of a specific type"""
        return [
            pokemon for pokemon in self.pokemons.values()
            if any(t['nom'] == type_name for t in pokemon.types)
        ]