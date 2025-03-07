import math

WIN_PATTERNS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Lignes
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Colonnes
    (0, 4, 8), (2, 4, 6)              # Diagonales
]

def evaluate(board):
    """Retourne +10 si O gagne, -10 si X gagne, 0 sinon."""
    for a, b, c in WIN_PATTERNS:
        if board[a] == board[b] == board[c] and board[a] != 0:
            return 10 if board[a] == 1 else -10
    return 0

def minimax(board, isMax):
    """Renvoie le score optimal pour le joueur actuel."""
    score = evaluate(board)
    if score or 0 not in board:  # Fin de partie
        return score

    best = -math.inf if isMax else math.inf
    for i in range(9):
        if board[i] == 0:
            board[i] = 1 if isMax else -1
            best = max(best, minimax(board, not isMax)) if isMax else min(best, minimax(board, not isMax))
            board[i] = 0  # Annuler le coup
    return best

def best_move(board):
    """Trouve le meilleur coup pour X (-1)."""
    bestVal, move = math.inf, -1
    for i in range(9):
        if board[i] == 0:
            board[i] = -1
            moveVal = minimax(board, True)
            board[i] = 0
            if moveVal < bestVal:
                bestVal, move = moveVal, i
    return move

def print_board(board):
    """Affiche le plateau."""
    symbols = {1: 'O', -1: 'X', 0: ' '}
    print("\n".join(" | ".join(symbols[board[i]] for i in range(j, j+3)) for j in range(0, 9, 3)))
    print("-" * 9)

# Exemple d'utilisation
if __name__ == "__main__":
    board = [-1, 1, -1,  0, 1, 0,  0, 0, 0]
    print("Plateau actuel :")
    print_board(board)

    move = best_move(board)
    print("Meilleur coup pour X (-1) :", move)
