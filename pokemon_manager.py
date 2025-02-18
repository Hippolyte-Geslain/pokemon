import json
import pygame
from Pokemon import Pokemon

class PokemonManager:
    def __init__(self):
        self.pokemons = {}  # Dictionary with ID as key and Pokemon instance as value
        self.pokedex = {}  # Dictionary to store Pokédex data
        self._load_pokemons()
        self._load_pokedex()
    
    def _load_pokemons(self):
        with open('pokemon_stats.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        for pokemon_data in data['pokemons']:
            image_path = f"images/{pokemon_data['image']}"
            try:
                pokemon_image = pygame.image.load(image_path).convert_alpha()
            except pygame.error as e:
                print(f"Failed to load image {image_path}: {e}")
                pokemon_image = pygame.Surface((64, 64))  # Create a blank surface as fallback
            
            pokemon = Pokemon(
                id=pokemon_data['id'],
                nom=pokemon_data['nom'],
                types=pokemon_data['types'],
                base=pokemon_data['base'],
                description=pokemon_data['description'],
                image=pokemon_image
            )
            self.pokemons[pokemon.id] = pokemon
    
    def _load_pokedex(self):
        try:
            with open('pokedex.json', 'r', encoding='utf-8') as file:
                self.pokedex = json.load(file)
        except FileNotFoundError:
            self.pokedex = {}

    def save_pokedex(self):
        with open('pokedex.json', 'w', encoding='utf-8') as file:
            json.dump(self.pokedex, file, indent=4)

    def get_pokemon(self, pokemon_id):
        return self.pokemons.get(pokemon_id)
    
    def get_all_pokemons(self):
        return list(self.pokemons.values())
    
    def get_pokemons_by_type(self, type_name):
        return [
            pokemon for pokemon in self.pokemons.values()
            if any(t['nom'] == type_name for t in pokemon.types)
        ]
    
    def get_pokemon_image(self, pokemon_id):
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

    def mark_pokemon_as_seen(self, pokemon_id):
        if pokemon_id not in self.pokedex:
            self.pokedex[pokemon_id] = True
            self.save_pokedex()