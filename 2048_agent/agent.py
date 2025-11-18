"""
AI Agent for 2048 game using expectiminimax algorithm, alpha-beta pruning,
and heuristics functions.

Models adversarial agent with 3 level search depth and pruning for efficiency.

Able to achive consistent scores of 1024 and 2048.
"""

import random
import math

class ComputerAI(BaseAI):
    def getMove(self, grid):
        """ Returns a randomly selected cell if possible """
        cells = grid.getAvailableCells()
        return random.choice(cells) if cells else None

class IntelligentAgent():    
    def __init__(self):
        self.search_depth     = 3
        self.possibleNewTiles = [(2, 0.9), (4, 0.1)]
    
    def evaluate(self, state):
        """
        evaluation heuristic function to measure grid states
        sum of functions with assigned weights of importance.
        """
        f1 = len(state.getAvailableCells())
        f2 = math.log2(state.getMaxTile()) if state.getMaxTile() != 0 else 0  # use log to prevent skew of heuristic 
        f3 = self.monotonicity(state)
        f4 = self.smoothness(state)
        f5 = self.large_edge_tiles(state)
        f6 = self.snake_pattern(state)
        
        # weights for corresponding heuristic functions
        # assigned through experimentation/observation
        w1 = 2.6  # open cells 
        w2 = 1.35  # max tile 
        w3 = 1.0  # monotonicity
        w4 = 0.15  # smoothness
        w5 = 1.4  # large tiles on edges
        w6 = 1.0
        
        return (w1 * f1) + (w2 * f2) + (w3 * f3) + (w4 * f4) + (w5 * f5) + (w6 * f6)
        
    def maximize(self, state, depth, alpha, beta):
        """
        represents human player with alpha-beta
        pruning.
        """
        moves = state.getAvailableMoves()
        # order pruning by empty cell count of moves
        moves.sort(key = lambda x: len(x[1].getAvailableCells()), reverse=True)
        
        if depth == 0 or not moves:  # terminal test
            return None, self.evaluate(state)
    
        best_move, maxUtility = None, float('-inf')
        
        for move, new_state in moves:
            _, utility = self.chance(new_state, depth - 1, alpha, beta)
            if utility > maxUtility:
                best_move, maxUtility = move, utility
            
            # prune branches with alpha beta algorithm
            alpha = max(alpha, utility)
            if alpha >= beta:
                break
        
        return best_move, maxUtility

    def chance(self, state, depth, alpha, beta):
        """
        chance node representing computerAI and opponent,
        playing advesarially.
        """
        empty_cells = state.getAvailableCells()
        
        if depth == 0 or not empty_cells:  # terminal test
            return None, self.evaluate(state)
        
        if len(empty_cells) > 6:  # sample cells if too many
            empty_cells = random.sample(empty_cells, 6)
        
        expected_utility = 0
        cell_prob = 1 / len(empty_cells)
        for pos in empty_cells:
            for tile, tile_prob in self.possibleNewTiles:
                new_state = state.clone()
                new_state.insertTile(pos, tile)
                _, utility = self.maximize(new_state, depth - 1, alpha, beta)
                # calculate expected utility by weighted probabilities
                expected_utility += (tile_prob * utility * cell_prob)
        
        return None, expected_utility
    
    def monotonicity(self, state):
        """
        heuristic creating penalty for non-monotonic rows/cols,
        "encouraging consistent tile ordering".
        """
        penalty = 0
        
        # check monotonicity across rows
        for i in range(state.size):
            row = state.map[i]
            for col in range(state.size - 1):
                curr = row[col]
                right = row[col + 1]
                if curr != 0 and right != 0:
                    # use log2 to prevent skew from tile values
                    penalty += abs(math.log2(curr) - math.log2(right))
        
        # check monotonicity across cols
        for col in range(state.size):
            for row in range(state.size - 1):
                curr = state.map[row][col]
                below = state.map[row + 1][col]
                if curr != 0 and below != 0:
                    penalty += abs(math.log2(curr) - math.log2(below))
                    
        return -penalty

    def smoothness(self, state):
        """
        heuristic for smoothness of tile values across grid.
        represents increased frequency of possible merges.
        """
        penalty = 0
        for r in range(state.size):
            for c in range(state.size):
                if state.map[r][c] == 0:
                    continue
                curr = state.map[r][c]
                # calculate adjacent cells that are within bound
                for dx, dy in [(0, 1), (1, 0)]:
                    nx, ny = r + dx, c + dy
                    if 0 <= nx < state.size and 0 <= ny < state.size:
                        if state.map[nx][ny] != 0:
                            adj = state.map[nx][ny]
                            # use log2 to prevent skew of tile values
                            penalty += abs(math.log2(curr) - math.log2(adj))

        # smoothness of grid is good
        return -penalty

    def large_edge_tiles(self, state):
        """
        heuristic for large values across board edge.
        inspiration from stack overflow thread linked in assignment.
        """
        max_tile = state.getMaxTile()
        bonus = 0
        
        # check corners
        for r, c in [(0, 0), (0, state.size - 1), (state.size - 1, state.size - 1), (state.size - 1, 0)]:
            if state.map[r][c] == max_tile:
                bonus += math.log2(max_tile)
        
        # check edges
        for r in range(1, state.size - 1):
            if state.map[r][0] == max_tile:
                bonus += math.log2(max_tile)
    
            if state.map[r][state.size - 1] == max_tile:
                bonus += math.log2(max_tile)
        
        for c in range(1, state.size - 1):
            if state.map[0][c] == max_tile:
                bonus += math.log2(max_tile)
    
            if state.map[state.size - 1][c] == max_tile:
                bonus += math.log2(max_tile)                
        
        return bonus

    def snake_pattern(self, state):
        """
        heuristic inspired from another stack overflow post.
        https://stackoverflow.com/questions/26762846/2048-heuristic-unexpected-results.
        """
        # multiply each cell in grid with decreasing weights
        # if snake shape then "easier to merge"
        mask = [
            [16, 15, 14, 13],
            [12, 11, 10,  9],
            [ 8,  7,  6,  5],
            [ 4,  3,  2,  1]
        ]
        score = 0
        for i in range(state.size):
            for j in range(state.size):
                score += (state.map[i][j] * mask[i][j])
        
        return score
                
    def getMove(self, grid):
        # pass in default alpha beta values
        best_move, _ = self.maximize(grid, self.search_depth, -float('inf'), float('inf'))
        return best_move