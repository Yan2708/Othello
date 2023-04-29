import Game.Rules as Rules
from math import inf
import copy
import sys
from GUI.utils import Utils


# TODO: Set strategie
class Strategy():

    def __init__(self, player_max, depth_max, weighting_nb_stroke, weighting_nb_pawns, weighting_position):
        self.player_max = player_max
        self.depth_max = depth_max
        self.weighting_nb_pawns = weighting_nb_pawns
        self.weighting_nb_stroke = weighting_nb_stroke
        self.weighting_position = weighting_position

    def set_weighting_nb_pawns(self, value):
        self.weighting_nb_pawns = value

    def set_weighting_nb_stroke(self, value):
        self.weighting_nb_stroke = value

    def set_weighting_position(self, value):
        self.weighting_position = value

    @staticmethod
    def evaluate_nb_pawns(board, player):
        return board.get_pawns_nb(player) - board.get_pawns_nb(not player)

    @staticmethod
    def evaluate_nb_strokes(board, player):
        return len(Rules.movespossible(board, player)) - len(Rules.movespossible(board, not player))

    @staticmethod
    def evaluate_strenght_position(board, player):
        Sum_strenght = 0
        for x in range(8):
            for y in range(8):
                current = (x, y)
                if Rules.is_in_corner(current):
                    Sum_strenght += 10 if board.status[x][y] == player else -10
                elif Rules.checkadjacent_for_corner(current):
                    Sum_strenght += -5 if board.status[x][y] == player else 5
                elif Rules.is_in_border(current):
                    Sum_strenght += 3 if board.status[x][y] == player else -3
                else:
                    Sum_strenght += 1 if board.status[x][y] == player else -1
        return Sum_strenght

    def global_evaluate(self, board, player):
        return Strategy.evaluate_nb_strokes(board, player) * self.weighting_nb_stroke + \
            Strategy.evaluate_nb_pawns(board, player) * self.weighting_nb_pawns + \
            Strategy.evaluate_strenght_position(board, player) * self.weighting_position

    def alpha_beta_search(self, board, alpha, beta, current_player, depth):
        if depth == 0 or board.isfull():
            return self.global_evaluate(board, current_player)

        m = -inf if current_player == self.player_max else inf
        update_alpha_beta = max if current_player == self.player_max else min

        for move in Rules.movespossible(board, current_player):
            board.simulate_stroke(move, current_player)
            val = self.alpha_beta_search(board, alpha, beta, not current_player, depth - 1)
            board.undo_move(move)
            m = update_alpha_beta(m, val)

            if current_player == self.player_max:
                alpha = max(alpha, m)

            else:
                beta = min(beta, m)

            if beta <= alpha:
                break
        return m

    @Utils.timer
    def get_best_move(self, state):
        best_score = -inf
        best_move = None
        fake_state = copy.deepcopy(state)
        for pos in Rules.movespossible(fake_state, self.player_max):
            fake_state.simulate_stroke(pos, self.player_max)
            score = self.alpha_beta_search(fake_state, -inf, inf, self.player_max, self.depth_max)
            fake_state.undo_move(pos)
            if score > best_score or (best_move is None and (score == -inf or score == inf)):
                best_score = score
                best_move = pos
        return best_move
