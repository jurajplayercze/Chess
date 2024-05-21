import pygame
from figures import Rook,Knight,Bishop,Queen,King,Pawn,Figure

#-Options------------------------------------------------
RESOLUTION = 600,600
CELL_SIZE = 75
COLOR_TURN = "white"
#--------------------------------------------------------

BOARD = {}
END = False
SELECTED_FIGURE = None
SELECTED_FIGURE_COORDS = None

def set_figure(screen: pygame.Surface, figure: Figure, coords):
    BOARD[coords] = figure
    i = (str(figure.image)).replace("-color",figure.color)
    i = pygame.image.load(i)
    image = pygame.transform.scale(i, (CELL_SIZE,CELL_SIZE))
    screen.blit(image, (coords[1] * CELL_SIZE, (7 - coords[0]) * CELL_SIZE))

def reset_color_cell(coords):
    pygame.draw.rect(screen, ("gray30" if (coords[0] + coords[1]) % 2 != 0 else "white"), (coords[1] * CELL_SIZE, (7 - coords[0]) * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_ending_screen(loser):
    if COLOR_TURN == "white":
        winner = "black"
    else:
        winner = "white"
    pygame.draw.rect(screen, "chartreuse4", ((RESOLUTION[0] // 2 - RESOLUTION[0] // 6), (RESOLUTION[1] // 2 - RESOLUTION[1] // 6), (RESOLUTION[0] // 3), (RESOLUTION[0] // 3)))
    font = pygame.font.Font(None,40)
    text_window = font.render("Winner: " + winner, True, ("black" if winner == "black" else "white"))
    text_rect = text_window.get_rect()
    text_rect.center = (RESOLUTION[0] // 2, RESOLUTION[1] // 2)
    screen.blit(text_window, text_rect)

def reset_selection():
    global SELECTED_FIGURE, SELECTED_FIGURE_COORDS
    SELECTED_FIGURE = None
    SELECTED_FIGURE_COORDS = None

def init_board(screen):
    for col, piece in enumerate([Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]):
        BOARD[(0, col)] = piece("white")
        set_figure(screen, piece("white"), (0, col))
    for col in range(8):
        BOARD[(1, col)] = Pawn("white")
        set_figure(screen, Pawn("white"), (1, col))
    for col, piece in enumerate([Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]):
        BOARD[(7, col)] = piece("black")
        set_figure(screen, piece("black"), (7, col))
    for col in range(8):
        BOARD[(6, col)] = Pawn("black")
        set_figure(screen, Pawn("black"), (6, col))
    for row in range(2, 6):
        for col in range(8):
            BOARD[(row, col)] = None

def is_same_color(color,coords):
    cell = BOARD.get(tuple(coords))
    if isinstance(cell,Figure) and cell.color == color:
        return True
    return False
#------Kings section---------------------------------------------------
def get_king_coords(color):
    for cell in BOARD:
        if isinstance(BOARD.get(cell),King):
            if BOARD.get(cell).color == color:
                return cell

def is_king_in_check(king_color: str, board = BOARD):
    king_position = get_king_coords(king_color)
    #Loop thru cells
    for coords, figure in board.items():
        #If cell is figure and figure is not same color as king
        if (figure != None) and (figure.color != king_color):
            #Get possible moves of the figure
            possible_moves = figure.get_possible_moves(coords, board)
            #If king is in possible moves of the figure
            if king_position in possible_moves:
                return True
    return False

#Return true, if king is going to be in check
def is_going_to_be_check(king_color: str, new_king_coords, board):
    #Get old coords of king
    old_king_coords = get_king_coords(king_color)
    #Get copy of board
    shadow_board = board.copy()
    shadow_board[old_king_coords] = None
    shadow_board[new_king_coords] = King(king_color)
    #Loop thru cells
    for cell in shadow_board:
        figure = shadow_board.get(cell)
        #If cell is figure and figure is not same color as king
        if isinstance(figure, Figure) and figure.color != king_color:
            #If coords of king is in possible moves of the figure
            if new_king_coords in figure.get_possible_moves(cell, shadow_board):
                return True
    return False

#Function that finds figure which checks king argument and returns it's coords
def get_checking_figure_coords(king_color,board):
    king = get_king_coords(king_color)
    for cell in board:
        figure = board.get(cell)
        #Is enemy figure
        if isinstance(figure, Figure) and figure.color != king_color:
            #Is checking king
            for move in figure.get_possible_moves(cell, board):
                if move == king:
                    return cell
    return None

def check_for_checkmate():
    for king_color in ["white", "black"]:
        #If looped king is checked
        if is_king_in_check(king_color):
            moves = []
            king_coords = get_king_coords(king_color)
            checking_figure_coords = get_checking_figure_coords(king_color,BOARD)
            checking_figure = BOARD.get(checking_figure_coords)
            checking_figure_moves = checking_figure.get_possible_moves(checking_figure_coords,BOARD)
            #Count valid moves of all figures of same color
            for cell in BOARD:
                figure = BOARD.get(cell)
                if isinstance(figure, Figure) and figure.color == king_color:
                    valid_moves = []
                    valid_moves = get_valid_moves(figure,cell)
                    moves.append(valid_moves)
            if all(not moves for moves in moves):
                END = True
                draw_ending_screen(COLOR_TURN)
#----------------------------------------------------------------------

def get_valid_moves(SELECTED_FIGURE: Figure, SELECTED_FIGURE_COORDS):
    moves = []
    moves = (SELECTED_FIGURE.get_possible_moves(SELECTED_FIGURE_COORDS,BOARD)).copy()
    #If TURN king is in check
    if is_king_in_check(COLOR_TURN):
        moves = []
        checking_figure_coords = get_checking_figure_coords(COLOR_TURN,BOARD)
        checking_figure = BOARD.get(checking_figure_coords)
        checking_figure_moves = checking_figure.get_possible_moves(checking_figure_coords,BOARD)
        #Check if selected figure can block check
        for friendly_move in SELECTED_FIGURE.get_possible_moves(SELECTED_FIGURE_COORDS,BOARD):
            if friendly_move in checking_figure_moves:
                shadow_board = BOARD.copy()
                shadow_board[friendly_move] = SELECTED_FIGURE
                if not is_going_to_be_check(COLOR_TURN,get_king_coords(COLOR_TURN),shadow_board):
                    moves.append(friendly_move)
        #Check for special pawn attack
        if isinstance(SELECTED_FIGURE,Pawn):
            if checking_figure_coords in SELECTED_FIGURE.get_all_special_attacks(SELECTED_FIGURE_COORDS,BOARD):
                moves.append(checking_figure_coords)
        #If figure can takeout checking figure
        elif checking_figure_coords in SELECTED_FIGURE.get_possible_moves(SELECTED_FIGURE_COORDS,BOARD):
            moves.append(checking_figure_coords)
        #Simulate all possible moves
        for move in moves.copy():
            shadow_board = BOARD.copy()
            shadow_board[move] = SELECTED_FIGURE
            shadow_board[SELECTED_FIGURE_COORDS] = None
            if get_checking_figure_coords(COLOR_TURN,shadow_board) != None:
                moves.remove(move)
        #If possible moves of selected figure is in checking figure moves
        if isinstance(SELECTED_FIGURE,King):
            for move in SELECTED_FIGURE.get_possible_moves(SELECTED_FIGURE_COORDS,BOARD):
                print("2",move)
                shadow_board = BOARD.copy()
                shadow_board[SELECTED_FIGURE_COORDS] = None
                shadow_board[move] = SELECTED_FIGURE
                if is_king_in_check(COLOR_TURN,shadow_board):
                    print("Appending move")
                    moves.append(move)
    return list(moves)

def show_possible_moves(valid_moves):
    for pos in valid_moves:
        temp_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        temp_surface.fill((255, 0, 0, 75))
        screen.blit(temp_surface, (pos[1] * CELL_SIZE, (7 - pos[0]) * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def highlight_selected_figure(bool,coords):
    if SELECTED_FIGURE != None:
        if bool == True:
            temp_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            temp_surface.fill((0, 255, 0, 75))
            screen.blit(temp_surface, (coords[1] * CELL_SIZE, (7 - coords[0]) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        else:
            reset_color_cell(coords)
            set_figure(screen,BOARD.get(coords),coords)

def hide_possible_moves():
    for pos in get_valid_moves(SELECTED_FIGURE,SELECTED_FIGURE_COORDS).copy():
        if BOARD[(pos[0],pos[1])] == None:
            reset_color_cell((pos[0],pos[1]))
        else:
            reset_color_cell((pos[0],pos[1]))
            set_figure(screen,BOARD[(pos[0],pos[1])],(pos[0],pos[1]))

def draw_board():
    for row in range(8):
        for col in range(8):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            if (row + col) % 2 != 0:
                pygame.draw.rect(screen, "white", (x, y, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, "gray30", (x, y, CELL_SIZE, CELL_SIZE))

def switch_turn():
    global COLOR_TURN
    if COLOR_TURN == "white":
        COLOR_TURN = "black"
    else:
        COLOR_TURN = "white"

pygame.init()
screen = pygame.display.set_mode((RESOLUTION))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()
screen.fill("black")
draw_board()
init_board(screen)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            # Převrácení osy Y a X(změna znaménka)
            y = RESOLUTION[0] - y
            clicked_cell_coords = (y // CELL_SIZE, x // CELL_SIZE)
            clicked_figure = BOARD.get(clicked_cell_coords)
            if (SELECTED_FIGURE == None) and (clicked_figure != None):
                if (COLOR_TURN == clicked_figure.color):
                    SELECTED_FIGURE = BOARD.get(clicked_cell_coords)
                    SELECTED_FIGURE_COORDS = clicked_cell_coords
                    show_possible_moves(get_valid_moves(SELECTED_FIGURE,SELECTED_FIGURE_COORDS).copy())
                    highlight_selected_figure(True,SELECTED_FIGURE_COORDS)
            elif (SELECTED_FIGURE != None) and (clicked_cell_coords != SELECTED_FIGURE_COORDS):
                if clicked_cell_coords in get_valid_moves(SELECTED_FIGURE, SELECTED_FIGURE_COORDS):                    
                    hide_possible_moves()
                    reset_color_cell(clicked_cell_coords)
                    highlight_selected_figure(False,SELECTED_FIGURE_COORDS)
                    set_figure(screen, SELECTED_FIGURE, clicked_cell_coords)
                    BOARD[SELECTED_FIGURE_COORDS] = None
                    BOARD[clicked_cell_coords] = SELECTED_FIGURE
                    reset_color_cell(SELECTED_FIGURE_COORDS)
                    SELECTED_FIGURE = None
                    SELECTED_FIGURE_COORDS = None
                    switch_turn()
                    check_for_checkmate()
            elif (clicked_cell_coords == SELECTED_FIGURE_COORDS):
                highlight_selected_figure(False,SELECTED_FIGURE_COORDS)
                hide_possible_moves()
                reset_selection()
    pygame.display.update()
    pygame.display.flip()
    pygame.display
    clock.tick(60)
pygame.quit()