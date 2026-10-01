"""Rules for a small, local two-player checkers variant."""
from dataclasses import dataclass

SIZE = 10

@dataclass
class Piece:
    color: str
    king: bool = False

class Game:
    def __init__(self):
        self.board = {
            (row, col): Piece("black" if row < 3 else "white")
            for row in range(SIZE) for col in range(SIZE)
            if (row + col) % 2 == 1 and (row < 3 or row > 6)
        }
        self.turn = "black"
        self.forced_piece = None
        self.winner = None

    def _moves(self, position, capture):
        piece = self.board.get(position)
        if piece is None:
            return []
        directions = (-1, 1) if piece.king else ((1,) if piece.color == "black" else (-1,))
        row, col = position
        distance = 2 if capture else 1
        moves = []
        for direction in directions:
            for horizontal in (-1, 1):
                target = (row + direction * distance, col + horizontal * distance)
                if not all(0 <= value < SIZE for value in target) or target in self.board:
                    continue
                if capture:
                    middle = self.board.get((row + direction, col + horizontal))
                    if middle is None or middle.color == piece.color:
                        continue
                moves.append(target)
        return moves

    def legal_moves(self, position):
        piece = self.board.get(position)
        if self.winner or piece is None or piece.color != self.turn:
            return []
        if self.forced_piece is not None and position != self.forced_piece:
            return []
        captures = self._moves(position, True)
        if self.forced_piece is not None:
            return captures
        if any(self._moves(pos, True) for pos, other in self.board.items() if other.color == self.turn):
            return captures
        return self._moves(position, False)

    def move(self, source, target):
        if target not in self.legal_moves(source):
            return False
        piece = self.board.pop(source)
        captured = abs(target[0] - source[0]) == 2
        if captured:
            del self.board[((source[0] + target[0]) // 2, (source[1] + target[1]) // 2)]
        self.board[target] = piece
        promoted = not piece.king and target[0] == (SIZE - 1 if piece.color == "black" else 0)
        if promoted:
            piece.king = True
        if captured and not promoted and self._moves(target, True):
            self.forced_piece = target
            return True
        self.forced_piece = None
        self.turn = "white" if self.turn == "black" else "black"
        if not any(self.legal_moves(pos) for pos in self.board):
            self.winner = piece.color
        return True
