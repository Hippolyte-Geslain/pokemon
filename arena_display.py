import pygame
import Combat
from pokemon_manager import PokemonManager
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
RED = (220, 20, 60)

WIDTH, HEIGHT = 900, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
fond = pygame.image.load("images/pokemon_fond.jpg")
fond = pygame.transform.scale(fond, (WIDTH, HEIGHT))
pygame.display.set_caption("Pokémon Fight")
pm = PokemonManager()

arena = BLACK
pokemon1 = pm.get_pokemon_image(2)
font = pygame.font.Font(None, 50)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # **Afficher l'image de fond**
    screen.blit(fond,(0,0))

    # Dessiner les pokemonns
    screen.blit(pokemon1,(0,0))

    pygame.display.flip()  # Mise à jour de l'affichage