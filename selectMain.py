import pygame
from Constantes import *
import Game
from boton import Boton
from cursor import Cursor

def selectMain():

    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])#, pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    done = False
    background = pygame.image.load("Fondos de pantalla/menu de seleccion.jpg").convert()
    pygame.display.set_caption("Menu de seleccion")
    icon = pygame.image.load("pelotaicon.png")
    pygame.display.set_icon(icon)

    cursor = Cursor()
    botonMateo = Boton("Botones/botones normales/boton mateo (normal).jpg", "Botones/botones de seleccion/boton mateo (seleccion).jpg", 200, 100)
    botonBraian = Boton("Botones/botones normales/boton braian (normal).jpg", "Botones/botones de seleccion/boton braian (seleccion).jpg", 200, 100)
    botonNicolas = Boton("Botones/botones normales/boton nicolas (normal).jpg", "Botones/botones de seleccion/boton nicolas (seleccion).jpg", 200, 100)
    botonGonzalo = Boton("Botones/botones normales/boton gonzalo (normal).jpg", "Botones/botones de seleccion/boton gonzalo (seleccion).jpg", 200, 100)
    botonTomasR = Boton("Botones/botones normales/boton tomas r (normal).jpg", "Botones/botones de seleccion/boton tomas r (seleccion).jpg", 200, 100)
    botonTomasG = Boton("Botones/botones normales/boton tomas g (normal).jpg", "Botones/botones de seleccion/boton tomas g (seleccion).jpg", 200, 100)
    count_press = 0
    team1_name = ""
    team2_name = ""
    game = Game()

    while not done:
        done = process_events()
        if team1_name != "" and team2_name != "":
            game.setTeam1Name(team1_name)
            game.setTeam2Name(team2_name)
            game.play()
        display_frame(screen, background)
        clock.tick(FPS)
    pygame.quit()

    def process_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cursor.colliderect(botonBraian.rect):
                    count_press+=1
                    # selección equipo 1
                    if count_press == 1:
                        team1_name = "braian"
                    # selección equipo 2
                    else:
                        team2_name = "braian"
                elif cursor.colliderect(botonGonzalo.rect):
                    count_press+=1
                    # selección equipo 1
                    if count_press == 1:
                        team1_name = "gonzalo"
                    # selección equipo 2
                    else:
                        team2_name = "gonzalo"
                elif cursor.colliderect(botonMateo.rect):
                    count_press+=1
                    # selección equipo 1
                    if count_press == 1:
                        team1_name = "mateo"
                    # selección equipo 2
                    else:
                        team2_name = "mateo"
                elif cursor.colliderect(botonNicolas.rect):
                    count_press+=1
                    # selección equipo 1
                    if count_press == 1:
                        team1_name = "nicolas"
                    # selección equipo 2
                    else:
                        team2_name = "nicolas"
                elif cursor.colliderect(botonTomasR.rect):
                    count_press+=1
                    # selección equipo 1
                    if count_press == 1:
                        team1_name = "tomas_r"
                    # selección equipo 2
                    else:
                        team2_name = "tomas_r"
                elif cursor.colliderect(botonTomasG.rect):
                    count_press+=1
                    # selección equipo 1
                    if count_press == 1:
                        team1_name = "tomas_g"
                    # selección equipo 2
                    else:
                        team2_name = "tomas_g"
        return False

    def display_frame(screen, background):
        screen.blit(background, [0 , 0])
        cursor.update()
        botonBraian.update(screen, cursor)
        botonMateo.update(screen, cursor)
        botonGonzalo.update(screen, cursor)
        botonNicolas.update(screen, cursor)
        botonTomasG.update(screen, cursor)
        botonTomasR.update(screen, cursor)

        pygame.display.update()
        #pygame.display.flip()

if __name__ == "__selectMain__":
    selectMain()