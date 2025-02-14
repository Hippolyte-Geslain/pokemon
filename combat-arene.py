import pygame
import random

pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arène Pokémon")
font = pygame.font.Font(None, 36)

class Pokemon:
    def __init__(self, name, hp, attack, defense, x, y):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.x = x
        self.y = y
    
    def take_damage(self, damage):
        self.hp -= max(0, damage - self.defense)
        if self.hp < 0:
            self.hp = 0

    def is_fainted(self):
        return self.hp <= 0
    
    def attack_pokemon(self, opponent):
        damage = max(1, self.attack + random.randint(-5, 5))
        print(f"{self.name} attaque {opponent.name} et inflige {damage} points de dégâts !")
        opponent.take_damage(damage)

def draw_pokemon(pokemon):
    text = font.render(f"{pokemon.name} HP: {pokemon.hp}", True, (255, 255, 255))
    screen.blit(text, (pokemon.x, pokemon.y))

# Création des Pokémon
pikachu = Pokemon("Pikachu", 50, 15, 5, 100, 200)
charmander = Pokemon("Salamèche", 45, 17, 4, 500, 200)

def battle(pokemon1, pokemon2):
    running = True
    clock = pygame.time.Clock()
    
    while running:
        screen.fill((0, 0, 0))
        draw_pokemon(pokemon1)
        draw_pokemon(pokemon2)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pokemon1.attack_pokemon(pokemon2)
        if pokemon2.is_fainted():
            print(f"{pokemon2.name} est K.O. ! {pokemon1.name} remporte le combat !")
            break
        
        pokemon2.attack_pokemon(pokemon1)
        if pokemon1.is_fainted():
            print(f"{pokemon1.name} est K.O. ! {pokemon2.name} remporte le combat !")
            break
        
        pygame.time.delay(1000)
        clock.tick(60)

battle(pikachu, charmander)
pygame.quit()