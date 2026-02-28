import random

def stars_start(height, width):
    NUM_STARS = 100
    stars = []

    for _ in range(NUM_STARS):
        x = random.randint(0, width)
        y = random.randint(0, height)
        brightness = random.randint(100, 255)
        direction = random.choice([-1, 1])
        stars.append([x, y, brightness, direction])

    mostrar_estrelas = True

    return stars, mostrar_estrelas