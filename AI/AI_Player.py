# -*- coding: utf-8 -*-

#TODO: Set strategie
class Strategy():
    def __init__(self,playeur_max,depth_max,weighting_nb_stroke,weighting_nb_pawns,weighting_position):
        self.playeur_max = playeur_max
        self.depth_max = depth_max
        self.weighting_nb_pawns = weighting_nb_pawns
        self.weighting_nb_stroke = weighting_nb_stroke
        self.weighting_position = weighting_position
    
    @staticmethod()
    def evaluate_nb_pawns(board,playeur):
        playeur_pawns_nb = board.get_black_pawns_nb() if playeur.color == False else board.get_black_pawns_nb()
        otherPly_pawns_nb =  board.get_black_pawns_nb() if playeur.color == True else board.get_black_pawns_nb()
        return playeur_pawns_nb - otherPly_pawns_nb
    
    @staticmethod()
    def evaluate_nb_stroke():
        return
    
    @staticmethod()
    def evaluate_position():
        return
    
    def min_max_alp_bet():
        return
        
