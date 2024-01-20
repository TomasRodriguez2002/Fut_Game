import pygame

class Boton(pygame.sprite.Sprite):

    def __init__(self, image1_path, image2_path, x, y):
        self.normal_image = pygame.image.load(image1_path).convert()
        self.select_image = pygame.image.load(image2_path).convert()
        self.actual_image = self.normal_image
        self.rect = self.actual_image.get_rect()
        self.rect.left, self.rect.top = (x,y)

    def update(self, screen, cursor):
        if cursor.colliderect(self.rect):
            self.actual_image = self.select_image
        else:
            self.actual_image = self.normal_image
        screen.blit(self.actual_image, self.rect)