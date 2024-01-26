
FPS = 30

# Dimensiones de pantalla
WIDTH = 1356
HEIGHT = 755

# Nombres de botones
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

# Acciones de Player
SHOT = 1
PASS = 2
MOVE = 3

# Limites de la cancha
LATERAL_IZQ = 48 # coord en y 
LATERAL_DER = 719 # coord en y
FONDO_DER = 1252 # coord en x 
FONDO_IZQ = 101 # coord en x
MITAD_CANCHA = 677 # coord en x
SAQUE = 383  # coord en y

PALO_SUP = 317 # coord en y
PALO_INF = 445 # coord en y
GROSOR_X_PALO_IZQ = (101, 103)
GROSOR_X_PALO_DER = (1250, 1252)
GROSOR_Y_PALO_INF = (443, 449)       
GROSOR_Y_PALO_SUP = (315, 321)

AREA_G_INF = 623 # coord en y
AREA_G_SUP = 144 # coord en y

AREA_G_MID_DER = 1029 # coord en x 
AREA_G_MID_IZQ = 324 # coord en x
AREA_C_INF = 527 # coord en y
AREA_C_SUP = 240 # coord en y 

AREA_C_MID_IZQ = 209 # coord en x 
AREA_C_MID_DER = 1144 # coord en x 

# Posiciones de jugadores 

POS_SAQUE = (MITAD_CANCHA, SAQUE)

# Equipo Lado Der
POS_P1_F5 = (773, SAQUE)
POS_P2_F5 = (MITAD_CANCHA+160, AREA_C_SUP)
POS_P3_F5 = (MITAD_CANCHA+277, SAQUE)
POS_P4_F5 = (MITAD_CANCHA+160, AREA_C_INF)
POS_P5_F5 = (FONDO_DER-10, SAQUE)
POS_TEAM2_F5 = [
    POS_P1_F5,
    POS_P2_F5,
    POS_P3_F5,
    POS_P4_F5,
    POS_P5_F5
                ]

# Equipo Lado Izq
POS_P6_F5 = (582, SAQUE)
POS_P7_F5 = (MITAD_CANCHA-160, AREA_C_SUP)
POS_P8_F5 = (MITAD_CANCHA-277, SAQUE)
POS_P9_F5 = (MITAD_CANCHA-160, AREA_C_INF)
POS_P10_F5 = (FONDO_IZQ+10, SAQUE)
POS_TEAM1_F5 = [
    POS_P6_F5,
    POS_P7_F5,
    POS_P8_F5,
    POS_P9_F5,
    POS_P10_F5
                ]