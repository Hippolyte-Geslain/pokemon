import pygame
# Initialisation de Pygame
pygame.init()

# Définition des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
RED = (220, 20, 60)

# Dimensions de la fenêtre
WIDTH, HEIGHT = 900, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokémon Menu")

# Charger l'image de fond
fond = pygame.image.load("images/pokemon_fond.jpg")  
fond = pygame.transform.scale(fond, (WIDTH, HEIGHT))

# Charger et jouer la musique de fond
pygame.mixer.init()
pygame.mixer.music.load("music/Title Screen - Dragon Ball Z Dokkan Battle OST Extended.mp3")  # Remplace par ton fichier audio
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Police de texte
font = pygame.font.Font(None, 50)

# Définition des boutons (x, y, largeur, hauteur)
buttons = {
    "Continue": pygame.Rect(350, 220, 200, 50),
    "New": pygame.Rect(350, 320, 200, 50),
    "Pokédex": pygame.Rect(350, 420, 200, 50),
    "Quit": pygame.Rect(350, 520, 200, 50),
}

# État du jeu (pour changer d'écran)
current_screen = "menu"

def draw_menu():
    """Affiche le menu principal."""
    screen.blit(fond, (0, 0))
    for text, rect in buttons.items():
        pygame.draw.rect(screen, BLUE, rect, border_radius=10)
        label = font.render(text, True, WHITE)
        screen.blit(label, (rect.x + 50, rect.y + 10))

def draw_new_screen(title):
    """Affiche un nouvel écran avec un titre spécifique."""
    screen.fill(WHITE)
    label = font.render(title, True, BLACK)
    screen.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT // 2 - label.get_height() // 2))
    pygame.display.flip()

running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for text, rect in buttons.items():
                if rect.collidepoint(event.pos): 
                    if text == "Quit":
                        running = False
                    else:
                        current_screen = text  # Change d'écran

    # Affichage selon l'écran actuel
    if current_screen == "menu":
        draw_menu()
    else:
        draw_new_screen(f"{current_screen} Screen")

    pygame.display.flip()

pygame.quit()
