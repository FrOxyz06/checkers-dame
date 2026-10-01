import unittest
from game import Game, Piece

class GameTests(unittest.TestCase):
    def position(self, pieces, turn="black"):
        game = Game()
        game.board = {pos: Piece(color, king) for pos, color, king in pieces}
        game.turn = turn
        return game

    def test_initial_layout(self):
        game = Game()
        self.assertEqual(len(game.board), 30)
        self.assertEqual(sum(p.color == "black" for p in game.board.values()), 15)
        self.assertTrue(all((row + col) % 2 for row, col in game.board))
        self.assertEqual(game.legal_moves((2, 1)), [(3, 0), (3, 2)])

    def test_moves_alternate_and_reject_wrong_turn(self):
        game = Game()
        self.assertFalse(game.move((7, 0), (6, 1)))
        self.assertTrue(game.move((2, 1), (3, 2)))
        self.assertEqual(game.turn, "white")
        self.assertTrue(game.move((7, 0), (6, 1)))
        self.assertEqual(game.turn, "black")

    def test_invalid_moves_preserve_board(self):
        game = Game()
        before = dict(game.board)
        for target in [(-1, 0), (10, 10), (2, 3), (1, 0), (4, 3)]:
            self.assertFalse(game.move((2, 1), target))
        self.assertEqual(game.board, before)

    def test_capture_removes_opponent_and_is_required(self):
        game = self.position([((2, 1), "black", False), ((2, 5), "black", False),
                              ((3, 2), "white", False), ((8, 7), "white", False)])
        self.assertEqual(game.legal_moves((2, 5)), [])
        self.assertEqual(game.legal_moves((2, 1)), [(4, 3)])
        self.assertTrue(game.move((2, 1), (4, 3)))
        self.assertNotIn((3, 2), game.board)
        self.assertEqual(game.turn, "white")

    def test_cannot_capture_own_piece(self):
        game = self.position([((2, 1), "black", False), ((3, 2), "black", False), ((8, 7), "white", False)])
        self.assertFalse(game.move((2, 1), (4, 3)))

    def test_capture_chain_uses_same_piece(self):
        game = self.position([((2, 1), "black", False), ((2, 7), "black", False),
                              ((3, 2), "white", False), ((5, 4), "white", False)])
        self.assertTrue(game.move((2, 1), (4, 3)))
        self.assertEqual(game.forced_piece, (4, 3))
        self.assertEqual(game.turn, "black")
        self.assertFalse(game.move((2, 7), (3, 8)))
        self.assertTrue(game.move((4, 3), (6, 5)))
        self.assertEqual(game.winner, "black")

    def test_promotion_and_king_backward_moves(self):
        game = self.position([((8, 1), "black", False), ((5, 8), "white", False)])
        self.assertTrue(game.move((8, 1), (9, 2)))
        self.assertTrue(game.board[(9, 2)].king)
        self.assertTrue(game.move((5, 8), (4, 7)))
        self.assertTrue(game.move((9, 2), (8, 1)))

    def test_white_capture_and_promotion_ends_turn(self):
        game = self.position([((2, 3), "white", False), ((1, 2), "black", False),
                              ((1, 0), "black", False)], "white")
        self.assertTrue(game.move((2, 3), (0, 1)))
        self.assertTrue(game.board[(0, 1)].king)
        self.assertIsNone(game.forced_piece)
        self.assertEqual(game.turn, "black")

    def test_blocked_opponent_loses(self):
        game = self.position([((2, 1), "black", False), ((0, 1), "white", False)])
        self.assertTrue(game.move((2, 1), (3, 2)))
        self.assertEqual(game.winner, "black")
        self.assertFalse(game.move((0, 1), (1, 0)))

if __name__ == "__main__":
    unittest.main()
