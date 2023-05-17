import pygame
import sys

from src.const import *
from src.game import Game
from src.square import Square
from src.move import Move
from src.player import Player

from src.network import Network

#FPS
FPS = 60
CLOCK = pygame.time.Clock()

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1]), int(str[2]), int(str[3])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3])

class Client:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) # hiển hị màn hình kích thước setup trong const
        pygame.display.set_caption('Chess-Game-AI')
        self.game = Game()

    def mainloop(self):
        n = Network()
        startPos = read_pos(n.getPos())
        p = Player(startPos[0],startPos[1], startPos[2], startPos[3], "white")
        p2 = Player(0,0,0,0, "black")
        screen = self.screen
        game = self.game
        dragger = self.game.dragger
        board = self.game.board
        if startPos == (0, 0, 0, 0):
            player1_color = "white"
            player2_color = "black"
        else:
            player1_color = "black"
            player2_color = "white"
        while True:
            game.show_bg(screen) # SHOW MÀN HÌNH
            game.show_last_move(screen) 
            game.show_moves(screen)
            game.show_pieces(screen) # show bàn cờ
            game.show_hover(screen)

            if game.next_player == player2_color:
                p2Pos = read_pos(n.send(make_pos((p.x, p.y,p.m, p.n))))
                move = p2Pos
                p2.x = init_row = move[0]
                p2.y = init_col = move[1]
                p2.m = final_row = move[2]
                p2.n = final_col = move[3]
                clicked_row = init_row
                clicked_col = init_col
                released_row = final_row
                released_col = final_col
                    
                # if click square có một picece ?
                if board.squares[clicked_row][clicked_col].has_piece():
                    piece = board.squares[clicked_row][clicked_col].piece
                # valid piece (color) ?
                    if piece.color == game.next_player:
                        board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                        dragger.save_initial2((init_col, init_row))
                        dragger.drag_piece(piece)        
                initial = Square(dragger.initial_row, dragger.initial_col)
                final = Square(released_row, released_col)
                move = Move(initial, final)
                if dragger.dragging:
                    if board.valid_move(dragger.piece, move): 
                        captured = board.squares[released_row][released_col].has_piece()
                        board.set_true_en_passant(dragger.piece)
                        board.move(dragger.piece, move)
                        # sound
                        game.play_sound(captured)
                        # show methods
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_pieces(screen)
                        #next turn
                        game.next_turn()
                dragger.undrag_piece()
            # p2.update()
            for event in pygame.event.get():
                if game.next_player == player1_color:
                    # click piece
                    if event.type == pygame.MOUSEBUTTONDOWN: # khi người chơi nhấp chuột thì.
                        dragger.update_mouse(event.pos)   #in ra vị trí khi nhấp chuột vào 
                    # kiểm tra xem có quân cờ tại vị trí click chuột ko 
                        clicked_row = dragger.mouseY // SQSIZE
                        clicked_col = dragger.mouseX // SQSIZE

                        # if click square có một picece ?
                        
                        if board.squares[clicked_row][clicked_col].has_piece():
                            piece = board.squares[clicked_row][clicked_col].piece
                        # valid piece (color) ?
                            if piece.color == game.next_player:
                                board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                dragger.save_initial(event.pos)
                                dragger.drag_piece(piece)      
                            # show methods 
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_moves(screen)
                                game.show_pieces(screen)  
                    #mouse motion kiểm tra đúng là người chơi    đang kéo quân cờ hay không
                    elif event.type == pygame.MOUSEMOTION:
                        motion_row = event.pos[1] // SQSIZE 
                        motion_col = event.pos[0] // SQSIZE

                        game.set_hover(motion_row,motion_col)

                        if dragger.dragging: # boolearn  
                                dragger.update_mouse(event.pos)
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_moves(screen)
                                game.show_pieces(screen)
                                game.show_hover(screen)
                                dragger.update_blit(screen)

                        # click release     
                    elif event.type == pygame.MOUSEBUTTONUP:# nếu người chơi buông chuột (release) thì:
                    
                        if dragger.dragging:# nếu kéo quân thực hiện nhấp chuột quân ở đã di chuyển   
                            dragger.update_mouse(event.pos)

                            released_row = dragger.mouseY // SQSIZE# sự chuyển đổi vị trí(ô vuông) khi di chuyển quân cờ
                            released_col = dragger.mouseX // SQSIZE

                            
                            # kiểm tra quân cờ di chuyển đúng vị trí ko 
                            # tạo vị trí di chuyển mới 
                            initial = Square(dragger.initial_row, dragger.initial_col)
                            final = Square(released_row, released_col)
                            move = Move(initial, final)

                                # nếu đây là di chuyển hợp lệ âm thanh đc sử dụng
                            if board.valid_move(dragger.piece, move): 

                                n.send(make_pos((clicked_row, clicked_col, released_row, released_col)))
                                
                                captured = board.squares[released_row][released_col].has_piece()
                                board.set_true_en_passant(dragger.piece)
                                board.move(dragger.piece, move)
                                # sound
                                game.play_sound(captured)
                                # show methods
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_pieces(screen)
                                #next turn
                                game.next_turn()

                        dragger.undrag_piece()

                        # key press
                    elif event.type == pygame.KEYDOWN:
                            # change themes
                        if event.key == pygame.K_t:
                                game.change_theme()
                            # change themes
                        if event.key == pygame.K_r:
                                game.reset()
                                game = self.game
                                board = self.game.board
                                dragger = self.game.dragger
                    #quit application  
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                pygame.display.update()
                CLOCK.tick(FPS)
        
# main = Main()
# main.mainloop()