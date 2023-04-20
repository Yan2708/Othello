import Game.Rules as Rules
from math import inf
import copy
import sys
#TODO: Set strategie
class Strategy():
    def __init__(self,player_max,depth_max,weighting_nb_stroke,weighting_nb_pawns,weighting_position):
        self.player_max = player_max
        self.depth_max = depth_max
        self.weighting_nb_pawns = weighting_nb_pawns
        self.weighting_nb_stroke = weighting_nb_stroke
        self.weighting_position = weighting_position
    
    @staticmethod
    def evaluate_nb_pawns(board,player):
        player_pawns_nb = board.get_pawns_nb(False) if player == False else board.get_pawns_nb(True)
        otherPly_pawns_nb =  board.get_pawns_nb(False) if not player == False else board.get_pawns_nb(True)
        return player_pawns_nb - otherPly_pawns_nb
    
    @staticmethod
    def evaluate_nb_strokes(board,player):
        player_strokes_nb = len(Rules.movespossible(board, player))
        otherPly_strokes_nb = len(Rules.movespossible(board, not player))
        return player_strokes_nb - otherPly_strokes_nb
        return
    
    @staticmethod
    def evaluate_strenght_position(board,player):
        player_strenght = Strategy.check_strenght_position(board,player)
        otherPly_strenght = Strategy.check_strenght_position(board,not player)
        return player_strenght - otherPly_strenght
    
    #TODO: ajouter les points au bordures
    @staticmethod
    def check_strenght_position(board,player):
        Sum_strenght = 0
        for x in range(8):
            for y in range(8):
                current = (x,y)
                if board.status[x][y] == player:
                    if Rules.is_corner(current):
                        Sum_strenght += 10
                    elif Rules.checkadjacent_for_corner(current):
                        Sum_strenght -=5
                    else:
                        Sum_strenght += 1
                else:
                    if Rules.is_corner(current):
                        Sum_strenght -= 10
                    elif Rules.checkadjacent_for_corner(current):
                        Sum_strenght +=5
                    else:
                        Sum_strenght -= 1
        return Sum_strenght
    
    @staticmethod
    def simulate_stroke(board,move,player):
        fake_board = copy.deepcopy(board)
        fake_board.status[move[0]][move[1]] = player
        return fake_board
    

    def global_evaluate(self,board,player):
        strokes_nb_rate = Strategy.evaluate_nb_strokes(board,player)
        pawns_nb_rate = Strategy.evaluate_nb_pawns(board, player)
        strenght_rate = Strategy.evaluate_strenght_position(board, player)
        return strokes_nb_rate*self.weighting_nb_stroke+pawns_nb_rate*self.weighting_nb_pawns+strenght_rate*self.weighting_position
    
    def alpha_beta_search(self,board,alpha,beta,current_player,depth):
        
        if depth == 0 or board.isfull():
            return self.global_evaluate(board,current_player)
        
        #Max
        if current_player == self.player_max:
            m = -inf
            for move in Rules.movespossible(board,current_player):
                new_board = Strategy.simulate_stroke(board,move,current_player)
                val = self.alpha_beta_search(new_board,alpha,beta,not current_player,depth-1)
                m = max(m, val)
                alpha = max(alpha,val)
                if beta <= alpha :#and alpha != -inf:
                    break
            return m
        #Min
        else:
            m = inf
            for move in Rules.movespossible(board,current_player):
                new_board = Strategy.simulate_stroke(board,move,current_player)
                val = self.alpha_beta_search(new_board,alpha,beta,not current_player,depth-1)
                m = min(m, val)
                beta = min(beta,val)
                if beta <= alpha :#and beta != inf:
                    break
            return m
    
    def get_best_move(self,state):
        best_score = -inf
        best_move = None
        for pos in Rules.movespossible(state,self.player_max):
            fake_state = Strategy.simulate_stroke(state,pos,self.player_max)
            score = self.alpha_beta_search(fake_state, -inf, inf, self.player_max, self.depth_max)
            print(pos,"=>",score)
            if score > best_score:
                best_score = score
                best_move = pos
        return best_move
        
