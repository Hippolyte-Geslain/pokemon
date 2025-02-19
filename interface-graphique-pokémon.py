import pygame
from Combat import Combat
from pokemon_manager import PokemonManager
from player_manager import PlayerManager
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
        self.state = "PLAYER_SELECT"  # States: MENU, BATTLE, POKEDEX, PLAYER_SELECT, END
        self.pm = PokemonManager()
        self.player_manager = PlayerManager()
        self.current_player = None
        self.selected_pokemon = None
        self.your_pokemon = None
        self.opponent_pokemon = None
        self.battle = None
        self.end_message = ""
        self.new_player_name = ""
        self.scroll_offset = 0

    def load_assets(self):
        # Background
        try:
            self.background = pygame.image.load("images/pokemon_fond.jpg")
            self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
        except pygame.error as e:
            print(f"Failed to load background image: {e}")

        # Battle background
        try:
            self.battle_bg = pygame.image.load("images/battle_background.jpg")
            self.battle_bg = pygame.transform.scale(self.battle_bg, (self.WIDTH, self.HEIGHT))
        except pygame.error as e:
            print(f"Failed to load battle background image: {e}")

        # Font
        self.font = pygame.font.Font(None, 50)

        # Music
        try:
            pygame.mixer.music.load("music/Title Screen - Dragon Ball Z Dokkan Battle OST Extended.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Failed to load or play music: {e}")

    def draw_menu(self):
        self.screen.blit(self.background, (0, 0))

        buttons = {
            "Play": pygame.Rect(300, 220, 300, 70),
            "Pokédex": pygame.Rect(300, 320, 300, 70),
            "Player Select": pygame.Rect(300, 420, 300, 70),
            "Quit": pygame.Rect(300, 520, 300, 70),
        }

        for text, rect in buttons.items():
            pygame.draw.rect(self.screen, self.BLUE, rect, border_radius=10)
            label = self.font.render(text, True, self.WHITE)
            self.screen.blit(label, (rect.x + 50, rect.y + 10))

        return buttons

    def draw_player_select(self):
        self.screen.fill(self.CREAM)
        title = self.font.render("Select Player", True, self.BLACK)
        self.screen.blit(title, (self.WIDTH // 2 - title.get_width() // 2, 50))

        y_offset = 150
        buttons = {}
        players = self.player_manager.load_players()
        for player_name in players:
            button = pygame.Rect(350, y_offset, 200, 50)
            pygame.draw.rect(self.screen, self.BLUE, button, border_radius=10)
            label = self.font.render(player_name, True, self.WHITE)
            self.screen.blit(label, (button.x + 50, button.y + 10))
            buttons[player_name] = button
            y_offset += 100

        # New player input
        new_player_button = pygame.Rect(350, y_offset, 200, 50)
        pygame.draw.rect(self.screen, self.BLUE, new_player_button, border_radius=10)
        label = self.font.render("New Player", True, self.WHITE)
        self.screen.blit(label, (new_player_button.x + 50, new_player_button.y + 10))
        buttons["New Player"] = new_player_button

        return buttons

    def draw_pokedex(self):
        self.screen.fill(self.CREAM)
        title = self.font.render("Pokédex", True, self.BLACK)
        self.screen.blit(title, (self.WIDTH // 2 - title.get_width() // 2, 50))

        y_offset = 150 + self.scroll_offset  # Apply scroll offset
        x_offset = 100
        col_count = 0
        row_height = 200
        col_width = 200
        buttons = {}

        if self.current_player:
            fought_pokemon = self.player_manager.get_player_data(self.current_player)['fought_pokemon']
            for pokemon_id in fought_pokemon:
                pokemon = self.pm.get_pokemon(pokemon_id)
                if pokemon:
                    button = pygame.Rect(x_offset, y_offset, 150, 150)
                    self.pm.display_pokemon(self.screen, pokemon, (x_offset, y_offset))
                    name = self.font.render(pokemon.nom, True, self.BLACK)
                    self.screen.blit(name, (x_offset + 75 - name.get_width() // 2, y_offset + 150))
                    buttons[pokemon_id] = button
                    col_count += 1
                    if col_count >= 4:  # Move to next row after 4 columns
                        col_count = 0
                        y_offset += row_height
                        x_offset = 100
                    else:
                        x_offset += col_width

        # Draw a button to return to the menu
        menu_button = pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT - 100, 200, 50)
        pygame.draw.rect(self.screen, self.BLUE, menu_button, border_radius=10)
        label = self.font.render("Menu", True, self.WHITE)
        self.screen.blit(label, (menu_button.x + 50, menu_button.y + 10))
        buttons["Menu"] = menu_button

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

            # Draw attack button
            attack_button = pygame.Rect(350, 600, 200, 50)
            pygame.draw.rect(self.screen, self.BLUE, attack_button, border_radius=10)
            label = self.font.render("Attack", True, self.WHITE)
            self.screen.blit(label, (attack_button.x + 50, attack_button.y + 10))

            return attack_button

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
        self.screen.blit(name, (x - 260, y - 45))  # Above HP text
        level = self.font.render(f"{pokemon.lvl}", True, self.BLACK)
        self.screen.blit(level, (x, y - 35))  # Above HP text
        # HP text
        hp_text = self.font.render(f"{pokemon.hp} {pokemon.hp_max}", True, self.BLACK)
        if not is_opponent:
            self.screen.blit(hp_text, (position[0]-75, position[1]+57))

    def draw_end_screen(self, message):
        self.screen.fill(self.BLACK)
        end_text = self.font.render(message, True, self.WHITE)
        text_rect = end_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.blit(end_text, text_rect)

        # Draw a button to return to the menu
        menu_button = pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT // 2 + 50, 200, 50)
        pygame.draw.rect(self.screen, self.BLUE, menu_button, border_radius=10)
        label = self.font.render("Menu", True, self.WHITE)
        self.screen.blit(label, (menu_button.x + 50, menu_button.y + 10))

        return menu_button

    def start_battle(self):
        if self.selected_pokemon:
            self.your_pokemon = self.pm.get_pokemon(self.selected_pokemon)
        else:
            self.your_pokemon = self.pm.get_pokemon(1)  # Default to Bulbasaur if none selected
        self.opponent_pokemon = self.pm.get_pokemon(random.randint(1, 151))
        self.battle = Combat(self.your_pokemon, self.opponent_pokemon)
        self.state = "BATTLE"
        if self.current_player:
            self.player_manager.add_fought_pokemon(self.current_player, self.your_pokemon.id)
            self.player_manager.add_fought_pokemon(self.current_player, self.opponent_pokemon.id)

    def execute_turn(self):
        # Player's turn
        damage = self.battle.calculate_damage(self.your_pokemon, self.opponent_pokemon)
        self.opponent_pokemon.take_dmg(damage)

        if self.opponent_pokemon.ko:
            self.state = "END"
            self.end_message = "You Win!"
            return

        # Opponent's turn
        pygame.time.delay(1000)  # Add delay for opponent's turn
        damage = self.battle.calculate_damage(self.opponent_pokemon, self.your_pokemon)
        self.your_pokemon.take_dmg(damage)

        if self.your_pokemon.ko:
            self.state = "END"
            self.end_message = "Game Over"

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
                                elif text == "Play":
                                    self.start_battle()
                                elif text == "Pokédex":
                                    self.state = "POKEDEX"
                                elif text =='Player Select':
                                    self.state = 'PLAYER_SELECT'

                    elif self.state == "BATTLE":
                        attack_button = self.draw_battle()
                        if attack_button.collidepoint(event.pos):
                            self.execute_turn()

                    elif self.state == "END":
                        menu_button = self.draw_end_screen(self.end_message)
                        if menu_button.collidepoint(event.pos):
                            self.state = "MENU"

                    elif self.state == "POKEDEX":
                        self.scroll_offset = 0
                        buttons = self.draw_pokedex()
                        for pokemon_id, rect in buttons.items():
                            if rect.collidepoint(event.pos):
                                if pokemon_id == "Menu":
                                    self.state = "MENU"
                                else:
                                    self.selected_pokemon = pokemon_id
                                    self.start_battle()

                    elif self.state == "PLAYER_SELECT":
                        buttons = self.draw_player_select()
                        for player_name, rect in buttons.items():
                            if rect.collidepoint(event.pos):
                                if player_name == "New Player":
                                    self.new_player_name = input("Enter new player name: ")
                                    self.player_manager.create_player(self.new_player_name)
                                    self.current_player = self.new_player_name
                                else:
                                    self.current_player = player_name
                                self.state = "MENU"

                if event.type == pygame.MOUSEWHEEL:
                    if self.state == "POKEDEX":
                        self.scroll_offset += event.y * 20

            # Draw current state
            if self.state == "MENU":
                self.draw_menu()
            elif self.state == "BATTLE":
                self.draw_battle()
            elif self.state == "END":
                self.draw_end_screen(self.end_message)
            elif self.state == "POKEDEX":
                self.draw_pokedex()
            elif self.state == "PLAYER_SELECT":
                self.draw_player_select()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = PokemonGame()
    game.run()