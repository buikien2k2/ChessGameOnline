import pygame

class Sound:

    def __init__(self, path):
        self.path = path
        self.sound = pygame.mixer.Sound(path)# đường dẫn của âm thanh vào game

    def play(self):
        pygame.mixer.Sound.play(self.sound)  # âm thanh của trò chơi     