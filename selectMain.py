import pygame
from Constantes import *
from Game import Game
from boton import Boton
from cursor import Cursor

BRAIAN = "braian"
MATEO = "mateo"
GONZALO = "gonzalo"
NICOLAS = "nicolas"
TOMAS_R = "tomas_r"
TOMAS_G = "tomas_g"

# Dimensiones de cada botón
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 100

# Separación vertical entre botones
GAP_Y = 20

# Variables globales
team1_name = ""
team2_name = ""
count_press = 0

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
    # Calcular posiciones de los botones
    center_x = (WIDTH - BUTTON_WIDTH) // 2

    # Coordenadas para los botones
    button1_y = (HEIGHT - (2 * BUTTON_HEIGHT + GAP_Y)) // 2
    button2_y = button1_y + BUTTON_HEIGHT + GAP_Y
    button3_y = button2_y + BUTTON_HEIGHT + GAP_Y
    button4_y = button1_y
    button5_y = button2_y
    button6_y = button3_y

    # Crear los botones con las coordenadas calculadas
    botonMateo = Boton("Botones/botones normales/boton mateo (normal).jpg", "Botones/botones de seleccion/boton mateo (seleccion).jpg", center_x - BUTTON_WIDTH - GAP_Y, button1_y)
    botonBraian = Boton("Botones/botones normales/boton braian (normal).jpg", "Botones/botones de seleccion/boton braian (seleccion).jpg", center_x - BUTTON_WIDTH - GAP_Y, button2_y)
    botonNicolas = Boton("Botones/botones normales/boton nicolas (normal).jpg", "Botones/botones de seleccion/boton nicolas (seleccion).jpg", center_x - BUTTON_WIDTH - GAP_Y, button3_y)
    botonGonzalo = Boton("Botones/botones normales/boton gonzalo (normal).jpg", "Botones/botones de seleccion/boton gonzalo (seleccion).jpg", center_x + BUTTON_WIDTH + GAP_Y, button4_y)
    botonTomasR = Boton("Botones/botones normales/boton tomas r (normal).jpg", "Botones/botones de seleccion/boton tomas r (seleccion).jpg", center_x + BUTTON_WIDTH + GAP_Y, button5_y)
    botonTomasG = Boton("Botones/botones normales/boton tomas g (normal).jpg", "Botones/botones de seleccion/boton tomas g (seleccion).jpg", center_x + BUTTON_WIDTH + GAP_Y, button6_y)

    global count_press, team1_name, team2_name

    while not done:
        done = process_events(cursor, botonBraian, botonGonzalo, botonMateo, botonNicolas, botonTomasG, botonTomasR)
        if team1_name != "" and team2_name != "":
            game = Game(team1_name, team2_name)
            game.play()
        botones = [botonMateo, botonBraian, botonNicolas, botonTomasG, botonTomasR, botonGonzalo]
        display_frame(screen, background, cursor, botones)
        clock.tick(FPS)
    pygame.quit()

def set_team_names(name):
    global count_press, team1_name, team2_name
    count_press += 1
    if count_press == 1:
        team1_name = name
    else:
        team2_name = name

def process_events(cursor, botonBraian, botonGonzalo, botonMateo, botonNicolas, botonTomasG, botonTomasR):
    global count_press, team1_name, team2_name
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if cursor.colliderect(botonBraian.rect):
                set_team_names(BRAIAN)
            elif cursor.colliderect(botonGonzalo.rect):
                set_team_names(GONZALO)
            elif cursor.colliderect(botonMateo.rect):
                set_team_names(MATEO)
            elif cursor.colliderect(botonNicolas.rect):
                set_team_names(NICOLAS)
            elif cursor.colliderect(botonTomasR.rect):
                set_team_names(TOMAS_R)
            elif cursor.colliderect(botonTomasG.rect):
                set_team_names(TOMAS_G)
    return False

def display_frame(screen, background, cursor, botones):
    screen.blit(background, [0 , 0])
    cursor.update()
    for boton in botones:
        boton.update(screen, cursor)

    pygame.display.update()

if __name__ == "__main__":
    selectMain()
