import pygame
from Ball import Ball
from Mediator import Mediator

class Game(object):

    def __init__(self):
        self.sprites = pygame.sprite.Group()
        self.ball = Ball()
        self.nicolasFactory = TeamNicolasFactory()
        self.team1 = self.nicolasFactory.create()
        self.tomasGFactory = TeamTomasGFactory()
        self.team2 = self.tomasGFactory.create()
        self.mediator = Mediator()
        self.mediator.setBall(self.ball)
        self.sprites.add(self.ball)
        for player in self.team1:
            self.mediator.addPlayer1(player)
            self.sprites.add(player)
        for player in self.team2:
            self.mediator.addPlayer2(player)
            self.sprites.add(player)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def run_logic(self):
        self.sprites.update()

    def display_frame(self, screen, background):
        screen.blit(background, [0 , 0])
        self.sprites.draw(screen)
        pygame.display.flip()