import pygame
import os
from dotenv import load_dotenv
import random

load_dotenv()

WIDTH = int(os.getenv('WIDTH'))
HEIGHT = int(os.getenv('HEIGHT'))

class Meteor:
    def __init__(self, level):
        self.radius = random.randint(10, 30)
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = -self.radius
        
        # velocidade aumenta com o level
        self.speed = random.uniform(2, 4) + level * 0.3
        
        # vida baseada no tamanho + level
        self.hp = 1 + level

        self.colors = ((139,69,19), (210,105,30), (222,184,135), (244,164,96))
        
    def update(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, random.choice(self.colors), (int(self.x), int(self.y)), self.radius)

    def off_screen(self):
        return self.y - self.radius > HEIGHT