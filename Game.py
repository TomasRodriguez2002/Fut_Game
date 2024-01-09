import pygame
from Ball import Ball
from players.PlayerTomiRFactory import PlayerTomiRFactory
from players.PlayerGonzaloFactory import PlayerGonzaloFactory
from players.PlayerNicolasFactory import PlayerNicolasFactory
from players.GoalKeeperFactory import GoalKeeperFactory


class Game(object):

    def __init__(self):
        self.sprites = pygame.sprite.Group()
        self.ball = Ball()
        self.playerTomiRFactory = PlayerTomiRFactory()
        self.playerNicolasFactory = PlayerNicolasFactory()
        self.playersField1 = self.playerTomiRFactory.createPlayer()
        self.playersField2 = self.playerNicolasFactory.createPlayer()
        self.goalKeeperFactory = GoalKeeperFactory()
        self.goalKeeper1 = self.goalKeeperFactory.createGoalKeeper()
        self.goalKeeper2 = self.goalKeeperFactory.createGoalKeeper()
        #self.player1 = Player((WIDTH // 2)-200, (HEIGHT // 2)-200, self.ball)
        #self.player2 = Player((WIDTH // 2)+23, (HEIGHT // 2)-200, self.ball)
        self.sprites.add(self.ball)
        self.sprites.add(self.goalKeeper1)
        self.sprites.add(self.goalKeeper2)
        for player in self.playersField1:
            self.sprites.add(player)
        for player in self.playersField2:
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