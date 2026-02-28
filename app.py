from tracemalloc import stop
import pygame
from components.stars import stars_start
from components.player import Player
from components.meteor import Meteor
import os
from dotenv import load_dotenv
import math
import time
import threading

pygame.init()

# Configurações da tela

load_dotenv()

WIDTH = int(os.getenv('WIDTH'))
HEIGHT = int(os.getenv('HEIGHT'))

screen = pygame.display.set_mode((int(WIDTH), int(HEIGHT)))
pygame.display.set_caption("Guardians Of Space")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 40)
subfont = pygame.font.SysFont("arial", 25)
details = pygame.font.SysFont("arial", 15)

# Aqui mostra as estrelas
stars, mostrar_estrelas = stars_start(HEIGHT, WIDTH)

# Aqui fica a logica dos meteoros
meteors = []
spawn_timer = 0
spawn_delay = 60
level = 1
score = 0

running = True
game_over = False

player = Player(WIDTH // 2, HEIGHT * 0.95)

seconds = 0
frame_count = 0
stop_count = False
last_second = 0

# Reseta o jogo
def reset_game():
    global player, meteors, spawn_timer, level, score, game_over, stop_count

    player = Player(WIDTH // 2, HEIGHT * 0.95)
    meteors = []
    spawn_timer = 0
    level = 1
    score = 0
    game_over = False
    stop_count = False

while running:
    clock.tick(60)

    frame_count += 1

    if frame_count == 60 and not stop_count:
        seconds += 1
        frame_count = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                mostrar_estrelas = not mostrar_estrelas

    screen.fill((0, 0, 0))  # fundo preto

    timer = details.render(f"Segundos percorridos: {seconds}", True, 'white')
    screen.blit(timer, (10, 10))

    # Logica de mostrar estrelas no fundo do espaco
    if mostrar_estrelas:
        for star in stars:
            x, y, brightness, direction = star

            # efeito de piscar
            brightness += direction * 2
            if brightness >= 255:
                brightness = 255
                direction = -1
            elif brightness <= 100:
                brightness = 100
                direction = 1

            star[2] = brightness
            star[3] = direction

            color = (brightness, brightness, brightness)
            pygame.draw.circle(screen, color, (x, y), 1)

    # Logica da nave movimentar
    if not game_over:
        if seconds % 20 == 0 and seconds != 0 and seconds != last_second:
            print(level)
            level += 1
            last_second = seconds

        keys = pygame.key.get_pressed()
        player.update(keys)
        player.draw(screen)

        # Logica do meteoro de spawnar cada meteoro
        spawn_timer += 1
        if spawn_timer >= spawn_delay:
            meteors.append(Meteor(level))
            spawn_timer = 0
        
        # logica de colisao
        for meteor in meteors[:]:
            meteor.update()
            meteor.draw(screen)

            if meteor.off_screen():
                meteors.remove(meteor)
            
            player_center_x = player.x + player.width // 2
            player_center_y = player.y + player.height // 2

            dist = math.sqrt((meteor.x - player_center_x) ** 2 +
                            (meteor.y - player_center_y) ** 2)

            if dist < meteor.radius + player.width // 2:
                game_over = True
            
    if game_over:
        stop_count = True
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        text = font.render("Voce foi atingido por um meteoro!", True, (255, 0, 0))
        subtext = subfont.render("Pressione o ESC para reiniciar o jogo", True, 'white')
        timer = details.render(f"Segundos percorridos: {seconds}", True, 'white')

        screen.blit(text, (WIDTH // 2 - text.get_width() // 2,
                        HEIGHT // 2 - text.get_height() // 2))

        screen.blit(subtext, (WIDTH // 2 - text.get_width() // 2.8,
                        (HEIGHT // 2 - text.get_height() // 2) + 50))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                reset_game()
                stop_count = False
                seconds = 0
                frame_count = 0

        elif event.type == pygame.QUIT:
            running = False
        
    pygame.display.flip()

pygame.quit()