class Figure:
    possible_moves = []
    color = "black"
    image = None
    def __init__(self,color):
        self.color = color
    def get_possible_moves(self,coords: list, board: list):
        moves = []
        for cell in moves:
            if (cell[0] or cell[1]) > 7 or (cell[0] or cell[1]) < 0:
                moves.remove(cell)      
        return moves

class Pawn(Figure):
    image = "Chess/images/-color_pawn.png"
    def get_all_special_attacks(self, coords: list, board: dict):
        moves = []
        row, col = coords
        if self.color == "white":
            moves.append((row+1,col+1))
            moves.append((row+1,col-1))
        else:
            moves.append((row-1,col+1))
            moves.append((row-1,col-1))
        return moves
    def get_special_attacks(self,coords: list, board: dict):
        moves = []
        row, col = coords
        if self.color == "white":
            #Check if figure can go diagonally
            if board.get((row+1,col+1)) != None and board.get((row+1,col+1)).color == "black":
                moves.append((row+1,col+1))
            if board.get((row+1,col-1)) != None and board.get((row+1,col-1)).color == "black":
                moves.append((row+1,col-1))
        else:
            if board.get((row-1,col+1)) != None and board.get((row-1,col+1)).color == "white":
                moves.append((row-1,col+1))
            if board.get((row-1,col-1)) != None and board.get((row-1,col-1)).color == "white":
                moves.append((row-1,col-1))
        return moves

    def get_possible_moves(self, coords: list, board: dict):
        moves = []
        row, col = coords
        if self.color == "white":
            #Check if figure can go diagonally
            if (row == 1) and (board.get((row+1,col)) == None) and (board.get((row+2,col)) == None):
                moves.append((row+2,col))
            if board.get((row+1,col)) == None:
                moves.append((row+1,col))
        else:
            if (row == 6) and (board.get((row-1,col)) == None) and (board.get((row-2,col)) == None):
                moves.append((row-2,col))
            if board.get((row-1,col)) == None:
                moves.append((row-1,col))
        moves.extend(self.get_special_attacks(coords,board))
        return moves

class King(Figure):
    possible_moves = [[0,1],[1,0],[1,1],[-1,1]]
    image = "Chess/images/-color_king.png"
    def get_possible_moves(self, coords, board: dict):
        king_moves = []
        row, col = coords
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]
        for x, y in directions:
            new_row, new_col = row + x, col + y
            # Is within board
            if (0 <= new_row <= 7) and (0 <= new_col <= 7):
                if board.get((new_row, new_col)) is None:
                    king_moves.append((new_row, new_col))
                elif board.get((new_row, new_col)).color != self.color:
                    king_moves.append((new_row, new_col))
        #Remove possible check cells
        for cell in board:
            #Get figure at coords
            figure = board.get(cell)
            #Is figure, is not same color, is not King
            if isinstance(figure,Figure) and figure.color != self.color and not isinstance(figure,King):#Upravit i pro kinga!!!
                #Get possible moves of the figure
                if not isinstance(figure,Pawn):
                    for possible_move in figure.get_possible_moves(cell,board):
                        #If moves of king contains possible move of the figure
                        if possible_move in king_moves:
                            #Remove move from kings moves
                            king_moves.remove(possible_move)
                else:
                    for pawn_attack in figure.get_all_special_attacks(cell,board).copy():
                        if pawn_attack in king_moves:
                            king_moves.remove(pawn_attack)
        return king_moves

class Queen(Figure):
    image = "Chess/images/-color_queen.png"
    def get_possible_moves(self, coords, board: dict):
        moves = []
        row, col = coords
        directions = [[1, 1], [1, -1], [-1, 1], [-1, -1], [0, 1], [0, -1], [1, 0], [-1, 0]]
        for x, y in directions:
            new_row, new_col = row, col
            while True:
                new_row += x
                new_col += y
                # Is within board
                if (0 <= new_row <= 7) and (0 <= new_col <= 7):
                    if board.get((new_row, new_col)) == None:
                        moves.append((new_row, new_col))
                    elif board.get((new_row, new_col)).color != self.color:
                        moves.append((new_row, new_col))
                        break
                    else:
                        break
                else:
                    break
        return moves

class Bishop(Figure):
    image = "Chess/images/-color_bishop.png"
    def get_possible_moves(self, coords, board: dict):
        moves = []
        row, col = coords
        directions = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
        for x, y in directions:
            new_row, new_col = row, col
            while True:
                new_row += x
                new_col += y
                # Is within board
                if (0 <= new_row <= 7) and (0 <= new_col <= 7):
                    if board.get((new_row, new_col)) == None:
                        moves.append((new_row, new_col))
                    elif board.get((new_row, new_col)).color != self.color:
                        moves.append((new_row, new_col))
                        break
                    else:
                        break
                else:
                    break
        return moves

class Knight(Figure):
    moves_between_coords = False
    image = "Chess/images/-color_knight.png"
    def get_possible_moves(self, coords, board: dict):
        moves = []
        row, col = coords
        directions = [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2]]
        for x, y in directions:
            new_row, new_col = row + x, col + y
            #Is within board
            if (new_row >= 0 and new_row <= 7) and (new_col >= 0 and new_col <= 7):
                #Is empty
                if board.get((new_row, new_col)) == None:
                    moves.append((new_row, new_col))
                #Is enemy
                elif board.get((new_row, new_col)).color != self.color:
                    moves.append((new_row, new_col))
        return moves

class Rook(Figure):
    image = "Chess/images/-color_rook.png"
    def get_possible_moves(self, coords, board: dict):
        moves = []
        row, col = coords
        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        for x, y in directions:
            new_row, new_col = row, col
            while True:
                new_row += x
                new_col += y
                # Is within board
                if (0 <= new_row <= 7) and (0 <= new_col <= 7):
                    if board.get((new_row, new_col)) is None:
                        moves.append((new_row, new_col))
                    elif board.get((new_row, new_col)).color != self.color:
                        moves.append((new_row, new_col))
                        break
                    else:
                        break
                else:
                    break
        return moves