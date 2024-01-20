import pygame, random
from Constantes import *
from Ball import Ball
from Mediator import Mediator
from players.TeamNicolasFactory import TeamNicolasFactory
from players.TeamTomasGFactory import TeamTomasGFactory
from players.TeamGonzaloFactory import TeamGonzaloFactory
from players.TeamMateoFactory import TeamMateoFactory
from players.TeamBraianFactory import TeamBraianFactory
from players.TeamTomasRFactory import TeamTomasRFactory

pygame.font.init()
font = pygame.font.Font(None, 100)

class Game(object):

    def __init__(self, team1_name, team2_name):
        self.team1_name = team1_name
        self.team2_name = team2_name
        self.team2 = None
        self.team1 = None
        self.ball = None
        self.mediator = None
        self.goal_message = None
        self.current_goal_message = None
        self.sprites = pygame.sprite.Group()
        self.initialize_game()

    def initialize_game(self):
        self.goal_message = None         
        self.current_goal_message = None
        self.sprites = pygame.sprite.Group()
        self.mediator = Mediator()
        self.ball = Ball(self, self.mediator, "ball.png")

        if self.team1_name == "braian":
            braianFactory = TeamBraianFactory("sprites/playerNico(Peruano).png", self.mediator, True, 5)
            self.team1 = braianFactory.createTeam()
        elif self.team2_name == "braian":
            braianFactory = TeamBraianFactory("sprites/playerNico(Peruano).png", self.mediator, False, 5)
            self.team2 = braianFactory.createTeam()
            
        if self.team1_name == "mateo":
            mateoFactory = TeamMateoFactory("sprites/playerNico(Peruano).png", self.mediator, True, 5)
            self.team1 = mateoFactory.createTeam()
        elif self.team2_name == "mateo":
            mateoFactory = TeamMateoFactory("sprites/playerNico(Peruano).png", self.mediator, False, 5)
            self.team2 = mateoFactory.createTeam()

        if self.team1_name == "gonzalo":
            gonzaloFactory = TeamGonzaloFactory("sprites/playerNico(Peruano).png", self.mediator, True, 5)
            self.team1 = gonzaloFactory.createTeam()
        elif self.team2_name == "gonzalo":
            gonzaloFactory = TeamGonzaloFactory("sprites/playerNico(Peruano).png", self.mediator, False, 5)
            self.team2 = gonzaloFactory.createTeam()

        if self.team1_name == "nicolas":
            nicolasFactory = TeamNicolasFactory("sprites/playerNico(Peruano).png", self.mediator, True, 5)
            self.team1 = nicolasFactory.createTeam()
        elif self.team2_name == "nicolas":
            nicolasFactory = TeamNicolasFactory("sprites/playerNico(Peruano).png", self.mediator, False, 5)
            self.team2 = nicolasFactory.createTeam()

        if self.team1_name == "tomas_r":
            tomasRFactory = TeamTomasRFactory("sprites/playerNico(Peruano).png", self.mediator, True, 5)
            self.team1 = tomasRFactory.createTeam()
        elif self.team2_name == "tomas_r":
            tomasRFactory = TeamTomasRFactory("sprites/playerNico(Peruano).png", self.mediator, False, 5)
            self.team2 = tomasRFactory.createTeam()

        if self.team1_name == "tomas_g":
            tomasGFactory = TeamTomasGFactory("sprites/playerNico(Peruano).png", self.mediator, True, 5)
            self.team1 = tomasGFactory.createTeam()
        elif self.team2_name == "tomas_g":
            tomasGFactory = TeamTomasGFactory("sprites/playerNico(Peruano).png", self.mediator, False, 5)
            self.team2 = tomasGFactory.createTeam()
        
        self.sprites.add(self.ball)
        self.mediator.setBall(self.ball)
        for player in self.team1:
            self.mediator.addPlayer1(player)
            self.sprites.add(player)
        for player in self.team2:
            self.mediator.addPlayer2(player)
            self.sprites.add(player)
        self.mediator.restart_positions(random.choice([True, False]))

    def play(self):
        pygame.init()
        screen = pygame.display.set_mode([WIDTH, HEIGHT])#, pygame.FULLSCREEN)
        clock = pygame.time.Clock()
        done = False
        background = pygame.image.load("estadio2.png").convert()
        pygame.display.set_caption("Fut_Game")
        icon = pygame.image.load("pelotaicon.png")
        pygame.display.set_icon(icon)
        while not done:
            done = self.process_events()
            self.run_logic()
            self.display_frame(screen, background)
            clock.tick(FPS)
        pygame.quit()

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