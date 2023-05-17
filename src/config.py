import pygame
import os

from src.sound import Sound
from src.theme import Theme

class Config: # lớp cấu hình 
        
    def __init__(self):# lớp thêm chủ đê 
        self.themes = []# danh sách chủ đề
        self._add_themes()
        self.idx = 0# chỉ số  của chủ đề 
        self.theme = self.themes[self.idx]# gọi 1 chủ đề trong ds chủ đề 
        self.font = pygame.font.SysFont('monospace', 18, bold=True) 
        # font chữ 
        self.move_sound = Sound(
            os.path.join('assets/sounds/move.wav'))
        self.capture_sound = Sound(
            os.path.join('assets/sounds/capture.wav'))
        
    def change_theme(self):#thay đổi chủ đề
        self.idx += 1
        self.idx %= len(self.themes)
        self.theme = self.themes[self.idx]


    def _add_themes(self):
        green = Theme((234, 235, 200), (119, 154, 88), (244, 247, 116), (172, 195, 51), '#C86464', '#C84646')
        brown = Theme((235, 209, 166), (165, 117, 80), (245, 234, 100), (209, 185, 59), '#C86464', '#C84646')
        blue = Theme((229, 228, 200), (60, 95, 135), (123, 187, 227), (43, 119, 191), '#C86464', '#C84646')
        gray = Theme((120, 119, 118), (86, 85, 84), (99, 126, 143), (82, 102, 128), '#C86464', '#C84646')

        self.themes = [green, brown, blue, gray]