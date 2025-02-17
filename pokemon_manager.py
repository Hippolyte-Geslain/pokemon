import json
from Pokemon import Pokemon
import pygame
class PokemonManager:
    def __init__(self):
        self.pokemons = {}  # Dictionary with ID as key and Pokemon instance as value
        self._load_pokemons()
    
    def _load_pokemons(self):
        with open('pokemon_stats.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        for pokemon_data in data['pokemons']:
            image_path = f"images/{pokemon_data['image']}"
            pokemon = Pokemon(
                id=pokemon_data['id'],
                nom=pokemon_data['nom'],
                types=pokemon_data['types'],
                base=pokemon_data['base'],
                description=pokemon_data['description'],
                image=pygame.image.load(image_path)
            )
            self.pokemons[pokemon.id] = pokemon
    
    def get_pokemon(self, pokemon_id):
        return self.pokemons.get(pokemon_id)
    
    def get_all_pokemons(self):
        return list(self.pokemons.values())
    
    def get_pokemons_by_type(self, type_name):
        return [
            pokemon for pokemon in self.pokemons.values()
            if any(t['nom'] == type_name for t in pokemon.types)
        ]
    def get_pokemon_image(self,pokemon_id):
        return self.get_pokemon(pokemon_id).image

    def display_pokemon(self, screen, pokemon, position):
        """Display a pokemon at the given position on screen"""
        if pokemon and hasattr(pokemon, 'image'):
            try:
                # Scale image if needed (optional)
                scaled_image = pygame.transform.scale(pokemon.image, (150, 150))  # Adjust size as needed
                screen.blit(scaled_image, position)
                
            except pygame.error as e:
                print(f"Error displaying Pokemon {pokemon.nom}: {e}")
                # Create a fallback surface if image fails to display
                fallback = pygame.Surface((150, 150))
                fallback.fill((100, 100, 100))  # Gray color
                screen.blit(fallback, position)