import pygame

class Boton(pygame.sprite.Sprite):

    def __init__(self, image1_path, image2_path, x, y):
        self.normal_image = pygame.image.load(image1_path).convert()
        self.select_image = pygame.image.load(image2_path).convert()
        self.actual_image = self.normal_image
        self.rect = self.actual_image.get_rect()
        self.rect.left, self.rect.top = (x,y)
        self.isPush = False
        self.boton_sound = pygame.mixer.Sound("Sounds/boton.wav")

    def push(self): 
        self.boton_sound.play()           
        self.isPush = not self.isPush

    def update(self, screen, cursor):
        if cursor.colliderect(self.rect):
            self.actual_image = self.select_image
        elif not self.isPush:
            self.actual_image = self.normal_image
        screen.blit(self.actual_image, self.rect)