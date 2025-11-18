"""
Sudoku solver modeled as constraint satisfaction problem.

Uses backtracking with Minimum Remaining Values heuristic and forward check.
"""

import sys
import heapq
import copy

ROW = "ABCDEFGHI"
COL = "123456789"

def check_same_square(r1, c1, r2, c2):
    """Helper function to check if two positions in same square."""
    
    # subtract by ascii value to get index of rows
    # integer division by 3 for mapping to each square on board
    if (ord(r1) - ord('A')) // 3 == (ord(r2) - ord('A')) // 3:
        if (int(c1) - 1) // 3 == (int(c2) - 1) // 3:
            return True
    return False


def forward_check(unassigned, p, move):
    """Helper function for forward check of inevitable failure."""

    r, c = p
    for pos in unassigned:
        if p == pos:
            continue
        r2, c2 = pos
        if pos[0] == r or pos[1] == c or check_same_square(r, c, r2, c2):
            unassigned[pos].discard(move)
        
        if len(unassigned[pos]) == 0:
            return False
    return True


def backtracking(board):
    """Takes a board and returns solved board."""

    # backtracking
    # need to use MRV heuristic and forward checking to solve
    #   MRV -- choose variable with fewest legal moves
    #   FC  -- keep track of remaining legal values for unassigned var
    #          terminate when any variable has no legal values
    
    # calculate legal moves for unassigned positions
    unassigned = {}
    
    for r in ROW:
        for c in COL:
            if (board[r + c]) == 0:  # unassigned variable found
                # initialize with all possible legal moves
                unassigned[r + c] = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
    
    # filter out illegal moves for unassigned variables
    for r in ROW:
        for c in COL:
            if (board[r + c]) != 0:
                move = board[r + c]
                # remove value from legal moves of
                # unassigned variables if same row, col, or square
                for pos in unassigned:
                    r2, c2 = pos
                    if pos[0] == r or pos[1] == c or check_same_square(r, c, r2, c2):
                        unassigned[pos].discard(move)
    
    # nested recursive function
    def backtrack(unassigned, board):
        # if assignment complete return board
        if not unassigned:
            return board
        
        # priority queue for MRV heuristic
        pq = []
        for pos, val in unassigned.items():
            heapq.heappush(pq, (len(val), pos))
    
        _, pos = heapq.heappop(pq)
        legal_moves = list(unassigned[pos])
        
        for move in legal_moves:
            board[pos] = move
            
            # forward check with copy of unassigned dictionary
            # to keep original intact in case of failure
            unassigned_copy = copy.deepcopy(unassigned)
            
            if forward_check(unassigned_copy, pos, move):
                # if ok then assign and update remaining legal values
                unassigned_copy.pop(pos)
                
                # recursive call
                res = backtrack(unassigned_copy, board)
                if res is not None:
                    return res
            
            # undo assignment
            board[pos] = 0
            
        return None
    
    solved_board = backtrack(unassigned, board)
    return solved_board if solved_board else board
