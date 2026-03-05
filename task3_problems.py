"""Task 3: Problem Definitions for Search Comparison

This module defines the states, actions, and goal tests for the requested problems:
1. Milk and Water Jug Problem
2. Missionaries and Cannibals Problem
3. Tic Tac Toe (simplified as search problem)
4. Eight Queens Problem
"""

from typing import List, Tuple, Any


# 1. Milk and Water Jug Problem
# State: (jug1_volume, jug2_volume)
class WaterJugProblem:
    def __init__(self, capacity1=4, capacity2=3, target=2):
        self.capacity1 = capacity1
        self.capacity2 = capacity2
        self.target = target
    
    def initial_state(self):
        return (0, 0)
    
    def goal_test(self, state):
        return state[0] == self.target or state[1] == self.target
    
    def get_successors(self, state):
        j1, j2 = state
        successors = []
        
        # Fill jug 1
        if j1 < self.capacity1:
            successors.append(("Fill Jug 1", (self.capacity1, j2), 1))
        
        # Fill jug 2
        if j2 < self.capacity2:
            successors.append(("Fill Jug 2", (j1, self.capacity2), 1))
        
        # Empty jug 1
        if j1 > 0:
            successors.append(("Empty Jug 1", (0, j2), 1))
        
        # Empty jug 2
        if j2 > 0:
            successors.append(("Empty Jug 2", (j1, 0), 1))
        
        # Pour jug 1 to jug 2
        if j1 > 0 and j2 < self.capacity2:
            amount = min(j1, self.capacity2 - j2)
            successors.append(("Pour J1 -> J2", (j1 - amount, j2 + amount), 1))
        
        # Pour jug 2 to jug 1
        if j2 > 0 and j1 < self.capacity1:
            amount = min(j2, self.capacity1 - j1)
            successors.append(("Pour J2 -> J1", (j1 + amount, j2 - amount), 1))
        
        return successors


# 2. Missionaries and Cannibals Problem
# State: (m_left, c_left, boat_pos) where boat_pos: 0 for left, 1 for right
class MissionariesCannibalsProblem:
    def __init__(self, total_m=3, total_c=3):
        self.total_m = total_m
        self.total_c = total_c
    
    def initial_state(self):
        return (self.total_m, self.total_c, 0)
    
    def goal_test(self, state):
        return state == (0, 0, 1)
    
    def is_valid(self, m, c):
        if m < 0 or c < 0 or m > self.total_m or c > self.total_c:
            return False
        if m > 0 and m < c:
            return False
        m_right = self.total_m - m
        c_right = self.total_c - c
        if m_right > 0 and m_right < c_right:
            return False
        return True
    
    def get_successors(self, state):
        m, c, boat = state
        successors = []
        moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
        
        for dm, dc in moves:
            if boat == 0:  # Moving left to right
                new_state = (m - dm, c - dc, 1)
                action = f"Move {dm}M, {dc}C to Right"
            else:  # Moving right to left
                new_state = (m + dm, c + dc, 0)
                action = f"Move {dm}M, {dc}C to Left"
            
            if self.is_valid(new_state[0], new_state[1]):
                successors.append((action, new_state, 1))
        
        return successors


# 3. Tic Tac Toe (Simplified Search)
# State: board as tuple of 9 characters
class TicTacToeProblem:
    def __init__(self):
        self.initial_board = (' ',) * 9
    
    def initial_state(self):
        return self.initial_board
    
    def check_win(self, board, player):
        lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        return any(all(board[i] == player for i in line) for line in lines)
    
    def goal_test(self, state):
        # Goal: Find a sequence of moves that leads to X winning
        return self.check_win(state, 'X')
    
    def get_successors(self, state):
        board = list(state)
        x_count = board.count('X')
        o_count = board.count('O')
        
        # X always moves first
        player = 'X' if x_count == o_count else 'O'
        
        # If someone already won, no more moves
        if self.check_win(state, 'X') or self.check_win(state, 'O'):
            return []
            
        successors = []
        for i in range(9):
            if board[i] == ' ':
                new_board = board[:]
                new_board[i] = player
                successors.append((f"Player {player} marks {i}", tuple(new_board), 1))
        
        return successors


# 4. Eight Queens Problem
# State: tuple of column positions for each row (0-7)
class EightQueensProblem:
    def __init__(self, n=8):
        self.n = n
    
    def initial_state(self):
        return ()
    
    def goal_test(self, state):
        return len(state) == self.n
    
    def is_safe(self, state, col):
        row = len(state)
        for r, c in enumerate(state):
            if c == col or abs(c - col) == abs(r - row):
                return False
        return True
    
    def get_successors(self, state):
        if len(state) >= self.n:
            return []
            
        successors = []
        for col in range(self.n):
            if self.is_safe(state, col):
                new_state = state + (col,)
                successors.append((f"Place Queen at row {len(state)}, col {col}", new_state, 1))
        
        return successors


if __name__ == "__main__":
    print("AI Search Problems Defined:")
    print("1. Water Jug (4L, 3L -> 2L)")
    print("2. Missionaries and Cannibals (3M, 3C)")
    print("3. Tic Tac Toe (X Win search)")
    print("4. Eight Queens")
