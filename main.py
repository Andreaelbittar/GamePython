import pygame
import random
import sys

# Inicialización de Pygame
pygame.init()

# Dimensiones de la ventana del juego
WIDTH = 800
HEIGHT = 600

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Niveles de intensidad
INTENSITY_LEVELS = {
    1: 2,
    2: 4,
    3: 6,
    4: 8,
    5: 10
}

# Creación de la ventana del juego
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Esquivar Obstáculos")

clock = pygame.time.Clock()

# Cargar imagen de fondo
background_image = pygame.image.load("background.jpg").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Clase del jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Cargar imagen y escalarla
        self.image = pygame.image.load("mario.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

# Clase del obstáculo
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, color, speed):
        super().__init__()

        if color == RED:
            self.image = pygame.Surface((random.randint(10, 80), 20))
            self.image.fill(RED)
        elif color == BLUE:
            self.image = pygame.Surface((random.randint(10, 80), 20))
            self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = speed

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed_y = random.randint(1, 8)

# Función para mostrar el menú
def show_menu():
    menu_title_font = pygame.font.Font(None, 72)
    menu_start_font = pygame.font.Font(None, 50)
    menu_quit_font = pygame.font.Font(None, 50)

    menu_title = menu_title_font.render("Menu Principal", True, WHITE)
    menu_start = menu_start_font.render("Iniciar juego", True, WHITE)
    menu_quit = menu_quit_font.render("Salir", True, WHITE)

    menu_title_rect = menu_title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    menu_start_rect = menu_start.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    menu_quit_rect = menu_quit.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))

    while True:
        window.fill((0, 0, 0))
        window.blit(background_image, (0, 0))
        window.blit(menu_title, menu_title_rect)
        window.blit(menu_start, menu_start_rect)
        window.blit(menu_quit, menu_quit_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if menu_start_rect.collidepoint(mouse_pos):
                    return
                elif menu_quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

# Función para mostrar "GAME OVER"
def show_game_over():
    game_over_font = pygame.font.Font(None, 72)
    game_over_text = game_over_font.render("GAME OVER", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    window.fill((0, 0, 0))
    window.blit(background_image, (0, 0))
    window.blit(game_over_text, game_over_rect)
    pygame.display.flip()
    pygame.time.wait(5000)

# Mostrar menú antes de iniciar el juego
show_menu()

# Grupos de sprites
all_sprites = pygame.sprite.Group()
red_obstacles = pygame.sprite.Group()
blue_obstacles = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(2):
    red_obstacle = Obstacle(RED, INTENSITY_LEVELS[1])
    all_sprites.add(red_obstacle)
    red_obstacles.add(red_obstacle)

    blue_obstacle = Obstacle(BLUE, INTENSITY_LEVELS[1])
    all_sprites.add(blue_obstacle)
    blue_obstacles.add(blue_obstacle)

# Variables del juego
score = 0
current_level = 1

# Fuente de texto
font = pygame.font.Font(None, 36)

# Bucle principal del juego
running = True
level_timer = pygame.time.get_ticks() + 10000  # Timer para cambiar de nivel después de 10 segundos
while running:
    # Actualización de la ventana del juego
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Renderizar imagen de fondo
    window.blit(background_image, (0, 0))

    # Actualización de los sprites
    all_sprites.update()

    # Comprobación de colisiones con obstáculos rojos
    hits_red = pygame.sprite.spritecollide(player, red_obstacles, False)
    if hits_red:
        show_game_over()
        show_menu()
        all_sprites.empty()
        red_obstacles.empty()
        blue_obstacles.empty()
        player = Player()
        all_sprites.add(player)
        for i in range(2):
            red_obstacle = Obstacle(RED, INTENSITY_LEVELS[1])
            all_sprites.add(red_obstacle)
            red_obstacles.add(red_obstacle)

            blue_obstacle = Obstacle(BLUE, INTENSITY_LEVELS[1])
            all_sprites.add(blue_obstacle)
            blue_obstacles.add(blue_obstacle)
        score = 0
        current_level = 1

    # Comprobación de colisiones con obstáculos azules
    hits_blue = pygame.sprite.spritecollide(player, blue_obstacles, False)
    if hits_blue:
        score += 1
        for hit in hits_blue:
            hit.rect.x = random.randint(0, WIDTH - hit.rect.width)
            hit.rect.y = random.randint(-100, -40)
            hit.speed_y = random.randint(1, INTENSITY_LEVELS[current_level])

    # Dibujar puntuación y nivel actual en la pantalla
    score_text = font.render("Puntuación: {}".format(score), True, WHITE)
    level_text = font.render("Nivel: {}".format(current_level), True, WHITE)
    window.blit(score_text, (10, 10))
    window.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))

    # Cambiar de nivel cada 10 segundos
    if pygame.time.get_ticks() >= level_timer:
        current_level += 1
        level_timer += 10000
        if current_level == 6:
            game_won_font = pygame.font.Font(None, 72)
            game_won_text = game_won_font.render("¡GANASTE!", True, WHITE)
            game_won_rect = game_won_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            window.fill((0, 0, 0))
            window.blit(background_image, (0, 0))
            window.blit(game_won_text, game_won_rect)
            pygame.display.flip()
            pygame.time.wait(5000)
            show_menu()
            all_sprites.empty()
            red_obstacles.empty()
            blue_obstacles.empty()
            player = Player()
            all_sprites.add(player)
            for i in range(2):
                red_obstacle = Obstacle(RED, INTENSITY_LEVELS[1])
                all_sprites.add(red_obstacle)
                red_obstacles.add(red_obstacle)

                blue_obstacle = Obstacle(BLUE, INTENSITY_LEVELS[1])
                all_sprites.add(blue_obstacle)
                blue_obstacles.add(blue_obstacle)
            score = 0
            current_level = 1
        else:
            for red_obstacle in red_obstacles:
                red_obstacle.speed_y = random.randint(1, INTENSITY_LEVELS[current_level])
            for blue_obstacle in blue_obstacles:
                blue_obstacle.speed_y = random.randint(1, INTENSITY_LEVELS[current_level])

    # Dibujar sprites en la pantalla
    all_sprites.draw(window)

    # Actualizar la pantalla
    pygame.display.flip()

# Salir del juego
pygame.quit()
sys.exit()
