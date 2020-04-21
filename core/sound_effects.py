import pygame
from threading import Thread

pygame.mixer.init()
apple_bite_sound = pygame.mixer.Sound("res/apple-bite.wav")
collision_sound = pygame.mixer.Sound("res/collide.wav")


def play_apple_bite():
    def wrapper():
        apple_bite_sound.play()
        pygame.time.delay(600)
        pygame.mixer.music.stop()

    Thread(target=wrapper, args=()).start()


def play_collision():
    def wrapper():
        collision_sound.play()
        pygame.time.delay(400)
        pygame.mixer.music.stop()

    Thread(target=wrapper, args=()).start()
