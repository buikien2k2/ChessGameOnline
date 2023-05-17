from src.const import *
from src.square import Square
from src.piece import *
from src.move import Move
from src.sound import Sound
import copy
import os

class Board: 

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]#tạo một danh sách tám số không cho mỗi cột
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move ,testing=False):
        initial = move.initial
        final = move.final

        en_passant_empty = self.squares[final.row][final.col].isempty()
        # tốt phong cấp 
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        if isinstance(piece, Pawn):
             # en passant capture
            diff = final.col - initial.col
            if diff != 0 and en_passant_empty:
                # console board move update
                self.squares[initial.row][initial.col + diff].piece = None
                self.squares[final.row][final.col].piece = piece
                if not testing:
                    sound = Sound(
                        os.path.join('assets/sounds/capture.wav'))
                    sound.play()

            # pawn promotion
            else:
                self.check_promotion(piece, final)

        # nhập thành

        if isinstance(piece, King):
            if self.castling(initial, final) and not testing:
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        # move 
        piece.moved = True
       # clear valid moves
        piece.clear_moves()
        # set last move     
        self.last_move = move 
    

    def valid_move(self, piece, move):  
        return move in piece.moves
    
    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2
    def set_true_en_passant(self, piece):
        
        if not isinstance(piece, Pawn):
            return

        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False
        
        piece.en_passant = True

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move, testing=True)
        
        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_rival_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        
        return False

               
    def calc_moves(self, piece, row, col, bool=True):
        '''
           calculate all the posiable(valib) moves of an specific piece on specific position
        '''

        def pawn_moves():# hàm để tốt di chuyển ("khó nhất")
            # steps
            steps = 1 if piece.moved else 2# kiểm tra nếu quân cờ đã di chuyển quân cờ di chuyển là 1 ngược lại quân cờ chưa di chuyển nhưng quân tốt của đối phương có thể di chuyển 1 ô hoặc 2 ô           
            

            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):  # di chuyển hàng trong phạm vi vượt qua, bắt đầu, kết thúc
                if Square.in_range(possible_move_row): # check có hình vuông có quân trông không nếu 
                    if self.squares[possible_move_row][col].isempty():
                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        # create a new move
                        move = Move(initial, final)

                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
                            # append new move
                            piece.add_move(move)
                    # blocked
                    else: break
                # not in range
                else: break
                    
            # diagonal moves 

            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):# check nếu ô vuông ở đây có không gian di chuyển hay ko 
                    if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):# nếu có quân đối thử khác màu sẽ có thể ăn quân
                        # create initial and final move squares
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create a new move
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
                            # append new move
                            piece.add_move(move)    

           # en passant moves 
            r = 3 if piece.color == 'white' else 4
            fr = 2 if piece.color == 'white' else 5
            # left en pessant
            if Square.in_range(col-1) and row == r:
                if self.squares[row][col-1].has_rival_piece(piece.color):
                    p = self.squares[row][col-1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # create initial and final move squares
                            initial = Square(row, col)
                            final = Square(fr, col-1, p)
                            # create a new move
                            move = Move(initial, final)

                            # check potencial checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)

            # right en pessant
            if Square.in_range(col+1) and row == r:
                if self.squares[row][col+1].has_rival_piece(piece.color):
                    p = self.squares[row][col+1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # create initial and final move squares
                            initial = Square(row, col)
                            final = Square(fr, col+1, p)
                            # create a new move
                            move = Move(initial, final)
                            
                            # check potencial checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)

        def knight_moves():# check knight?
            # knight is 8 moves if knight is knight center
            possible_moves = [
                (row - 2, col + 1),# nghĩa là bước di chuyển quân mã là lên cốt 2 ô vuông , hàng tăng 1 ô vuông
                (row - 1, col + 2),
                (row + 1, col + 2),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row + 1, col - 2),
                (row - 1, col - 2),
                (row - 2, col - 1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                # kiem tra quan co di chuyen dung ko, hinh vuong do trong hay la co quan khac dang o tren 
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        # create squares of the new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create new move
                        move = Move(initial, final)

                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            else: break
                        else:
                            # append new move
                            piece.add_move(move)

        def straightline_moves(incrs):# phương thức di chuyển theo đường thằng 
            for incr in incrs:#lặp lại các nước đi 
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):# nếu hình vuông trống
                        # create squares of the possible new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)

                        # create a possible new move
                        move = Move(initial, final)

                        # empty = continue looping 
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)
                        # has rival piece 
                        elif self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color): # tiếp tục kiểm tra nếu có quân địch 
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)
                            break 

                        # has   team piece = break 
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                    
                    else : break  # ngược lại nếu ko trong pham vi 

                    # tăng dần 
                    possible_move_row =  possible_move_row + row_incr 
                    possible_move_col =  possible_move_col + col_incr

        def king_moves(): # 11 nuoc di chuyen (2 nuoc nhap thanh xa, gan )
            adjs = [
                (row - 1, col + 0), # vua lên
                (row - 1, col + 1),  # vua đi lên phải
                (row + 0, col + 1),  # vua đi sang phải
                (row + 1, col + 1),  # vua đi xuống phải 
                (row + 1, col + 0),  # vua đi xuống
                (row + 1, col - 1),  # vua đi xuống trái
                (row + 0, col - 1),  # vua đi bên trái 
                (row -1 , col - 1),  # vua đi lên trái

            ] 

            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        # create squares of the new move

                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col) # piece=piece
                        # create new move
                        move = Move(initial, final)
                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            else: break
                        else:
                            # append new move
                            piece.add_move(move)
            # castling moves
            if not piece.moved:
                # queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            # castling is not possible because there are pieces in between ?
                            if self.squares[row][c].has_piece():
                                break

                            if c == 3:
                                # adds left rook to king
                                piece.left_rook = left_rook

                                # rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)
                                

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        # append new move to rook
                                        left_rook.add_move(moveR)
                                        # append new move to king
                                        piece.add_move(moveK)
                                else:
                                    # append new move to rook
                                    left_rook.add_move(moveR)
                                    # append new move king
                                    piece.add_move(moveK)
                               

                # king castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            # castling is not possible because there are pieces in between ?
                            if self.squares[row][c].has_piece():
                                break

                            if c == 6:
                                # adds right rook to king
                                piece.right_rook = right_rook

                                # rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)

                                # check potencial checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                        # append new move to rook
                                        right_rook.add_move(moveR)
                                        # append new move to king
                                        piece.add_move(moveK)
                                else:
                                    # append new move to rook
                                    right_rook.add_move(moveR)
                                    # append new move king
                                    piece.add_move(moveK)

        if isinstance(piece, Pawn): #kiểm tra xem quân cờ có đi đúng nước hay ko khi quân cờ di chuyển sự gia tăng lên thì cột giảm (nước đi đầu tiên)
            
            pawn_moves()

        elif isinstance(piece, Knight):
            
            knight_moves() # method in method

        elif isinstance(piece, Bishop): 
            straightline_moves([
                (-1, 1), # nước đường chéo phía bên phải 1 nc
                (-1, -1), # bên trái
                (1, 1), # gia tăng phía bên phải khi lùi bên phải
                (1, -1), # bên trái
            ])
           
        elif isinstance(piece, Rook): 
            straightline_moves([
                (-1, 0), # di chuyển lên 1 ô
                (0, 1),  # xe đối diện lên 1 ô 
                (1, 0), # xe lùi 1 nc 
                (0, -1), # xe đối diện lùi 1 nc

            ])


        elif isinstance(piece, Queen):
            straightline_moves([
                (-1, 1), # nước đường chéo phía bên phải 1 nc
                       
                (-1, -1), # bên trái
                (1, 1), # gia tăng phía bên phải khi lùi bên phải
                (1, -1), # bên trái
                (-1, 0), # di chuyển lên 1 ô
                (0, 1),  # xe đối diện lên 1 ô 
                (1, 0), # xe lùi 1 nc 
                (0, -1), # xe đối diện lùi 1 nc
                
           ])

        elif isinstance(piece, King):
            king_moves()

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)
        
    def _add_pieces(self, color): #sắp thứ tự quân (hàng 6,7 là quân trắng) ngược lại hàng 1,0 là quân đen
       
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
           
        # knights
            self.squares[row_other][1] = Square(row_other, 1, Knight(color))#quân mã sẽ ở cột 1 và cột 6 
            self.squares[row_other][6] = Square(row_other, 6, Knight(color))
        # bishops
            self.squares[row_other][2] = Square(row_other, 2, Bishop(color))#quân tượng sẽ ở cột 2 và cột 5 
            self.squares[row_other][5] = Square(row_other, 5, Bishop(color))
            

        # rooks
            self.squares[row_other][0] = Square(row_other, 0, Rook(color))#quân xe sẽ ở cột 0 và cột 7 
            self.squares[row_other][7] = Square(row_other, 7, Rook(color))
  
        # queen
            self.squares[row_other][3] = Square(row_other, 3, Queen(color)) #quân hậu sẽ ở cột 3

        # king
            self.squares[row_other][4] = Square(row_other, 4, King(color))#quân vua sẽ ở cột 4 
