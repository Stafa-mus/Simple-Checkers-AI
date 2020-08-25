from easyAI import TwoPlayersGame, AI_Player, Negamax
from easyAI.Player import Human_Player
import pygame

class GameController(TwoPlayersGame):
    '''
    Human player is player 1 (X) The human player moves from bottom to top
    AI player is player 2 (Y) The AI player moves from top to bottom
    '''

    def __init__(self, players):
        self.players = players
        self.nplayer = 1
        self.board = initialize_board()

    def possible_moves(self):
        if self.nplayer == 1: #it is the human's turn
            return get_all_possible_moves('x', self.board)
        elif self.nplayer == 2: #it is the AI player's turn
            return get_all_possible_moves('y', self.board)

    def make_move(self, move):
        self.board = make_move(move, self.board)

    def is_over(self):
        if len(get_all_possible_moves('x', self.board)) == 0:
            return True
        if len(get_all_possible_moves('y', self.board)) == 0:
            return True
        if not 'x' in self.board and not 'X' in self.board:
            return True
        if not 'y' in self.board and not 'Y' in self.board:
            return True
        return False

    def show(self):
        print_board(self.board)

    def scoring(self):
        score = 0
        if self.nplayer == 1:#it is x's turn (human)
            for x in range(0, 100):
                if self.board[x] == 'x':
                    score += 5
                if self.board[x] == 'X':
                    score += 10
                if self.board[x] == 'y':
                    score -= 2
                if self.board[x] == 'Y':
                    score -= 3
        elif self.nplayer == 2:
            for x in range(0, 100):
                if self.board[x] == 'y':
                    score += 5
                if self.board[x] == 'Y':
                    score += 10
                if self.board[x] == 'x':
                    score -= 2
                if self.board[x] == 'X':
                    score -= 3
        return score

def print_board(board):
    end_row = [9, 19, 29, 39, 49, 59, 69, 79, 89, 99]
    x = 0
    current_line = ''
    print('')
    print('  0  1  2  3  4  5  6  7  8  9')
    row = 0
    while x < 100:
        current_line += str(board[x]) + '  '
        if x in end_row:
            print(str(row) + ' ' + current_line)
            row += 1
            current_line = ''
        x += 1
    print('')

def initialize_board():
    board = []
    for x in range(0, 100):
        board.append('A')  # start with all as not valid
    row = 0
    x = 0
    end_row = [9, 19, 29, 39, 49, 59, 69, 79, 89, 99]
    while x < 100:
        if row == 0:
            if not x % 2 == 0:
                board[x] = '-'
        elif row % 2 == 0:
            if not x % 2 == 0:
                board[x] = '-'
        elif not row % 2 == 0:
            if x % 2 == 0:
                board[x] = '-'

        if x in end_row:
            row += 1
        x += 1
    for x in range(0, 39):
        if board[x] == '-':
            board[x] = 'y'
    for x in range(99, 60, -1):
        if board[x] == '-':
            board[x] = 'x'
    return board

def get_all_possible_moves(turn, board):
    capturing_moves = []
    non_capturing_moves = []
    if turn == 'x':
        turn = ['x', 'X']
    if turn == 'y':
        turn = ['y', 'Y']
    for position in range(0, 100):
        if board[position] in turn:
            cm = get_capturing_moves_2(position, board)
            if len(cm) == 0:
                pass
            else:
                for m in cm:
                    capturing_moves.append(m)
            ncm = get_non_capturing_moves(position, board)
            if len(ncm) == 0:
                pass
            else:
                for m in ncm:
                    non_capturing_moves.append(m)
    if len(capturing_moves) > 0:
        return capturing_moves
    all_possible_moves = capturing_moves + non_capturing_moves
    return all_possible_moves

def get_capturing_moves_2(cell_number, board):  # is able to return multiple captures
    moves = []
    p = cell_number
    if board[p] == 'x':
        tl = get_top_left(p)
        if not tl is None:
            tl_of_tl = get_top_left(tl)
            if not tl_of_tl is None:
                if board[tl_of_tl] == '-' and board[tl] in ['y', 'Y']:
                    moves.append([p, tl_of_tl])
        tr = get_top_right(p)
        if not tr is None:
            tr_of_tr = get_top_right(tr)
            if not tr_of_tr is None:
                if board[tr_of_tr] == '-' and board[tr] in ['y', 'Y']:
                    moves.append([p, tr_of_tr])
    elif board[p] == 'y':
        bl = get_bottom_left(p)
        if not bl is None:
            bl_of_bl = get_bottom_left(bl)
            if not bl_of_bl is None:
                if board[bl_of_bl] == '-' and board[bl] in ['x', 'X']:
                    moves.append([p, bl_of_bl])
        br = get_bottom_right(p)
        if not br is None:
            br_of_br = get_bottom_right(br)
            if not br_of_br is None:
                if board[br_of_br] == '-' and board[br] in ['x', 'X']:
                    moves.append([p, br_of_br])
    elif board[p] == 'X':
        brd = get_bottom_right_diagonal(p)
        bld = get_bottom_left_diagonal(p)
        trd = get_top_right_diagonal(p)
        tld = get_top_left_diagonal(p)
        for b in brd:
            if board[b] in ['y', 'Y']:
                if not get_bottom_right(b) is None:
                    if board[get_bottom_right(b)] in ['-']:
                        if is_empty_range(p, b, 'br', board):
                            moves.append([p, get_bottom_right(b)])
        for b in bld:
            if board[b] in ['y', 'Y']:
                if not get_bottom_left(b) is None:
                    if board[get_bottom_left(b)] in ['-']:
                        if is_empty_range(p, b, 'bl', board):
                            moves.append([p, get_bottom_left(b)])
        for b in trd:
            if board[b] in ['y', 'Y']:
                if not get_top_right(b) is None:
                    if board[get_top_right(b)] in ['-']:
                        if is_empty_range(p, b, 'tr', board):
                            moves.append([p, get_top_right(b)])
        for b in tld:
            if board[b] in ['y', 'Y']:
                if not get_top_left(b) is None:
                    if board[get_top_left(b)] in ['-']:
                        if is_empty_range(p, b, 'tl', board):
                            moves.append([p, get_top_left(b)])
    elif board[p] == 'Y':
        brd = get_bottom_right_diagonal(p)
        bld = get_bottom_left_diagonal(p)
        trd = get_top_right_diagonal(p)
        tld = get_top_left_diagonal(p)
        for b in brd:
            if board[b] in ['x', 'X']:
                if not get_bottom_right(b) is None:
                    if board[get_bottom_right(b)] in ['-']:
                        if is_empty_range(p, b, 'br', board):
                            moves.append([p, get_bottom_right(b)])
        for b in bld:
            if board[b] in ['x', 'X']:
                if not get_bottom_left(b) is None:
                    if board[get_bottom_left(b)] in ['-']:
                        if is_empty_range(p, b, 'bl', board):
                            moves.append([p, get_bottom_left(b)])
        for b in trd:
            if board[b] in ['x', 'X']:
                if not get_top_right(b) is None:
                    if board[get_top_right(b)] in ['-']:
                        if is_empty_range(p, b, 'tr', board):
                            moves.append([p, get_top_right(b)])
        for b in tld:
            if board[b] in ['x', 'X']:
                if not get_top_left(b) is None:
                    if board[get_top_left(b)] in ['-']:
                        if is_empty_range(p, b, 'tl', board):
                            moves.append([p, get_top_left(b)])
    for move in moves:
        board_copy = make_move(move, board)
        extra_moves = get_capturing_moves_2(move[1], board_copy)
        while len(extra_moves) > 0:
            move.append(extra_moves[0][1])
            board_copy = make_move([move[len(move) - 2], move[len(move) - 1]], board_copy)
            extra_moves = get_capturing_moves_2(move[len(move) - 1], board_copy)
    return moves

def get_non_capturing_moves(cell_number, board):
    moves = []
    p = cell_number
    if board[p] == 'x':
        tl = get_top_left(p)
        if not tl is None:
            if board[tl] == '-':
                moves.append([p, tl])
        tr = get_top_right(p)
        if not tr is None:
            if board[tr] == '-':
                moves.append([p, tr])
    elif board[p] == 'y':
        bl = get_bottom_left(p)
        if not bl is None:
            if board[bl] == '-':
                moves.append([p, bl])
        br = get_bottom_right(p)
        if not br is None:
            if board[br] == '-':
                moves.append([p, br])
    elif board[p] in ['X', 'Y']:
        br = get_bottom_right(p)
        bl = get_bottom_left(p)
        tr = get_top_right(p)
        tl = get_top_left(p)
        if not br is None and board[br] == '-':
            moves.append([p, br])
        if not bl is None and  board[bl] == '-':
            moves.append([p, bl])
        if not tr is None and board[tr] == '-':
            moves.append([p, tr])
        if not tl is None and board[tl] == '-':
            moves.append([p, tl])
    return moves

def get_bottom_right(cell_number):
    end_row = [9, 19, 29, 39, 49, 59, 69, 79, 89, 99]
    if cell_number < 90 and not cell_number in end_row:
        return cell_number + 11
    else:
        return None

def get_bottom_left( cell_number):
    start_row = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
    if cell_number < 90 and not cell_number in start_row:
        return cell_number + 9
    else:
        return None

def get_top_left(cell_number):
    start_row = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
    if cell_number > 9 and not cell_number in start_row:
        return cell_number - 11

def get_top_right(cell_number):
    end_row = [9, 19, 29, 39, 49, 59, 69, 79, 89, 99]
    if cell_number > 9 and not cell_number in end_row:
        return cell_number - 9

def get_bottom_right_diagonal(cell_number):
    diagonal = []
    c = cell_number
    while not get_bottom_right(c) is None and c < 90:
        diagonal.append(get_bottom_right(c))
        c = get_bottom_right(c)
    return diagonal

def get_bottom_left_diagonal(cell_number):
    diagonal = []
    c = cell_number
    while not get_bottom_left(c) is None and c < 90:
        diagonal.append(get_bottom_left(c))
        c = get_bottom_left(c)
    return diagonal

def get_top_right_diagonal(cell_number):
    diagonal = []
    c = cell_number
    while not get_top_right(c) is None and c > 9:
        diagonal.append(get_top_right(c))
        c = get_top_right(c)
    return diagonal

def get_top_left_diagonal(cell_number):
    diagonal = []
    c = cell_number
    while not get_top_left(c) is None and c > 9:
        diagonal.append(get_top_left(c))
        c = get_top_left(c)
    return diagonal

def is_empty_range(first_position, second_position, direction, board):
    fp = first_position
    sp = second_position
    dir = direction
    if fp == sp:
        return True
    else:
        if dir == 'tr':
            while not fp == sp and not get_top_right(fp) == sp:
                fp = get_top_right(fp)
                if not board[fp] == '-':
                    return False
        elif dir == 'tl':
            while not fp == sp and not get_top_left(fp) == sp:
                fp = get_top_left(fp)
                if not board[fp] == '-':
                    return False
        elif dir == 'br':
            while not fp == sp and not get_bottom_right(fp) == sp:
                fp = get_bottom_right(fp)
                if not board[fp] == '-':
                    return False
        elif dir == 'bl':
            while not fp == sp and not get_bottom_left(fp) == sp:
                fp = get_bottom_left(fp)
                if not board[fp] == '-':
                    return False
        return True

def make_move(move, board):
    b = copy_board(board)
    for i in range(0, len(move)-1):
        cp = get_captured_piece(move[i], move[i+1], b)
        if not cp is None:
            b[cp] = '-'
            b[move[i+1]] = b[move[i]]
            b[move[i]] = '-'
            for index in range(0, 10):
                if b[index] == 'x':
                    b[index] = 'X'
            for index in range(90, 100):
                if b[index] == 'y':
                    b[index] = 'Y'
        else:
            b[move[i+1]] = b[move[i]]
            b[move[i]] = '-'
            for index in range(0, 10):
                if b[index] == 'x':
                    b[index] = 'X'
            for index in range(90, 100):
                if b[index] == 'y':
                    b[index] = 'Y'
    for x in range(0, 10):
        if b[x] == 'x':
            b[x] = 'X'
    for x in range(90, 100):
        if b[x] == 'y':
            b[x] = 'Y'
    return b

def copy_board(board):
    b = []
    for a in board:
        b.append(a)
    return b

def get_captured_piece(first_move, destination, board):
    captured_piece = None
    if first_move == destination:
        return None
    if destination in [get_bottom_right(first_move), get_bottom_left(first_move), get_top_right(first_move), get_top_left(first_move)]:
        return None
    else:
        if not get_bottom_right(first_move) is None:
            if destination == get_bottom_right(get_bottom_right(first_move)):
                return get_bottom_right(first_move)
        if not get_bottom_left(first_move) is None:
            if destination == get_bottom_left(get_bottom_left(first_move)):
                return get_bottom_left(first_move)
        if not get_top_right(first_move) is None:
            if destination == get_top_right(get_top_right(first_move)):
                return get_top_right(first_move)
        if not get_top_left(first_move) is None:
            if destination == get_top_left(get_top_left(first_move)):
                return get_top_left(first_move)
        if board[first_move] in ['X', 'Y']:
            brd = get_bottom_right_diagonal(first_move)
            bld = get_bottom_left_diagonal(first_move)
            trd = get_top_right_diagonal(first_move)
            tld = get_top_left_diagonal(first_move)
            if not brd is None:
                if destination in brd:
                    return get_top_left(destination)
            if not bld is None:
                if destination in bld:
                    return get_top_right(destination)
            if not trd is None:
                if destination in trd:
                    return get_bottom_left(destination)
            if not tld is None:
                if destination in tld:
                    return get_bottom_right(destination)
    return None

if __name__ == "__main__":
    pygame.init()
    GameController([Human_Player(), AI_Player(Negamax(6))]).play()