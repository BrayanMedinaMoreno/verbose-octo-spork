import pygame
import random

# Inicializar Pygame
pygame.init()

# Configurar la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Juego de Ataque")

# Colores
black = (0, 0, 0)
white = (255, 255, 255)

# Dimensiones de los sprites
SPRITE_WIDTH = 30
SPRITE_HEIGHT = 30

# Cargar la hoja de sprites
sprite_sheet = pygame.image.load("BIRDSPRITESHEET_Blue_recortada.png").convert_alpha()

# Cargar la imagen de fondo
background_image = pygame.transform.scale(pygame.image.load("elements.png"), (screen_width, screen_height)).convert()

# Función para obtener un sprite de la hoja de sprites
def get_sprite(sheet, frame, width, height):
    x = (frame % 8) * width
    y = (frame // 8) * height
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), (x, y, width, height))
    return sprite

# Obtener un sprite estático para el jugador y los enemigos
player_sprite = get_sprite(sprite_sheet, 0, SPRITE_WIDTH, SPRITE_HEIGHT)
enemy_sprite = get_sprite(sprite_sheet, 0, SPRITE_WIDTH, SPRITE_HEIGHT)

# Jugador
player_size = 40
player_pos = [screen_width // 2, screen_height - 2 * player_size]
player_image = pygame.transform.scale(player_sprite, (player_size, player_size))

# Enemigos
enemy_size = 40
enemy_list = []
enemy_image = pygame.transform.scale(enemy_sprite, (enemy_size, enemy_size))

# Velocidad
speed = 10
enemy_speed = 5

# Reloj
clock = pygame.time.Clock()

# Fuente
font = pygame.font.SysFont("monospace", 26)

# Función para dibujar enemigos
def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        screen.blit(enemy_image, (enemy_pos[0], enemy_pos[1]))

# Función para actualizar la posición de los enemigos
def update_enemy_positions(enemy_list, speed):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < screen_height:
            enemy_pos[1] += speed
        else:
            enemy_list.pop(idx)
            new_enemy_pos = [random.randint(0, screen_width - enemy_size), 0]
            while check_overlap(new_enemy_pos, enemy_list):
                new_enemy_pos = [random.randint(0, screen_width - enemy_size), 0]
            enemy_list.append(new_enemy_pos)

# Función para detectar colisiones
def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True
    return False

# Función para detectar colisión entre jugador y enemigo
def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    # Ajustar las hitboxes para que sean más pequeñas
    hitbox_offset = 10
    if (e_x + hitbox_offset >= p_x and e_x + hitbox_offset < (p_x + player_size - hitbox_offset)) or (p_x + hitbox_offset >= e_x and p_x + hitbox_offset < (e_x + enemy_size - hitbox_offset)):
        if (e_y + hitbox_offset >= p_y and e_y + hitbox_offset < (p_y + player_size - hitbox_offset)) or (p_y + hitbox_offset >= e_y and p_y + hitbox_offset < (e_y + enemy_size - hitbox_offset)):
            return True
    return False

# Función para verificar si hay superposición de enemigos
def check_overlap(new_enemy_pos, enemy_list):
    for enemy_pos in enemy_list:
        if detect_collision(new_enemy_pos, enemy_pos):
            return True
    return False

# Función para mostrar el menú principal
def show_menu():
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        screen.fill(black)
        menu_text = font.render("Presiona ENTER para jugar o Q para salir", True, white)
        screen.blit(menu_text, (screen_width // 2 - menu_text.get_width() // 2, screen_height // 2 - menu_text.get_height() // 2))
        pygame.display.update()
        clock.tick(15)

# Función para mostrar el menú de fin de juego
def show_game_over_menu():
    game_over_menu = True
    while game_over_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_over_menu = False
                    main_game()
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        screen.fill(black)
        game_over_text = font.render("Presiona R para reiniciar o Q para salir", True, white)
        game_over_text2 = font.render("Juego Terminado.", True, white)
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))
        screen.blit(game_over_text2, (screen_width // 2 - game_over_text2.get_width() // 2, screen_height // 3 - game_over_text2.get_height() // 3))
        pygame.display.update()
        clock.tick(15)

# Función para agregar enemigos
def add_enemies(enemy_list, num_enemies):
    for _ in range(num_enemies):
        new_enemy_pos = [random.randint(0, screen_width - enemy_size), random.randint(-screen_height, 0)]
        while check_overlap(new_enemy_pos, enemy_list):
            new_enemy_pos = [random.randint(0, screen_width - enemy_size), random.randint(-screen_height, 0)]
        enemy_list.append(new_enemy_pos)

# Función principal del juego
def main_game():
    game_over = False
    enemy_list.clear()
    enemy_count = 3
    max_enemies = 10
    add_enemies(enemy_list, enemy_count)
    time_counter = 0
    global speed, enemy_speed
    speed = 10
    enemy_speed = 5

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= speed
        if keys[pygame.K_RIGHT] and player_pos[0] < screen_width - player_size:
            player_pos[0] += speed

        # Dibujar la imagen de fondo
        screen.blit(background_image, (0, 0))

        update_enemy_positions(enemy_list, enemy_speed)
        draw_enemies(enemy_list)

        screen.blit(player_image, (player_pos[0], player_pos[1]))

        if collision_check(enemy_list, player_pos):
            game_over = True

        # Aumentar la cantidad y velocidad de enemigos progresivamente
        if len(enemy_list) < max_enemies:
            add_enemies(enemy_list, 1)
            enemy_count += 1

        # Aumentar la velocidad de los enemigos y del jugador con el tiempo
        time_counter += 1
        if time_counter % 500 == 0:
            enemy_speed += 1
            speed += 1

        pygame.display.update()

        clock.tick(30)

    show_game_over_menu()

# Mostrar el menú principal y comenzar el juego
show_menu()
main_game()
pygame.quit()
