import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move
class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) # hiển hị màn hình kích thước setup trong const
        pygame.display.set_caption('Chess-Game-AI')
        self.game = Game()

    def mainloop(self):
         
        screen = self.screen
        game = self.game
        dragger = self.game.dragger
        board = self.game.board
        
        while True:
            game.show_bg(screen) # SHOW MÀN HÌNH
            game.show_last_move(screen) 
            game.show_moves(screen)
            game.show_pieces(screen) # show bàn cờ
            game.show_hover(screen)

            if dragger.dragging: # nếu quân cờ khi click chuột hiển thị đúng
                 dragger.update_blit(screen)


            for event in pygame.event.get():

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
                    elif event.type == pygame.QUIT:
                          pygame.quit()
                          sys.exit()



                    pygame.display.update()

main = Main()
main.mainloop()
