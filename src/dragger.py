import pygame

from const import *

class Dragger: 
    
    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0 # goi 2 thuoc tinh nhap chuot cua 2 ng choi 
        self.mouseY = 0
        self.initial_row = 0 # cột và hàng ban đầu là 0 
        self.initial_col = 0

        #blit method 

    def update_blit(self, surface):
         #khi người chơi click quân cờ muốn đi quân cờ đó sẽ to ra hơn những quân cờ khác
        self.piece.set_texture(size=128)
        texture = self.piece.texture
        # img
        img = pygame.image.load(texture) #âm thanh quân cờ phát ra khi di chuyển
        # rect
        img_center = (self.mouseX, self.mouseY) #vị trí ảnh chính giữa
        self.piece.texture_rect = img.get_rect(center=img_center)
         #update Blit
        surface.blit(img, self.piece.texture_rect)

    #other methods       

    def update_mouse(self, pos):# chen 1 tham so + vị trí trong ví  trí sẽ kèm tọa độ
        self.mouseX, self.mouseY = pos # (xcor, ycor)

    def save_initial(self, pos):
        self.initial_row = pos[1] // SQSIZE
        self.initial_col = pos[0] // SQSIZE 

    def drag_piece(self, piece):# save piece when piece move
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False