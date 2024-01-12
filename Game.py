import pygame
from Constantes import *
from Ball import Ball
from Mediator import Mediator
from players.TeamTomasRFactory import TeamTomasRFactory
from players.TeamNicolasFactory import TeamNicolasFactory
pygame.font.init()
font = pygame.font.Font(None, 100)

class Game(object):

    def __init__(self):
        self.sprites = pygame.sprite.Group()
        self.initialize_game()

    def initialize_game(self):
        self.sprites = pygame.sprite.Group()
        self.ball = Ball()
        self.mediator = Mediator()
        self.nicolasFactory = TeamNicolasFactory("sprites/playerNico(Peruano).png", self.mediator, True, 5)
        self.team1 = self.nicolasFactory.create()
        self.tomasRFactory = TeamTomasRFactory("player.png", self.mediator, False, 5)
        self.team2 = self.tomasRFactory.create()
        self.sprites.add(self.ball)
        self.mediator.setBall(self.ball)
        for player in self.team1:
            self.mediator.addPlayer1(player)
            self.sprites.add(player)
        for player in self.team2:
            self.mediator.addPlayer2(player)
            self.sprites.add(player)
        self.mediator.restart_positions()

    def reset_game(self):
        self.sprites.empty()  # Elimina todos los sprites actuales
        self.initialize_game()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                # Verificar si se presionó Ctrl+R para resetear el juego
                if event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.reset_game()
        return False

    def run_logic(self):
        self.sprites.update()

    def display_frame(self, screen, background):
        screen.blit(background, [0 , 0])
        self.sprites.draw(screen)
        if self.current_goal_message:
            screen.blit(self.current_goal_message, ((WIDTH - self.current_goal_message.get_width()) // 2, HEIGHT // 2))
            # Reduzca el temporizador del mensaje de gol en cada iteración
            self.goal_message_timer -= 1
            if self.goal_message_timer <= 0:
                self.current_goal_message = None  # Borra el mensaje cuando el temporizador llega a cero
        pygame.display.flip()

    def show_goal_message(self, message, duration):
            self.goal_message_timer = duration
            self.current_goal_message = font.render(message, True, (255, 255, 255))  # Color blanco