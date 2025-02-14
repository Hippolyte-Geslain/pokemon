import pygame
from pokemon_manager import test
class menu():
    def __init__(self,screen):
        self.screen = screen
        self.running = True
        self.font = pygame.font.Font(None, 50)
        self.interact_button = pygame.Rect(0,0,0,0)
        
    def button(self,text,x,y,width,height):
        self.interact_button.copy()
        

    def draw_text(self,text,rect,color="white"):
        text_surface = self.font.render(text,True,color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface,text_rect)
    
    def display(self):
        self.screen.fill((30,30,30))

        self.screen.blit(test.image,1,1)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.display()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()