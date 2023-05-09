import pygame

from const import *
from game import Game
from square import Square
from move import Move


class Player:
    def __init__(self, x, y, m, n):
        self.x = x
        self.y = y
        self.m = m
        self.n = n

    # def player_moves(self, p2Pos, x, y, m, n, board, game, dragger ,screen):
    #     p2Pos  = (0,0,0,0)
    #     x = clicked_row = p2Pos[0]
    #     y = clicked_col = p2Pos[1]
    #     m = released_row  = p2Pos[2]
    #     n = released_col  = p2Pos[3]
    #     # if click square có một picece ?
    #     if board.squares[clicked_row][clicked_col].has_piece():
    #         piece = board.squares[clicked_row][clicked_col].piece
    #     # valid piece (color) ?
    #         if piece.color == game.next_player:
    #             board.calc_moves(piece, clicked_row, clicked_col, bool=True)
    #             dragger.save_initial2((clicked_col, clicked_row))
    #             dragger.drag_piece(piece)        
    #     initial = Square(dragger.initial_row, dragger.initial_col)
    #     final = Square(released_row, released_col)
    #     move = Move(initial, final)
    #     if dragger.dragging:
    #         if board.valid_move(dragger.piece, move): 
    #             captured = board.squares[released_row][released_col].has_piece()
    #             board.set_true_en_passant(dragger.piece)
    #             board.move(dragger.piece, move)
    #             # sound
    #             game.play_sound(captured)
    #             # show methods
    #             game.show_bg(screen)
    #             game.show_last_move(screen)
    #             game.show_pieces(screen)
    #             #next turn
    #             game.next_turn()
    #     dragger.undrag_piece()