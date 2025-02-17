import pygame
from Combat import Combat, game
from pokemon_manager import PokemonManager
import random

class PokemonGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        # Screen setup
        self.WIDTH, self.HEIGHT = 900, 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pokémon Game")

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (70, 130, 180)
        self.RED = (220, 20, 60)
        self.GREEN = (50, 205, 50)
        self.YELLOW = (255, 255, 0)
        self.CREAM = (248, 248, 232)  
        self.GRAY = (100, 100, 100)
        # Load assets
        self.load_assets()
        
        # Initialize game state
        self.state = "MENU"  # States: MENU, BATTLE, POKEDEX
        self.pm = PokemonManager()
        self.your_pokemon = None
        self.opponent_pokemon = None
        self.battle = None

    def load_assets(self):
        # Background
        self.background = pygame.image.load("images/pokemon_fond.jpg")
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
        
        # Battle background
        self.battle_bg = pygame.image.load("images/battle_background.jpg")
        self.battle_bg = pygame.transform.scale(self.battle_bg, (self.WIDTH, self.HEIGHT))
        
        # Font
        self.font = pygame.font.Font(None, 50)
        
        # Music
        pygame.mixer.music.load("music/Title Screen - Dragon Ball Z Dokkan Battle OST Extended.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def draw_menu(self):
        self.screen.blit(self.background, (0, 0))
        
        buttons = {
            "Continue": pygame.Rect(350, 220, 200, 50),
            "New Game": pygame.Rect(350, 320, 200, 50),
            "Pokédex": pygame.Rect(350, 420, 200, 50),
            "Quit": pygame.Rect(350, 520, 200, 50),
        }

        for text, rect in buttons.items():
            pygame.draw.rect(self.screen, self.BLUE, rect, border_radius=10)
            label = self.font.render(text, True, self.WHITE)
            self.screen.blit(label, (rect.x + 50, rect.y + 10))

        return buttons

    def draw_battle(self):
        self.screen.blit(self.battle_bg, (0, 0))
        
        if self.your_pokemon and self.opponent_pokemon:
            # Your Pokemon (bottom left)
            your_pokemon_pos = (100, 400)
            self.pm.display_pokemon(self.screen, self.your_pokemon, your_pokemon_pos)
            self.draw_hp_bar(self.your_pokemon, (650, 450))
            self.draw_pokemon_stats(self.your_pokemon, (800, 425))
            
            # Opponent Pokemon (top right)
            opponent_pos = (600, 100)
            self.pm.display_pokemon(self.screen, self.opponent_pokemon, opponent_pos)
            self.draw_hp_bar(self.opponent_pokemon, (190, 165))
            self.draw_pokemon_stats(self.opponent_pokemon, (350, 150), is_opponent=True)

    def draw_hp_bar(self, pokemon, position):
        # HP bar background
        bar_bg = pygame.Rect(position[0], position[1], 200, 20)
        pygame.draw.rect(self.screen, self.BLACK, bar_bg)
        
        # HP bar
        hp_ratio = pokemon.hp / pokemon.hp_max
        bar_width = int(196 * hp_ratio)
        bar_color = self.GREEN if hp_ratio > 0.5 else self.YELLOW if hp_ratio > 0.2 else self.RED
        hp_bar = pygame.Rect(position[0] + 2, position[1] + 2, bar_width, 16)
        pygame.draw.rect(self.screen, bar_color, hp_bar)
        
        

    def draw_pokemon_stats(self, pokemon, position, is_opponent=False):
        x, y = position
        
        # Draw Pokemon name and level
        name = self.font.render(f"{pokemon.nom}", True, self.BLACK)
        self.screen.blit(name, (x-260, y - 45))  # Above HP text
        level = self.font.render(f"{pokemon.lvl}", True, self.BLACK)
        self.screen.blit(level, (x, y-35))  # Above HP text
        # HP text
        hp_text = self.font.render(f"{pokemon.hp}/{pokemon.hp_max}", True, self.BLACK)
        self.screen.blit(hp_text, (position[0], position[1] - 30))

    def start_battle(self):
        self.your_pokemon = self.pm.get_pokemon(1)  # For testing, use Bulbasaur
        self.opponent_pokemon = self.pm.get_pokemon(random.randint(1, 151))
        self.battle = Combat(self.your_pokemon, self.opponent_pokemon)
        self.state = "BATTLE"

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.state == "MENU":
                        buttons = self.draw_menu()
                        for text, rect in buttons.items():
                            if rect.collidepoint(event.pos):
                                if text == "Quit":
                                    running = False
                                elif text == "New Game":
                                    self.start_battle()
                    
                    elif self.state == "BATTLE":
                        # Handle battle clicks
                        pass

            # Draw current state
            if self.state == "MENU":
                self.draw_menu()
            elif self.state == "BATTLE":
                self.draw_battle()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = PokemonGame()
    game.run()