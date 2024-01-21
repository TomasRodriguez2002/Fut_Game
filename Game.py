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
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])#, pygame.FULLSCREEN)
        self.background = pygame.image.load("Sprites/estadio.png").convert()
        self.team1_name = team1_name
        self.team2_name = team2_name
        self.goals_team1 = 0
        self.goals_team2 = 0
        self.sprite_player1 = ""
        self.sprite_player2 = ""
        self.half_time = False
        self.whistle = pygame.mixer.Sound("Sounds/whistle.wav")
        self.goal = pygame.mixer.Sound("Sounds/goal.wav")
        self.goal.set_volume(0.05)
        self.pause_sound = pygame.mixer.Sound("Sounds/pausa.wav")
        self.winner_sound = pygame.mixer.Sound("Sounds/winner.wav")
        self.winner_sound.set_volume(0.3)
        self.tie_sound = pygame.mixer.Sound("Sounds/empate.wav")
        self.environment = pygame.mixer.Sound("Sounds/ambiente.wav")
        self.environment.set_volume(0.1)
        self.canal1 = self.environment.play(-1)
        self.paused = False
        self.show_return_menu_message = False
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
            self.paused = False
            self.total_ticks = 0
            self.minutes = 0
            self.seconds = 0
            self.goals_team1 = 0
            self.goals_team2 = 0
            self.show_return_menu_message = False
        self.team1_created = False
        self.goal_message = None         
        self.current_goal_message = None
        self.sprites = pygame.sprite.Group()
        self.mediator = Mediator()
        self.ball = Ball(self, self.mediator, "Sprites/ball.png")

        if self.team1_name == "braian" and not self.team1_created:
            self.sprite_player1 = "Sprites/playerNico(Peruano).png"
            braianFactory = TeamBraianFactory(self.sprite_player1, self.mediator, True, 5)
            self.team1 = braianFactory.createTeam()
            self.team1_created = True
        if self.team2_name == "braian":
            self.sprite_player2 = "Sprites/playerNico(Peruano).png"
            braianFactory = TeamBraianFactory(self.sprite_player2, self.mediator, False, 5)
            self.team2 = braianFactory.createTeam()
            
        if self.team1_name == "mateo" and not self.team1_created:
            self.sprite_player1 = "Sprites/playerMateo.png"
            mateoFactory = TeamMateoFactory(self.sprite_player1, self.mediator, True, 5)
            self.team1 = mateoFactory.createTeam()
            self.team1_created = True
        if self.team2_name == "mateo":
            self.sprite_player2 = "Sprites/playerMateo.png"
            mateoFactory = TeamMateoFactory(self.sprite_player2, self.mediator, False, 5)
            self.team2 = mateoFactory.createTeam()

        if self.team1_name == "gonzalo" and not self.team1_created:
            self.sprite_player1 = "Sprites/playerNico(Peruano).png"
            gonzaloFactory = TeamGonzaloFactory(self.sprite_player1, self.mediator, True, 5)
            self.team1 = gonzaloFactory.createTeam()
            self.team1_created = True
        if self.team2_name == "gonzalo":
            self.sprite_player2 = "Sprites/playerNico(Peruano).png"
            gonzaloFactory = TeamGonzaloFactory(self.sprite_player2, self.mediator, False, 5)
            self.team2 = gonzaloFactory.createTeam()

        if self.team1_name == "nicolas" and not self.team1_created:
            self.sprite_player1 = "Sprites/playerNico.png"
            nicolasFactory = TeamNicolasFactory(self.sprite_player1, self.mediator, True, 5)
            self.team1 = nicolasFactory.createTeam()
            self.team1_created = True
        if self.team2_name == "nicolas":
            self.sprite_player2 = "Sprites/playerNico.png"
            nicolasFactory = TeamNicolasFactory(self.sprite_player2, self.mediator, False, 5)
            self.team2 = nicolasFactory.createTeam()

        if self.team1_name == "tomas_r" and not self.team1_created:
            self.sprite_player1 = "Sprites/tr.png"
            tomasRFactory = TeamTomasRFactory(self.sprite_player1, self.mediator, True, 5)
            self.team1 = tomasRFactory.createTeam()
            self.team1_created = True
        if self.team2_name == "tomas_r":
            self.sprite_player2 = "Sprites/tr.png"
            tomasRFactory = TeamTomasRFactory(self.sprite_player2, self.mediator, False, 5)
            self.team2 = tomasRFactory.createTeam()

        if self.team1_name == "tomas_g" and not self.team1_created:
            self.sprite_player1 = "Sprites/playerTomasG.png"
            tomasGFactory = TeamTomasGFactory(self.sprite_player1, self.mediator, True, 5)
            self.team1 = tomasGFactory.createTeam()
            self.team1_created = True
        if self.team2_name == "tomas_g":
            self.sprite_player2 = "Sprites/playerTomasG.png"
            tomasGFactory = TeamTomasGFactory(self.sprite_player2, self.mediator, False, 5)
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

    def pause(self):
        self.canal1.pause()
        self.pause_sound.play()
        self.paused = True
        self.display_frame()
        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.paused = False
                    pygame.quit()
                    return True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.pause_sound.play()
                        self.canal1.unpause()
                        self.paused = False
        return False
    
    def game_finish(self):
        self.canal1.pause()
        if self.goals_team1 != self.goals_team2:
            canal_winner_sound = self.winner_sound.play()
        else:
            canal_tie_sound = self.tie_sound.play()
        self.show_return_menu_message = True
        self.display_frame()
        finished_game = True
        while finished_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished_game = False
                    pygame.quit()
                    return True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        finished_game = False
                        if self.goals_team1 != self.goals_team2:
                            canal_winner_sound.pause()
                        else:
                            canal_tie_sound.pause()
        return True

    def play(self):
        pygame.init()
        clock = pygame.time.Clock()
        done = False
        pygame.display.set_caption("Fut_Game")
        icon = pygame.image.load("pelotaicon.png")
        pygame.display.set_icon(icon)
        while not done:
            done = self.process_events()
            if not done:
                done = self.run_logic()
                self.display_frame()
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
        aux1 = self.goals_team1
        self.goals_team1 = self.goals_team2
        self.goals_team2 = aux1
        self.initialize_game()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.canal1.pause()
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.canal1.pause()
                    return True
                if event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.reset_game()
                if event.key == pygame.K_SPACE:
                    return self.pause()
        return False

    def run_logic(self):
        self.sprites.update()
        if self.minutes == 1 and not self.half_time:
            self.resume_game()
        if self.minutes == 2:
            return self.game_finish()
        self.total_ticks += 1
        # Actualizar el tiempo cada segundo (30 ticks)
        if self.total_ticks % 30 == 0:
            self.seconds += 1
            if self.seconds == 60:
                self.minutes += 1
                self.seconds = 0
        return False

    def display_frame(self):
        self.screen.blit(self.background, [0 , 0])
        self.sprites.draw(self.screen)

        if self.current_goal_message:
            self.screen.blit(self.current_goal_message, ((WIDTH - self.current_goal_message.get_width()) // 2, HEIGHT // 2))
            # Reduzca el temporizador del mensaje de gol en cada iteración
            self.goal_message_timer -= 1
            if self.goal_message_timer <= 0:
                self.current_goal_message = None  # Borra el mensaje cuando el temporizador llega a cero
        
        # Mostrar el contador de tiempo en la parte superior al centro
        timer_text = f"{self.minutes:02d}:{self.seconds:02d}"
        timer_surface = font.render(timer_text, True, (255, 255, 255))
        # Ajustar el tamaño en y del contador de tiempo a 50
        timer_surface = pygame.transform.scale(timer_surface, (75, 45))
        timer_position = (MITAD_CANCHA-(timer_surface.get_width()//2), 0)

        if self.show_return_menu_message:     

            if self.goals_team1 > self.goals_team2:
                sprite_player_image = pygame.image.load(self.sprite_player1)
                sprite_player_image = pygame.transform.scale(sprite_player_image, (100, 100))
                sprite_player_position = (MITAD_CANCHA-((sprite_player_image.get_width()) // 2),SAQUE-((sprite_player_image.get_height())//2))
                self.screen.blit(sprite_player_image, sprite_player_position)

                show_winner_message = font.render("Ganador!", True, (255, 255, 255))
                show_winner_message = pygame.transform.scale(show_winner_message, (150, 40)) 
                show_winner_message_position = ((WIDTH - show_winner_message.get_width()) // 2, HEIGHT // 2 + 50)
                self.screen.blit(show_winner_message, show_winner_message_position)

                sprite_crown_image = pygame.image.load("Fondos de pantalla/corona.png")
                sprite_crown_image = pygame.transform.scale(sprite_crown_image, (80, 80))
                sprite_crown_position = (MITAD_CANCHA-((sprite_crown_image.get_width()) // 2),(SAQUE-((sprite_player_image.get_height())//2))-50)
                self.screen.blit(sprite_crown_image, sprite_crown_position)
                
            elif self.goals_team1 < self.goals_team2:
                sprite_player_image = pygame.image.load(self.sprite_player2)
                sprite_player_image = pygame.transform.scale(sprite_player_image, (100, 100))
                sprite_player_position = (MITAD_CANCHA-((sprite_player_image.get_width()) // 2),SAQUE-((sprite_player_image.get_height())//2))
                self.screen.blit(sprite_player_image, sprite_player_position)

                show_winner_message = font.render("Ganador!", True, (255, 255, 255))
                show_winner_message = pygame.transform.scale(show_winner_message, (150, 40)) 
                show_winner_message_position = ((WIDTH - show_winner_message.get_width()) // 2, HEIGHT // 2 + 50)
                self.screen.blit(show_winner_message, show_winner_message_position)

                sprite_crown_image = pygame.image.load("Fondos de pantalla/corona.png")
                sprite_crown_image = pygame.transform.scale(sprite_crown_image, (80, 80))
                sprite_crown_position = (MITAD_CANCHA-((sprite_crown_image.get_width()) // 2),(SAQUE-((sprite_player_image.get_height())//2))-50)
                self.screen.blit(sprite_crown_image, sprite_crown_position)

            else:
                show_tie_message = font.render("Empate", True, (255, 255, 255)) 
                show_tie_message = pygame.transform.scale(show_tie_message, (150, 40))                
                show_tie_message_position = ((WIDTH - show_tie_message.get_width()) // 2, HEIGHT // 2 + 50)
                self.screen.blit(show_tie_message, show_tie_message_position)

            escape_message = font.render("Presiona ESC para volver al menú", True, (255, 255, 255))
            escape_message = pygame.transform.scale(escape_message, (450, 40))  # Ajustar el tamaño
            escape_message_position = (MITAD_CANCHA-((escape_message.get_width()) // 2), AREA_G_INF-((escape_message.get_height())//2))
            self.screen.blit(escape_message, escape_message_position)
        
        if self.paused:
            pause_message = font.render("Pausa", True, (255, 255, 255))
            #pause_message_position = ((WIDTH - pause_message.get_width()) // 2, HEIGHT // 2)
            pause_message_position = (MITAD_CANCHA-((pause_message.get_width()) // 2), SAQUE-((pause_message.get_height()) // 2))
            self.screen.blit(pause_message, pause_message_position)
        
        self.screen.blit(timer_surface, timer_position)

        # Mostrar contadores de goles del team 1
        goals_text_team1 = f"{self.goals_team1}"
        goals_team1_surface = font.render(goals_text_team1, True, (255, 255, 255))
        goals_team1_position = (550, 0)
        # Ajustar el tamaño en y del contador de goles a 50
        goals_team1_surface = pygame.transform.scale(goals_team1_surface, (45, 45))

        # Mostrar contadores de goles del team 2
        goals_text_team2 = f"{self.goals_team2}"
        goals_team2_surface = font.render(goals_text_team2, True, (255, 255, 255))
        goals_team2_position = (750, 0)
        # Ajustar el tamaño en y del contador de goles a 50
        goals_team2_surface = pygame.transform.scale(goals_team2_surface, (45, 45))

        # Mostrar sprite_player1 a la izquierda del contador de goles del team 1
        sprite_player1_image = pygame.image.load(self.sprite_player1)
        sprite_player1_image = pygame.transform.scale(sprite_player1_image, (45, 45))
        sprite_player1_position = (goals_team1_position[0] - 60, 0)

        # Mostrar sprite_player2 a la derecha del contador de goles del team 2
        sprite_player2_image = pygame.image.load(self.sprite_player2)
        sprite_player2_image = pygame.transform.scale(sprite_player2_image, (45, 45))
        sprite_player2_position = (goals_team2_position[0] + 60, 0)

        self.screen.blit(sprite_player1_image, sprite_player1_position)
        self.screen.blit(goals_team1_surface, goals_team1_position)
        self.screen.blit(goals_team2_surface, goals_team2_position)
        self.screen.blit(sprite_player2_image, sprite_player2_position)

        pygame.display.flip()

    def show_goal_message(self, message, duration):
            self.goal_message_timer = duration
            self.current_goal_message = font.render(message, True, (255, 255, 255))  # Color blanco