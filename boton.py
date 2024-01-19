import pygame

class Boton(pygame.sprite.Sprite):

    def __init__(self, image1, image2, x, y):
        self.normal_image = image1
        self.select_image = image2
        self.actual_image = self.normal_image
        self.rect = self.actual_image.get_rect()
        self.rect.left, self.rect.top = (x,y)

    def update(self, screen, cursor):
        if cursor.colliderect(self.rect):
            self.actual_image = self.select_image
        else:
            self.actual_image = self.normal_image
        screen.blit(self.actual_image, self.rect)