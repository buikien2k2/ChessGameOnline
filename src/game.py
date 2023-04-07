import pygame

from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square

class Game:

    def __init__(self):
         self.next_player = 'white' 
         self.hovered_sqr = None
         self.board = Board()
         self.dragger = Dragger() 
         self.config = Config()

         #show methods

    def show_bg(self, surface):
        theme = self.config.theme

        for row in range(ROWS):  # thực hiện 2 vòng lặp để duyệt tất ca các hình vuông trên bàn cờ
            for col in range(COLS):
                    # color
                    color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                    # rect
                    rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                    # blit
                    pygame.draw.rect(surface, color, rect)

                      # tọa độ hàng , check tọa độ hàng =0 hay ko 
                    if col == 0: # đặt tọa độ cột
                    # color
                        color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                     # label
                        label = self.config.font.render(str(ROWS-row), 1, color)
                        label_pos = (5, 5 + row * SQSIZE)
                     # blit
                        surface.blit(label,label_pos)

                    # tọa độ cột 
                    if row == 7:
                    #color
                        color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    #label 
                        label = self.config.font.render(Square.get_alphacol(col), 1, color)
                        label_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    #blit
                        surface.blit(label,label_pos)
                              

    def show_pieces(self, surface):
        for row in range(ROWS):# thực hiện 2 vòng lặp để duyệt tất ca các hình vuông trên bàn cờ
            for col in range(COLS):
                # piece ?
                 if self.board.squares[row][col].has_piece():#kiểm tra nếu có một quân cờ trên một hình vuông
                    piece = self.board.squares[row][col].piece  # lưu quân cờ vào biến piece, gán vào piece để tối ưu
                    # all pieces except dragger piece
                    if piece is not self.dragger.piece:# hình ảnh khi di chuyển không bị nhòe 
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2 #căn hình ảnh giữa hình ảnh trên trục X và Y
                        piece.texture_rect = img.get_rect(center=img_center)# căn giữa hình ảnh trong hình vuông
                        surface.blit(img, piece.texture_rect)
    def show_moves(self, surface):
        theme = self.config.theme

        if self.dragger.dragging:
            piece = self.dragger.piece

            # loop all valid moves
            for move in piece.moves:
                # color
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                # rect
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)
              
    # other methods

    def show_last_move(self, surface):# hiển thị nước đi khi thả chuột là đúng hay sai nếu đúng là màu sáng nếu sai hiển thị màu đậm
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                # color
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                # rect
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            # color
            color = (180, 180, 180)
            # rect
            rect = (self.hovered_sqr.col * SQSIZE, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            # blit
            pygame.draw.rect(surface, color, rect, width=3)


    def next_turn(self):# tao phương thức mới để khi ng trắng đi sau đó đen đi sau đó trắng đi .. 
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, captured=False):# hiệu ứng âm thanh
        if captured:# check nếu một quân cờ bị ăn thì âm thanh ăn quân sẽ hiện lên 
            self.config.capture_sound.play()
        else:# ngược lại là âm thanh di chuyển quân bth 
            self.config.move_sound.play()

    def reset(self):
        self.__init__()# resset va tao tro choi moi     
