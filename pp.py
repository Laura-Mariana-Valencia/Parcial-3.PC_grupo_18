from collections import defaultdict
import random
from tkinter import font
import pygame

# Inicializar Pygame
pygame.init()

# Cargar imagen del tablero
tablero_img = pygame.image.load("parques.png")
width, height = tablero_img.get_size()

# Establecer el tamaño deseado (por ejemplo, un 50% del tamaño original)
scaled_width = int(width * 0.7)  # 50% del ancho original
scaled_height = int(height * 0.7)  # 50% de la altura original

# Escalar la imagen a un tamaño más pequeño
tablero_img = pygame.transform.scale(tablero_img, (scaled_width, scaled_height))

# Mostrar la imagen redimensionada
screen = pygame.display.set_mode((scaled_width, scaled_height))
screen.blit(tablero_img, (0, 0))
pygame.display.flip()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 182, 193)
BLUE = (173, 216, 230)
GREEN = (144, 238, 144)
YELLOW = (255, 255, 153)

# Fuente para los números de los dados
pygame.font.init()
font = pygame.font.Font(None, 200)
# Reloj para controlar FPS
clock = pygame.time.Clock()

# Posiciones de las casillas (simplificadas)
path_positions = {0: (24, 85), 1: (86, 23), 2: (98, 159), 3: (160, 99), #cárcel azul
                  4: (446, 99), 5: (521, 23), 6: (582, 86), 7: (506, 157), #cárcel verde
                  8: (100, 445), 9: (26, 519), 10: (86, 577), 11: (160, 507), #cárcel amarillo
                  12: (444, 505), 13: (504, 445), 14: (519, 577), 15: (579, 519), #cárcel rojo
                  16: (283, 590), 17: (363, 592), 18: (363, 568), 19: (363, 544), 20: (361, 517), 21: (359, 493), 
                  22: (356, 467), 23: (366, 431), 24: (385, 403), 25: (408, 382), 26: (435, 371), 27: (465, 364), 
                  28: (492, 363), 29: (519, 365), 30: (540, 366), 31: (567, 364), 32: (590, 364), #Rojo 1 al 17 (primero seguro)
                  33: (593, 316), 34: (589, 245), 35: (567, 244), 36: (543, 245), 37: (518, 246), 38: (494, 241), 
                  39: (467, 244), 40: (436, 236), 41: (409, 219), 42: (385, 196), 43: (371, 166), 44: (359, 138), 
                  45: (367, 110), 46: (367, 88), 47: (367, 63), 48: (368, 38), 49: (363, 10), #Verde 18 al 34 (primero seguro)
                  50: (302, 11), 51: (223, 10), 52: (223, 36), 53: (222, 65), 54: (214, 86), 55: (215, 112), 
                  56: (226, 136), 57: (219, 162), 58: (203, 186), 59: (183, 199), 60: (160, 212), 61:(137, 217), 
                  62: (113, 214), 63: (87, 214), 64: (61, 215), 65: (37, 215), 66: (10, 216), #Azul 35 al 51 (primero seguro)
                  67: (13, 304), 68: (10, 378), 69: (37, 379), 70: (63, 380), 71: (87, 378), 72: (111, 376), 73: (135, 376), 
                  74: (165, 383), 75: (188, 396), 76: (207, 418), 77: (224, 440), 78: (234, 467), 79: (225, 492), 80: (226, 515), 
                  81: (222, 541), 82: (222, 568), 83: (221, 591),#Amarillo 52 al 68 (primero seguro)
                  84: (296, 567), 85: (298, 545), 86: (299, 517), 87: (299, 493), 88: (301, 468), 89: (299, 443), 90: (300, 416),#Camino llegada rojo
                  91: (568, 301), 92: (540, 301), 93: (517, 298), 94: (491, 297), 95: (467, 297), 96: (442, 297), 97: (417, 297),#Camino llegada verde
                  98: (302, 37), 99: (301, 63), 100: (302, 86), 101: (303, 112), 102: (303, 137), 103: (304, 161), 104: (304, 187),#Camino llegada azul
                  105: (37, 302), 106: (63, 301), 107: (89, 301), 108: (111, 301), 109: (137, 301), 110: (162, 300), 111: (188, 299),#Camino llegada amarillo 
                  112: (230, 299), #llegada amarillo
                  113: (300, 234), #llegada azul
                  114: (368, 295), #llegada verde
                  115: (303, 371),} #llegada rojo
#Variables
dado1, dado2 = 1, 1  # Valores iniciales de los dados

# Diccionario para almacenar las fichas de cada color
fichas = {
    "rojo": [path_positions[i] for i in range(12, 16)],
    "verde": [path_positions[i] for i in range(4, 8)],
    "azul": [path_positions[i] for i in range(0, 4)],
    "amarillo": [path_positions[i] for i in range(8, 12)],
}

caminos = {"rojo": [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 
                    42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 
                    63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 
                    16, 84, 85, 86, 87, 88, 89, 90, 115],  
           "verde": [38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 
                     59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 
                     80, 81, 82, 83, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 
                     91, 92, 93, 94, 95, 96, 97, 114],
           "azul": [55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 
                    76, 77, 78, 79, 80, 81, 82, 83, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 
                    29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 
                    50, 98, 99, 100, 101, 102, 103, 104, 113],
           
           "amarillo": [72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 16, 17, 18, 19, 20, 21, 22, 23, 24, 
                        25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 
                        46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 
                        67, 105, 106, 107, 108, 109, 110, 111, 112]}

carceles = {
    "rojo": [path_positions[i] for i in range(12, 16)],    
    "verde": [path_positions[i] for i in range(4, 8)],
    "azul": [path_positions[i] for i in range(0, 4)],
    "amarillo": [path_positions[i] for i in range(8, 12)],

}

salidas = {
    "rojo": path_positions[21],
    "verde": path_positions[38],
    "azul": path_positions[55],    
    "amarillo": path_positions[72]    
}

llegadas = {
    "rojo": path_positions[115],
    "verde": path_positions[114],
    "azul": path_positions[113],    
    "amarillo": path_positions[112]    
}
seguros = {
    "azul": [path_positions[50], path_positions[62]],
    "verde": [path_positions[33], path_positions[45]],
    "amarillo": [path_positions[67], path_positions[79]],
    "rojo": [path_positions[16], path_positions[28]]
}

jugadores = ["rojo", "verde", "azul", "amarillo"]
turno = 0
color = jugadores[turno]
pares_consecutivos = 0

# Diccionario de colores para las fichas
colores_fichas = {
    "rojo": RED,
    "verde": GREEN,
    "azul": BLUE,
    "amarillo": YELLOW
}

# Función para mostrar texto en la pantalla
def mostrar_texto(texto, x, y, tamaño=36, color=BLACK):
    fuente = pygame.font.Font(None, tamaño)
    texto_surface = fuente.render(texto, True, color)
    screen.blit(texto_surface, (x, y))

# Función del menú inicial
def menu_inicial():
    screen.fill(WHITE)
    mostrar_texto("Presiona 'N' para Modo Normal", 100, 200, tamaño=50, color=BLACK)
    mostrar_texto("Presiona 'D' para Modo Desarrollador", 100, 300, tamaño=50, color=BLACK)
    pygame.display.flip()

    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    return False  # Modo normal
                elif event.key == pygame.K_d:
                    return True  # Modo desarrollador

# Llamar al menú inicial antes del bucle principal
modo_desarrollador = menu_inicial()

# Función para ingresar valores manualmente en modo desarrollador
def ingresar_valores_manuales():
    screen.fill(WHITE)
    mostrar_texto("Ingresa el valor del primer dado (1-6):", 100, 200, tamaño=40, color=BLACK)
    pygame.display.flip()

    dado1 = None
    while dado1 is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode.isdigit() and 1 <= int(event.unicode) <= 6:
                    dado1 = int(event.unicode)
                    break

    screen.fill(WHITE)
    mostrar_texto("Ingresa el valor del segundo dado (1-6):", 100, 200, tamaño=40, color=BLACK)
    pygame.display.flip()

    dado2 = None
    while dado2 is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode.isdigit() and 1 <= int(event.unicode) <= 6:
                    dado2 = int(event.unicode)
                    break

    return dado1, dado2

def dibujar_fichas():
    posiciones_ocupadas = {}

    for color, fichas_color in fichas.items():
        for ficha_index, pos_index in enumerate(fichas_color):
            if isinstance(pos_index, tuple):
                pos = pos_index
            elif isinstance(pos_index, int) and pos_index in path_positions:
                pos = path_positions[pos_index]
            else:
                continue

            if pos not in posiciones_ocupadas:
                posiciones_ocupadas[pos] = []
            posiciones_ocupadas[pos].append((color, ficha_index))

    for pos, fichas_en_casilla in posiciones_ocupadas.items():
        num_fichas = len(fichas_en_casilla)
        offsets = [(0, 0)]

        if num_fichas == 2:
            offsets = [(-10, 0), (10, 0)]
        elif num_fichas == 3:
            offsets = [(-10, -10), (10, -10), (0, 10)]
        elif num_fichas >= 4:
            offsets = [(-10, -10), (10, -10), (-10, 10), (10, 10)]

        for i, (color, ficha_index) in enumerate(fichas_en_casilla):
            radio = 18  
            offset_x, offset_y = offsets[i % len(offsets)]
            pos_desplazada = (pos[0] + offset_x, pos[1] + offset_y)

            pygame.draw.circle(screen, colores_fichas[color], pos_desplazada, radio)
            font = pygame.font.Font(None, 28)
            text_surface = font.render(str(ficha_index + 1), True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=pos_desplazada)
            screen.blit(text_surface, text_rect)

# Función para lanzar los dados
def lanzar_dados():
    return random.randint(1, 6), random.randint(1, 6)

# Función para mover una ficha
movimientos_adicionales = 0  # Contador de movimientos adicionales

def mover_ficha(color, ficha_index, pasos):
    if ficha_index < len(fichas[color]):
        pos_actual = fichas[color][ficha_index]

        # Si la ficha está en la cárcel, no se mueve
        if pos_actual in carceles[color]:
            return

        # Si la ficha está en la salida, se mueve al primer paso del camino
        if pos_actual == salidas[color]:
            fichas[color][ficha_index] = caminos[color][0]
            nueva_pos = caminos[color][0]
        else:
            # Si la ficha está en el camino, se mueve según los pasos
            if pos_actual in caminos[color]:
                indice_camino = caminos[color].index(pos_actual)
                nuevo_indice = indice_camino + pasos

                # Verificar si el nuevo índice está dentro del rango del camino
                if nuevo_indice < len(caminos[color]):
                    nueva_pos = caminos[color][nuevo_indice]

                    # Verificar si hay un bloqueo en la casilla de destino
                    if verificar_bloqueo_en_casilla(nueva_pos):
                        print(f"¡Hay un bloqueo en la casilla {nueva_pos}! Movimiento limitado a {pasos - 1} pasos.")
                        nuevo_indice = indice_camino + (pasos - 1)  # Limitar el movimiento a n-1 pasos
                        nueva_pos = caminos[color][nuevo_indice] if nuevo_indice < len(caminos[color]) else pos_actual

                    # Mover la ficha a la nueva posición
                    fichas[color][ficha_index] = nueva_pos

                    # Verificar si hay un bloqueo o captura en la nueva posición
                    bloqueo_o_captura = verificar_bloqueo_y_captura(color, nueva_pos)
                    if bloqueo_o_captura:
                        print(bloqueo_o_captura)
                else:
                    print(f"No puedes mover la ficha {ficha_index + 1} de {color} porque excede el rango del camino.")
            else:
                print(f"La ficha {ficha_index + 1} de {color} no está en una posición válida.")
#Regla 1 - Sacar fichas de carcel cuando sale 1
def sacar_ficha_de_carcel(color):
    # Verificar si ya hay dos fichas en la salida
    fichas_en_salida = 0
    for pos in fichas[color]:
        if pos == salidas[color]:
            fichas_en_salida += 1
            if fichas_en_salida >= 2:
                print(f"No se puede sacar una ficha de la cárcel porque ya hay dos fichas en la salida de {color}.")
                return False  # No se puede sacar una ficha de la cárcel

    # Si no hay dos fichas en la salida, proceder a sacar una ficha de la cárcel
    for i, pos in enumerate(fichas[color]):
        if pos in carceles[color]:  # Verificar si la ficha está en la cárcel
            # Sacar la ficha de la cárcel y moverla a la salida
            fichas[color][i] = salidas[color]
            print(f"¡Ficha {i + 1} de {color} ha salido de la cárcel!")

            # Verificar si hay una ficha de otro equipo en la salida
            for equipo_enemigo, fichas_enemigas in fichas.items():
                if equipo_enemigo != color:  # Solo verificar fichas de otros equipos
                    for ficha_index, pos_ficha in enumerate(fichas_enemigas):
                        if pos_ficha == salidas[color]:  # Si hay una ficha enemiga en la salida
                            # Capturar la ficha enemiga y enviarla a su cárcel
                            fichas[equipo_enemigo][ficha_index] = carceles[equipo_enemigo][0]
                            print(f"¡Ficha {ficha_index + 1} de {equipo_enemigo} ha sido capturada y enviada a la cárcel!")
                            break  # Solo capturar una ficha

            return True  # Se sacó una ficha de la cárcel

    return False  # No había fichas en la cárcel

#Regla 2 - capturas en salida
def verificar_captura(color, ficha_index):
    pos_actual = fichas[color][ficha_index]

    # Verificar si la ficha está en una salida o en un seguro
    if pos_actual == salidas[color] or pos_actual in carceles[color]:
        return False  # No se puede capturar

    # Verificar si la ficha está en la salida de un equipo enemigo
    for equipo_enemigo, salida_enemiga in salidas.items():
        if equipo_enemigo != color and pos_actual == salida_enemiga:
            # Verificar si hay una ficha del equipo enemigo en la misma posición
            for ficha_enemiga_index, pos_ficha_enemiga in enumerate(fichas[equipo_enemigo]):
                if pos_ficha_enemiga == pos_actual:
                    return True  # Se puede capturar

    return False  # No se puede capturar

movimientos_adicionales = 0  # Contador de movimientos adicionales

def capturar_ficha(color, ficha_index):
    global movimientos_adicionales

    # Devolver la ficha a la cárcel
    fichas[color][ficha_index] = carceles[color][0]
    print(f"¡Ficha {ficha_index + 1} de {color} ha sido capturada y devuelta a la cárcel!")

    # Activar 20 movimientos adicionales
    movimientos_adicionales = 20
    print(f"¡{color} ha ganado 20 movimientos adicionales!")

def manejar_fichas_en_salida(color):
    # Verificar si hay dos fichas en la salida
    fichas_en_salida = []
    for ficha_index, pos in enumerate(fichas[color]):
        if pos == salidas[color]:
            fichas_en_salida.append((color, ficha_index))

    if len(fichas_en_salida) == 2:
        # Verificar si hay una ficha enemiga en la salida
        for equipo_enemigo, salida_enemiga in salidas.items():
            if equipo_enemigo != color:
                for ficha_enemiga_index, pos_ficha_enemiga in enumerate(fichas[equipo_enemigo]):
                    if pos_ficha_enemiga == salidas[color]:
                        # Capturar la ficha enemiga
                        capturar_ficha(equipo_enemigo, ficha_enemiga_index)
                        return

        # Si no hay fichas enemigas, entonces hay un bloqueo
        print(f"¡Hay un bloqueo en la salida de {color}! No se pueden mover fichas hasta que una de ellas se mueva.")

#Regla 3 - Bloqueos y capturas
def verificar_bloqueo_y_captura(color, nueva_pos):
    # Verificar si hay otras fichas en la nueva posición
    fichas_en_casilla = []
    for equipo, fichas_equipo in fichas.items():
        for ficha_index, pos in enumerate(fichas_equipo):
            if pos == nueva_pos:
                fichas_en_casilla.append((equipo, ficha_index))

    # Si hay más de una ficha en la casilla
    if len(fichas_en_casilla) > 1:
        equipo1, ficha_index1 = fichas_en_casilla[0]
        equipo2, ficha_index2 = fichas_en_casilla[1]

        # a) Son del mismo color/equipo, forman un bloqueo
        if equipo1 == equipo2:
            print(f"¡Fichas del equipo {equipo1} forman un bloqueo en la casilla {nueva_pos}!")
            return "Forma un bloqueo con tus propias fichas."

        # b) Son de diferente color/equipo pero están en un seguro o en una salida
        if nueva_pos in carceles[equipo1] or nueva_pos == salidas[equipo1] or nueva_pos in carceles[equipo2] or nueva_pos == salidas[equipo2]:
            print(f"¡Fichas de {equipo1} y {equipo2} forman un bloqueo en una casilla especial!")
            return "Forma un bloqueo en una casilla especial."

        # c) Son de diferente equipo y no están en una casilla especial
        # Capturar la ficha del equipo contrario
        if equipo1 == color:
            capturar_ficha(equipo2, ficha_index2)
            return f"Capturaste una ficha de {equipo2} y la enviaste a la cárcel."
        else:
            capturar_ficha(equipo1, ficha_index1)
            return f"Capturaste una ficha de {equipo1} y la enviaste a la cárcel."

    return ""  # No hay bloqueo ni captura
#Regla 4 - Bloqueo si hay 2 fichas en la siguiente casilla
def verificar_bloqueo_en_casilla(casilla):
    fichas_en_casilla = 0
    for equipo, fichas_equipo in fichas.items():
        for pos in fichas_equipo:
            if pos == casilla:
                fichas_en_casilla += 1
                if fichas_en_casilla > 1:
                    return True  # Hay un bloqueo
    return False  # No hay bloqueo

#Regla 5 - verificar que los movimientos sean exactos para llegar a la meta
def verificar_movimiento_llegada(color, nuevo_indice, pasos):
    
    # Obtener la posición de llegada para el color actual
    llegada = None
    if color == "rojo":
        llegada = path_positions[115]  # Llegada rojo
    elif color == "verde":
        llegada = path_positions[114]  # Llegada verde
    elif color == "azul":
        llegada = path_positions[113]  # Llegada azul
    elif color == "amarillo":
        llegada = path_positions[112]  # Llegada amarillo

    # Verificar si la nueva posición es la casilla de llegada
    if caminos[color][nuevo_indice] == llegada:
        # Verificar si el número de pasos es exacto
        if pasos == (len(caminos[color]) - 1 - caminos[color].index(caminos[color][nuevo_indice - pasos])):
            return True  # Movimiento válido
        else:
            return False  # No es un movimiento exacto
    return True  # No es una casilla de llegada, movimiento válido

#Regla 6 - Verificar si se pueden mover las fichas
def convertir_tupla_a_indice(pos, color):
    for i, camino_pos in enumerate(caminos[color]):
        if camino_pos == pos:
            return i
    return -1  # Si no se encuentra la posición, devolver -1 (caso de error)

def hay_movimientos_posibles(color, dado1, dado2):
    # Verificar si hay fichas en la cárcel y si se puede sacar con un 5
    if dado1 == 5 or dado2 == 5 or dado1 + dado2:
        for pos in fichas[color]:
            if pos in carceles[color]:
                return True  # Se puede sacar una ficha de la cárcel

    # Verificar movimientos para fichas que no están en la cárcel
    for ficha_index, pos in enumerate(fichas[color]):
        if pos not in carceles[color]:  # Ignorar fichas en la cárcel
            # Convertir pos a un índice si es una tupla
            if isinstance(pos, tuple):
                pos_index = convertir_tupla_a_indice(pos, color)
            else:
                pos_index = pos  # Si ya es un índice, úsalo directamente

            # Calcular la nueva posición
            nueva_pos_index = (pos_index + (dado1 + dado2)) % len(caminos[color])
            nueva_pos = caminos[color][nueva_pos_index]  # Obtener la posición real (tupla o índice)

            # Verificar si la nueva posición es válida (no hay bloqueo, no está en una casilla especial, etc.)
            if not verificar_bloqueo_en_casilla(nueva_pos) and verificar_movimiento_llegada(color, nueva_pos_index, dado1 + dado2):
                return True  # Hay al menos un movimiento posible

    return False  # No hay movimientos posibles

#Regla 7 - 20 movimientos adicionales por captura
def manejar_movimientos_adicionales(color):
    global movimientos_adicionales

    if movimientos_adicionales > 0:
        print(f"Movimientos adicionales restantes: {movimientos_adicionales}")
        movimientos_adicionales -= 1

        # Permitir al jugador seleccionar una ficha para mover
        fichas_disponibles = mostrar_fichas_disponibles(color)
        if fichas_disponibles:
            ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
            if ficha_seleccionada is not None:
                # Mover la ficha seleccionada (aquí puedes usar un valor fijo o lanzar un dado)
                pasos = 1  # Por ejemplo, mover 1 paso en cada movimiento adicional
                mover_ficha(color, ficha_seleccionada, pasos)
                return True  # Se realizó un movimiento adicional

    return False  # No se realizó un movimiento adicional

#Regla 8 - 10 movimientos adicionales
def activar_movimientos_adicionales(color, cantidad):
    """
    Activa movimientos adicionales para el equipo especificado.
    """
    global movimientos_adicionales
    movimientos_adicionales = cantidad
    print(f"¡{color} ha ganado {cantidad} movimientos adicionales!")

#Regla 9 - los 10 o 20 movimientos se deben hacer primero
def manejar_movimientos_adicionales(color):
    global movimientos_adicionales

    if movimientos_adicionales > 0:
        print(f"Movimientos adicionales restantes: {movimientos_adicionales}")
        movimientos_adicionales -= 1

        # Permitir al jugador seleccionar una ficha para mover
        fichas_disponibles = mostrar_fichas_disponibles(color)
        if fichas_disponibles:
            ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
            if ficha_seleccionada is not None:
                # Mover la ficha seleccionada (aquí puedes usar un valor fijo o lanzar un dado)
                pasos = 1  # Por ejemplo, mover 1 paso en cada movimiento adicional
                mover_ficha(color, ficha_seleccionada, pasos)
                return True  # Se realizó un movimiento adicional
    return False  # No se realizó un movimiento adicional

#Regla 10 -si el lanzamiento de los dados es igual el tiro se repite
def verificar_dados_iguales(dado1, dado2):
    return dado1 == dado2

#Regla 11 - Si salen 3 pares la última ficha va a la carcel
def manejar_tres_pares_consecutivos(color):
    global pares_consecutivos, ultima_ficha_movida
    if pares_consecutivos == 3:
        print(f"¡Tres pares consecutivos! La última ficha movida de {color} regresa a la cárcel.")
        if ultima_ficha_movida:
            color_ficha, ficha_index = ultima_ficha_movida
            fichas[color_ficha][ficha_index] = carceles[color_ficha][0]  # Devolver a la cárcel
        pares_consecutivos = 0  # Reiniciar el contador

def mostrar_fichas_disponibles(color):
    fichas_disponibles = []
    for i, pos in enumerate(fichas[color]):
        if pos not in carceles[color]:
            fichas_disponibles.append(i)
    return fichas_disponibles

def seleccionar_ficha(color, fichas_disponibles):
    screen.fill(WHITE)
    mostrar_texto(f"Turno del jugador {color}", 100, 100, tamaño=40, color=BLACK)
    mostrar_texto("Selecciona una ficha para mover:", 100, 150, tamaño=40, color=BLACK)
    
    for i, ficha_index in enumerate(fichas_disponibles):
        mostrar_texto(f"{i + 1}. Ficha {ficha_index + 1}", 100, 200 + i * 50, tamaño=40, color=BLACK)
    
    pygame.display.flip()

    esperando_seleccion = True
    while esperando_seleccion:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode.isdigit():
                    seleccion = int(event.unicode) - 1
                    if 0 <= seleccion < len(fichas_disponibles):
                        return fichas_disponibles[seleccion]
    return None

# Inicializar valores
dado1, dado2 = lanzar_dados()
mostrar_dados = True  # Solo mostrar los dados cuando se presiona espacio

# Bucle principal
running = True
while running:
    screen.blit(tablero_img, (0, 0))  # Limpiar la pantalla

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Regla 9: Movimientos adicionales tienen prioridad
            if movimientos_adicionales > 0:
                print(f"Movimientos adicionales restantes: {movimientos_adicionales}")
                movimientos_adicionales -= 1

                # Permitir al jugador seleccionar una ficha para mover
                fichas_disponibles = mostrar_fichas_disponibles(color)
                if fichas_disponibles:
                    ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
                    if ficha_seleccionada is not None:
                        # Mover la ficha seleccionada (aquí puedes usar un valor fijo o lanzar un dado)
                        pasos = 1  # Por ejemplo, mover 1 paso en cada movimiento adicional
                        mover_ficha(color, ficha_seleccionada, pasos)

            # Lanzar los dados
            if modo_desarrollador:
                # Preguntar si desea lanzar los dados o ingresar manualmente
                screen.fill(WHITE)
                mostrar_texto("Presiona 'L' para lanzar dados", 100, 200, tamaño=40, color=BLACK)
                mostrar_texto("Presiona 'M' para ingresar valores manualmente", 100, 300, tamaño=40, color=BLACK)
                pygame.display.flip()

                esperando_eleccion = True
                while esperando_eleccion:
                    for sub_event in pygame.event.get():
                        if sub_event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        if sub_event.type == pygame.KEYDOWN:
                            if sub_event.key == pygame.K_l:  # Lanzar dados
                                dado1, dado2 = lanzar_dados()
                                esperando_eleccion = False
                            elif sub_event.key == pygame.K_m:  # Ingresar manualmente
                                dado1, dado2 = ingresar_valores_manuales()
                                esperando_eleccion = False
            else:
                dado1, dado2 = lanzar_dados()  # Lanzar los dados de manera aleatoria

            # En el bucle principal, después de lanzar los dados:
            suma_dados = dado1 + dado2

            # Verificar si la suma de los dados es 5
            if suma_dados == 5:
                # Verificar si hay dos fichas en la salida
                fichas_en_salida = [pos for pos in fichas[color] if pos == salidas[color]]
                if len(fichas_en_salida) < 2:  # Si hay menos de dos fichas en la salida
                    ficha_sacada = sacar_ficha_de_carcel(color)
                    if ficha_sacada:
                        print(f"¡Se sacó una ficha de la cárcel porque la suma de los dados es 5!")
                        # Si se sacó una ficha de la cárcel, mover otra ficha con la suma de los dados
                        fichas_disponibles = mostrar_fichas_disponibles(color)
                        if fichas_disponibles:
                            ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
                            if ficha_seleccionada is not None:
                                mover_ficha(color, ficha_seleccionada, suma_dados)
                                ultima_ficha_movida = (color, ficha_seleccionada)  # Registrar la última ficha movida
                    else:
                        print(f"No hay fichas en la cárcel para sacar con la suma de los dados igual a 5.")
                        # Si no se pudo sacar una ficha de la cárcel, mover una ficha con la suma de los dados
                        fichas_disponibles = mostrar_fichas_disponibles(color)
                        if fichas_disponibles:
                            ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
                            if ficha_seleccionada is not None:
                                mover_ficha(color, ficha_seleccionada, suma_dados)
                                ultima_ficha_movida = (color, ficha_seleccionada)  # Registrar la última ficha movida
                else:
                    print(f"¡Hay dos fichas en la salida de {color}! No se puede sacar otra ficha hasta que una se mueva.")
                    # Mover una ficha que ya está en el tablero
                    fichas_disponibles = mostrar_fichas_disponibles(color)
                    if fichas_disponibles:
                        ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
                        if ficha_seleccionada is not None:
                            mover_ficha(color, ficha_seleccionada, suma_dados)
                            ultima_ficha_movida = (color, ficha_seleccionada)  # Registrar la última ficha movida
            else:
                # Si la suma de los dados no es 5, verificar si uno de los dados es 5
                if dado1 == 5 or dado2 == 5:
                    # Verificar si hay dos fichas en la salida
                    fichas_en_salida = [pos for pos in fichas[color] if pos == salidas[color]]
                    if len(fichas_en_salida) < 2:  # Si hay menos de dos fichas en la salida
                        ficha_sacada = sacar_ficha_de_carcel(color)
                        if ficha_sacada:
                            print(f"¡Se sacó una ficha de la cárcel con un 5!")
                            # Si se sacó una ficha de la cárcel, mover otra ficha con el otro dado
                            if dado1 == 5:
                                pasos = dado2  # Usar el valor del otro dado
                            else:
                                pasos = dado1
                            # Mover una ficha que no esté en la cárcel
                            fichas_disponibles = mostrar_fichas_disponibles(color)
                            if fichas_disponibles:
                                ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
                                if ficha_seleccionada is not None:
                                    mover_ficha(color, ficha_seleccionada, pasos)
                                    ultima_ficha_movida = (color, ficha_seleccionada)  # Registrar la última ficha movida
                        else:
                            print(f"No hay fichas en la cárcel para sacar con un 5.")
                            # Si no se pudo sacar una ficha de la cárcel, mover una ficha con la suma de los dados
                            fichas_disponibles = mostrar_fichas_disponibles(color)
                            if fichas_disponibles:
                                ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
                                if ficha_seleccionada is not None:
                                    mover_ficha(color, ficha_seleccionada, suma_dados)
                                    ultima_ficha_movida = (color, ficha_seleccionada)  # Registrar la última ficha movida
                    else:
                        print(f"¡Hay dos fichas en la salida de {color}! No se puede sacar otra ficha hasta que una se mueva.")
                        # Mover una ficha que ya está en el tablero
                        fichas_disponibles = mostrar_fichas_disponibles(color)
                        if fichas_disponibles:
                            ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
                            if ficha_seleccionada is not None:
                                mover_ficha(color, ficha_seleccionada, suma_dados)
                                ultima_ficha_movida = (color, ficha_seleccionada)  # Registrar la última ficha movida
                else:
                    # Si no hay un 5, mover una ficha con la suma de los dados
                    fichas_disponibles = mostrar_fichas_disponibles(color)
                    if fichas_disponibles:
                        ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
                        if ficha_seleccionada is not None:
                            mover_ficha(color, ficha_seleccionada, suma_dados)
                            ultima_ficha_movida = (color, ficha_seleccionada)  # Registrar la última ficha movida

            # Regla 10: Verificar si los dados son iguales (par)
            if verificar_dados_iguales(dado1, dado2):
                print(f"¡Dados iguales! El equipo {color} repite su turno.")
                pares_consecutivos += 1  # Incrementar el contador de pares consecutivos
            else:
                pares_consecutivos = 0  # Reiniciar el contador si no son iguales

            # Regla 11: Manejar tres pares consecutivos
            manejar_tres_pares_consecutivos(color)

            # Verificar si hay movimientos posibles para el jugador actual
            if not hay_movimientos_posibles(color, dado1, dado2):
                print(f"No hay movimientos posibles para {color}. El turno pasa al siguiente jugador.")
                turno = (turno + 1) % len(jugadores)
                color = jugadores[turno]
                continue  # Pasar al siguiente turno

            # Cambiar el turno al siguiente jugador solo si no se sacó un 5 y no hay dados iguales
            if not verificar_dados_iguales(dado1, dado2):
                turno = (turno + 1) % len(jugadores)
                color = jugadores[turno]

    # Dibujar tablero y fichas
    screen.blit(tablero_img, (0, 0))
    dibujar_fichas()

    # Dibujar los dados (borrar antes de actualizar)
    pygame.draw.rect(screen, WHITE, (scaled_width - 153, 141, 145, 145))  # Dado 1
    pygame.draw.rect(screen, WHITE, (scaled_width - 153, 317.5, 145, 145))  # Dado 2

    # Dibujar números de los dados si se han lanzado
    if mostrar_dados:
        text1 = font.render(str(dado1), True, BLACK)
        text2 = font.render(str(dado2), True, BLACK)
        screen.blit(text1, (scaled_width - 115, 141))
        screen.blit(text2, (scaled_width - 115, 317.5))

    pygame.display.flip()  # Actualizar la pantalla UNA SOLA VEZ
    clock.tick(30)  # Controlar FPS

pygame.quit()