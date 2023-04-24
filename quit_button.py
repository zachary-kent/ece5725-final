import pygame
from pygame.locals import *



 
pygame.init()

size = width, height = 320, 240 
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

font = pygame.font.Font(None, 64)
white = (255, 255, 255)
quit_text = font.render("Quit", True, white)
quit_rect = quit_text.get_rect(centerx = width // 2, y = 3 * height // 4)

quit_clicked = False


try:
  # timer = Timeout(10)
  while not quit_clicked:
    screen.blit(quit_text, quit_rect)
    for event in pygame.event.get():
      quit_clicked = event.type == MOUSEBUTTONDOWN and quit_rect.collidepoint(event.pos)
    pygame.display.flip()
    clock.tick(60)
    
    
  
finally:
  pygame.quit()
