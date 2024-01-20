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
        self.goals_team1 = 0
        self.goals_team2 = 0
        self.half_time = False
        self.whistle = pygame.mixer.Sound("Sounds/whistle.wav")
        self.goal = pygame.mixer.Sound("Sounds/goal.wav")
        self.goal.set_volume(0.05)
        self.environment = pygame.mixer.Sound("Sounds/ambiente.wav")
        self.environment.set_volume(0.1)
        self.environment.play(-1)
        self.initialize_game()

    def initialize_game(self):
        self.team2 = None
        self.team1 = None
        self.ball = None
        self.mediator = None
        self.goal_message = None
        self.current_goal_message = None
        self.sprites = pygame.sprite.Group()
        if not self.half_time:
            self.total_ticks = 0
            self.minutes = 0
            self.seconds = 0
            self.goals_team1 = 0
            self.goals_team2 = 0
        self.team1_created = False
        self.goal_message = None         
        self.current_goal_message = None
        self.sprites = pygame.sprite.Group()
        self.mediator = Mediator()
        self.ball = Ball(self, self.mediator, "ball.png")

        if self.team1_name == "braian" and not self.team1_created:
            braianFactory = TeamBraianFactory("sprites/playerNico(Peruano).png", self.mediator, True, 5)
            self.team1 = braianFactory.createTeam()
            self.team1_created = True
        if self.team2_name == "braian":
            braianFactory = TeamBraianFactory("sprites/playerNico(Peruano).png", self.mediator, False, 5)
            self.team2 = braianFactory.createTeam()
            
        if self.team1_name == "mateo" and not self.team1_created:
            mateoFactory = TeamMateoFactory("sprites/playerNico(Peruano).png", self.mediator, True, 5)
            self.team1 = mateoFactory.createTeam()
            self.team1_created = True
        if self.team2_name == "mateo":
            mateoFactory = TeamMateoFactory("sprites/playerNico(Peruano).png", self.mediator, False, 5)
            self.team2 = mateoFactory.createTeam()

        if self.team1_name == "gonzalo" and not self.team1_created:
            gonzaloFactory = TeamGonzaloFactory("sprites/playerNico(Peruano).png", self.mediator, True, 5)
            self.team1 = gonzaloFactory.createTeam()
            self.team1_created = True
        if self.team2_name == "gonzalo":
            gonzaloFactory = TeamGonzaloFactory("sprites/playerNico(Peruano).png", self.mediator, False, 5)
            self.team2 = gonzaloFactory.createTeam()

        if self.team1_name == "nicolas" and not self.team1_created:
            nicolasFactory = TeamNicolasFactory("sprites/playerNico(Peruano).png", self.mediator, True, 5)
            self.team1 = nicolasFactory.createTeam()
            self.team1_created = True
        if self.team2_name == "nicolas":
            nicolasFactory = TeamNicolasFactory("sprites/playerNico(Peruano).png", self.mediator, False, 5)
            self.team2 = nicolasFactory.createTeam()

        if self.team1_name == "tomas_r" and not self.team1_created:
            tomasRFactory = TeamTomasRFactory("player.png", self.mediator, True, 5)
            self.team1 = tomasRFactory.createTeam()
            self.team1_created = True
        if self.team2_name == "tomas_r":
            tomasRFactory = TeamTomasRFactory("player.png", self.mediator, False, 5)
            self.team2 = tomasRFactory.createTeam()

        if self.team1_name == "tomas_g" and not self.team1_created:
            tomasGFactory = TeamTomasGFactory("sprites/playerNico(Peruano).png", self.mediator, True, 5)
            self.team1 = tomasGFactory.createTeam()
            self.team1_created = True
        if self.team2_name == "tomas_g":
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
        return

    def reset_game(self):
        self.sprites.empty() 
        self.half_time = False 
        self.initialize_game()

    def resume_game(self):
        self.half_time = True
        self.sprites.empty()
        aux = self.team1_name
        self.team1_name = self.team2_name
        self.team2_name = aux
        self.initialize_game()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.pause()
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.pause()
                    return True
                # Verificar si se presionó Ctrl+R para resetear el juego
                if event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.reset_game()
        return False

    def run_logic(self):
        self.sprites.update()
        if self.seconds == 10 and not self.half_time:
            self.resume_game()
        if self.seconds == 20:
            pass
        self.total_ticks += 1
        # Actualizar el tiempo cada segundo (30 ticks)
        if self.total_ticks % 30 == 0:
            self.seconds += 1
            if self.seconds == 60:
                self.minutes += 1
                self.seconds = 0

    def display_frame(self, screen, background):
        screen.blit(background, [0 , 0])
        self.sprites.draw(screen)
        if self.current_goal_message:
            screen.blit(self.current_goal_message, ((WIDTH - self.current_goal_message.get_width()) // 2, HEIGHT // 2))
            # Reduzca el temporizador del mensaje de gol en cada iteración
            self.goal_message_timer -= 1
            if self.goal_message_timer <= 0:
                self.current_goal_message = None  # Borra el mensaje cuando el temporizador llega a cero
            
        # Mostrar el contador de tiempo en la parte superior al centro
        timer_text = f"{self.minutes:02d}:{self.seconds:02d}"
        timer_surface = font.render(timer_text, True, (255, 255, 255))
        # Ajustar el tamaño en y del contador de tiempo a 50
        timer_surface = pygame.transform.scale(timer_surface, (75, 45))
        timer_position = (MITAD_CANCHA-(timer_surface.get_width()//2), 5)
        
        screen.blit(timer_surface, timer_position)

        # Mostrar contadores de goles
        goals_text = f"{self.goals_team1} - {self.goals_team2}"
        goals_surface = font.render(goals_text, True, (255, 255, 255))
        goals_position = (650, 5)
        
        # Ajustar el tamaño en y del contador de goles a 50
        goals_surface = pygame.transform.scale(goals_surface, (75, 45))
        
        screen.blit(goals_surface, goals_position)

        pygame.display.flip()


    def show_goal_message(self, message, duration):
            self.goal_message_timer = duration
            self.current_goal_message = font.render(message, True, (255, 255, 255))  # Color blanco