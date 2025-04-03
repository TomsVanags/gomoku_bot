import random

# Minimax with Alpha-Beta Pruning algorithm
def minimax(board, depth, maximizing_player, alpha, beta):
    # Example for minimax, extend it according to your evaluation function.
    if depth == 0 or is_game_over(board):
        return evaluate_board(board), None  # Return evaluation and no move.
    
    legal_moves = get_legal_moves(board)
    
    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in legal_moves:
            new_board = apply_move(board, move, 1)  # Assuming 1 for 'black'
            eval, _ = minimax(new_board, depth - 1, False, alpha, beta)  # Unpack evaluation and move
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move  # Return evaluation and best move
    
    else:
        min_eval = float('inf')
        best_move = None
        for move in legal_moves:
            new_board = apply_move(board, move, 2)  # Assuming 2 for 'white'
            eval, _ = minimax(new_board, depth - 1, True, alpha, beta)  # Unpack evaluation and move
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move  # Return evaluation and best move


# Check if the game is over (either win or draw)
def is_game_over(board):
    # Check for winning condition
    for x in range(16):
        for y in range(16):
            if board[y][x] != 0 and check_win(board, x, y, board[y][x]):
                return True
    
    # Check for draw condition (board is full with no winner)
    for x in range(16):
        for y in range(16):
            if board[y][x] == 0:
                return False  # There's still an empty spot, game continues
    
    return True  # All spots filled, it's a draw

# Check if a player has won from a starting point (x, y)
def check_win(board, x, y, player):
    # Check horizontally, vertically, and diagonally for 5 consecutive stones
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Right, Down, Down-Right, Down-Left
    for dx, dy in directions:
        count = 1
        for i in range(1, 5):
            nx, ny = x + i * dx, y + i * dy
            if 0 <= nx < 16 and 0 <= ny < 16 and board[ny][nx] == player:
                count += 1
            else:
                break
        for i in range(1, 5):
            nx, ny = x - i * dx, y - i * dy
            if 0 <= nx < 16 and 0 <= ny < 16 and board[ny][nx] == player:
                count += 1
            else:
                break
        if count >= 5:
            return True
    return False

# Evaluate the board state
def evaluate_board(board):
    # Basic evaluation: +1 for black, -1 for white stones on the board
    black_score = 0
    white_score = 0
    
    for x in range(16):
        for y in range(16):
            if board[y][x] == 1:
                black_score += 1
            elif board[y][x] == 2:
                white_score += 1
    
    return black_score - white_score  # Return the difference (black - white)

# Get all empty cells on the board (legal moves)
def get_legal_moves(board):
    moves = []
    for x in range(16):
        for y in range(16):
            if board[y][x] == 0:  # Empty cell
                moves.append((x, y))
    return moves

# Apply a move to the board (simulate a move)
def apply_move(board, move, player):
    new_board = [row[:] for row in board]  # Create a copy of the board
    x, y = move
    new_board[y][x] = player
    return new_board

