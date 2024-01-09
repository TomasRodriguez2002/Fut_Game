import pygame
from  import Game

class Game(object):

    def __init__(self):
        self.sprites = pygame.sprite.Group()
        self.ball = Ball()
        self.
        self.team1 = [] #usar factory
        self.team1 = 
        self.team2 = [] #usar factory
        #self.player1 = Player((WIDTH // 2)-200, (HEIGHT // 2)-200, self.ball)
        #self.player2 = Player((WIDTH // 2)+23, (HEIGHT // 2)-200, self.ball)
        #self.player1.addTeammate(self.player2)
        #self.player2.addTeammate(self.player1)
        #self.ball.addTeammate(self.player1)
        #self.ball.addTeammate(self.player2)
        #self.sprites.add(self.player1)
        #self.sprites.add(self.player2)
        self.sprites.add(self.ball)
        self.sprites.add(self.team1)
        self.sprites.add(self.team2)

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