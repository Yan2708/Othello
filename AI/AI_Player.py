import Game.Rules as Rules
from math import inf
import copy
import sys
from GUI.utils import Utils
import time


# TODO: Set strategie
class Strategy():
    BOARD_SCORE = [
        [50, -50, 10, 10, 10, 10, -50, 50],
        [-50, -50, 4, 4, 4, 4, -50, -50],
        [10, 4, 1, 1, 1, 1, 4, 10],
        [10, 4, 1, 1, 1, 1, 4, 10],
        [10, 4, 1, 1, 1, 1, 4, 10],
        [10, 4, 1, 1, 1, 1, 4, 10],
        [-50, -50, 4, 4, 4, 4, -50, -50],
        [50, -50, 10, 10, 10, 10, -50, 50],
    ]
    def __init__(self, player_max, depth_max, weighting_nb_stroke, weighting_nb_pawns, weighting_position):
        self.player_max = player_max
        self.depth_max = depth_max
        self.weighting_nb_pawns = weighting_nb_pawns
        self.weighting_nb_stroke = weighting_nb_stroke
        self.weighting_position = weighting_position
        self.transpoTable = {}

    def set_weighting_nb_pawns(self, value):
        self.weighting_nb_pawns = value

    def set_weighting_nb_stroke(self, value):
        self.weighting_nb_stroke = value

    def set_weighting_position(self, value):
        self.weighting_position = value
        
    # Usefull to optimisation
    def getHashBoard(self, board):
        return hash(str(board))

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
                Sum_strenght += Strategy.BOARD_SCORE[x][y] if board.status[x][y] == player else -Strategy.BOARD_SCORE[x][y]
        return Sum_strenght

    def global_evaluate(self, board, player):
        return Strategy.evaluate_nb_strokes(board, player) * self.weighting_nb_stroke + \
            Strategy.evaluate_nb_pawns(board, player) * self.weighting_nb_pawns + \
            Strategy.evaluate_strenght_position(board, player) * self.weighting_position
      
    @staticmethod
    def estimate_move_quality(board, move, player):
        toFlip = board.change(move[0], move[1], player)
        quality = board.get_pawns_nb(player) - board.get_pawns_nb(not player)
        board.undo_change(move[0],move[1],toFlip)
        return quality

    def alpha_beta_search(self, board, alpha, beta, current_player, depth):
        
        if depth == 0 or board.isfull() or len(Rules.movespossible(board, current_player)) == 0:
            board_hash_key = self.getHashBoard(board)
            if board_hash_key in self.transpoTable:
                return self.transpoTable[board_hash_key]
            else:
                value_eval = self.global_evaluate(board, current_player)
                self.transpoTable[board_hash_key] = value_eval
                return value_eval
            
        m = -inf if current_player == self.player_max else inf
        update_alpha_beta = max if current_player == self.player_max else min
        
        for move in Rules.movespossible(board, current_player):
            toFlip = board.change(move[0], move[1], current_player)
            val = self.alpha_beta_search(board, alpha, beta, not current_player, depth - 1)
            board.undo_change(move[0], move[1],toFlip)
            m = update_alpha_beta(m, val)
            
            if current_player == self.player_max:
                alpha = max(alpha, m)                
            else:
                beta = min(beta, m)

            if beta <= alpha:
                break
            
        return m

    @Utils.timer
    def get_best_move(self, state, time_limit):
        start_time = time.perf_counter()
        best_score = -inf
        best_move = None
        fake_state = copy.deepcopy(state)

        possible_moves = Rules.movespossible(fake_state, self.player_max)
        sorted_moves = sorted(possible_moves,
                              key=lambda move: Strategy.estimate_move_quality(fake_state, move, self.player_max),
                              reverse=True)

        for depth in range(1, self.depth_max + 1):
            for pos in sorted_moves:
                toFlip = fake_state.change(pos[0], pos[1], self.player_max)
                score = self.alpha_beta_search(fake_state, -inf, inf, self.player_max, depth)
                fake_state.undo_change(pos[0], pos[1],toFlip)
                print(pos,score,depth,"current best =>",best_move,best_score)
                if score > best_score or (best_move is None and (score == -inf or score == inf)):
                    best_score = score
                    best_move = pos
                if time.perf_counter() - start_time > time_limit:
                    break
        return best_move
