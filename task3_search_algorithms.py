"""Task 3: Uninformed Search Strategies - BFS and DFS with Variants

This module implements Breadth-First Search (BFS) and Depth-First Search (DFS)
along with their variants for solving various AI problems.
"""

from collections import deque
from typing import List, Set, Tuple, Optional, Callable
import time


class SearchNode:
    """Represents a node in the search tree."""
    
    def __init__(self, state, parent=None, action=None, depth=0, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
        self.path_cost = path_cost
    
    def __repr__(self):
        return f"Node(state={self.state}, depth={self.depth})"
    
    def __eq__(self, other):
        return isinstance(other, SearchNode) and self.state == other.state
    
    def __hash__(self):
        return hash(str(self.state))


class SearchStatistics:
    """Track statistics during search."""
    
    def __init__(self):
        self.nodes_expanded = 0
        self.nodes_generated = 0
        self.max_frontier_size = 0
        self.solution_depth = 0
        self.execution_time = 0.0


def reconstruct_path(node: SearchNode) -> List:
    """Reconstruct the path from start to goal."""
    path = []
    actions = []
    
    while node:
        path.append(node.state)
        if node.action:
            actions.append(node.action)
        node = node.parent
    
    return list(reversed(path)), list(reversed(actions))


def breadth_first_search(initial_state, goal_test: Callable, get_successors: Callable,
                         max_depth: Optional[int] = None) -> Tuple[SearchNode, SearchStatistics]:
    """Standard Breadth-First Search.
    
    Args:
        initial_state: Starting state
        goal_test: Function to check if a state is the goal
        get_successors: Function to get successor states
        max_depth: Maximum depth to search (None for unlimited)
    
    Returns:
        Tuple of (goal_node, statistics) or (None, statistics) if no solution
    """
    stats = SearchStatistics()
    start_time = time.time()
    
    if goal_test(initial_state):
        stats.execution_time = time.time() - start_time
        return SearchNode(initial_state), stats
    
    frontier = deque([SearchNode(initial_state)])
    explored = set()
    stats.nodes_generated = 1
    
    while frontier:
        stats.max_frontier_size = max(stats.max_frontier_size, len(frontier))
        node = frontier.popleft()
        explored.add(str(node.state))
        stats.nodes_expanded += 1
        
        if max_depth and node.depth >= max_depth:
            continue
        
        for action, successor_state, cost in get_successors(node.state):
            child = SearchNode(
                successor_state,
                parent=node,
                action=action,
                depth=node.depth + 1,
                path_cost=node.path_cost + cost
            )
            
            if str(child.state) not in explored and child not in frontier:
                if goal_test(child.state):
                    stats.solution_depth = child.depth
                    stats.execution_time = time.time() - start_time
                    return child, stats
                
                frontier.append(child)
                stats.nodes_generated += 1
    
    stats.execution_time = time.time() - start_time
    return None, stats


def depth_first_search(initial_state, goal_test: Callable, get_successors: Callable,
                       max_depth: Optional[int] = None) -> Tuple[SearchNode, SearchStatistics]:
    """Standard Depth-First Search.
    
    Args:
        initial_state: Starting state
        goal_test: Function to check if a state is the goal
        get_successors: Function to get successor states
        max_depth: Maximum depth to search (None for unlimited)
    
    Returns:
        Tuple of (goal_node, statistics) or (None, statistics) if no solution
    """
    stats = SearchStatistics()
    start_time = time.time()
    
    if goal_test(initial_state):
        stats.execution_time = time.time() - start_time
        return SearchNode(initial_state), stats
    
    frontier = [SearchNode(initial_state)]  # Stack (LIFO)
    explored = set()
    stats.nodes_generated = 1
    
    while frontier:
        stats.max_frontier_size = max(stats.max_frontier_size, len(frontier))
        node = frontier.pop()  # Pop from end (LIFO)
        
        if str(node.state) in explored:
            continue
        
        explored.add(str(node.state))
        stats.nodes_expanded += 1
        
        if goal_test(node.state):
            stats.solution_depth = node.depth
            stats.execution_time = time.time() - start_time
            return node, stats
        
        if max_depth and node.depth >= max_depth:
            continue
        
        # Add successors in reverse order to maintain left-to-right expansion
        successors = []
        for action, successor_state, cost in get_successors(node.state):
            child = SearchNode(
                successor_state,
                parent=node,
                action=action,
                depth=node.depth + 1,
                path_cost=node.path_cost + cost
            )
            if str(child.state) not in explored:
                successors.append(child)
                stats.nodes_generated += 1
        
        # Add in reverse to maintain order
        frontier.extend(reversed(successors))
    
    stats.execution_time = time.time() - start_time
    return None, stats


def depth_limited_search(initial_state, goal_test: Callable, get_successors: Callable,
                         depth_limit: int) -> Tuple[SearchNode, SearchStatistics]:
    """Depth-Limited Search (DLS) - DFS variant with depth limit."""
    return depth_first_search(initial_state, goal_test, get_successors, max_depth=depth_limit)


def iterative_deepening_search(initial_state, goal_test: Callable, get_successors: Callable,
                               max_depth: int = 100) -> Tuple[SearchNode, SearchStatistics]:
    """Iterative Deepening Depth-First Search (IDDFS)."""
    combined_stats = SearchStatistics()
    start_time = time.time()
    
    for depth_limit in range(max_depth + 1):
        result, stats = depth_limited_search(initial_state, goal_test, get_successors, depth_limit)
        
        combined_stats.nodes_expanded += stats.nodes_expanded
        combined_stats.nodes_generated += stats.nodes_generated
        combined_stats.max_frontier_size = max(combined_stats.max_frontier_size, stats.max_frontier_size)
        
        if result:
            combined_stats.solution_depth = result.depth
            combined_stats.execution_time = time.time() - start_time
            return result, combined_stats
    
    combined_stats.execution_time = time.time() - start_time
    return None, combined_stats


def bidirectional_search(initial_state, goal_state, get_successors: Callable,
                         get_predecessors: Callable) -> Tuple[SearchNode, SearchStatistics]:
    """Bidirectional Search - searches from both start and goal."""
    stats = SearchStatistics()
    start_time = time.time()
    
    if initial_state == goal_state:
        stats.execution_time = time.time() - start_time
        return SearchNode(initial_state), stats
    
    # Forward search from initial state
    forward_frontier = deque([SearchNode(initial_state)])
    forward_explored = {str(initial_state): SearchNode(initial_state)}
    
    # Backward search from goal state
    backward_frontier = deque([SearchNode(goal_state)])
    backward_explored = {str(goal_state): SearchNode(goal_state)}
    
    stats.nodes_generated = 2
    
    while forward_frontier and backward_frontier:
        stats.max_frontier_size = max(stats.max_frontier_size, 
                                      len(forward_frontier) + len(backward_frontier))
        
        # Forward step
        if forward_frontier:
            node = forward_frontier.popleft()
            stats.nodes_expanded += 1
            
            for action, successor_state, cost in get_successors(node.state):
                child = SearchNode(successor_state, parent=node, action=action,
                                   depth=node.depth + 1, path_cost=node.path_cost + cost)
                
                state_str = str(child.state)
                
                # Check if we've met the backward search
                if state_str in backward_explored:
                    # Reconstruct path
                    forward_path, _ = reconstruct_path(child)
                    backward_path, _ = reconstruct_path(backward_explored[state_str])
                    backward_path.reverse()
                    
                    stats.solution_depth = child.depth + backward_explored[state_str].depth
                    stats.execution_time = time.time() - start_time
                    return child, stats
                
                if state_str not in forward_explored:
                    forward_frontier.append(child)
                    forward_explored[state_str] = child
                    stats.nodes_generated += 1
        
        # Backward step
        if backward_frontier:
            node = backward_frontier.popleft()
            stats.nodes_expanded += 1
            
            for action, predecessor_state, cost in get_predecessors(node.state):
                child = SearchNode(predecessor_state, parent=node, action=action,
                                   depth=node.depth + 1, path_cost=node.path_cost + cost)
                
                state_str = str(child.state)
                
                # Check if we've met the forward search
                if state_str in forward_explored:
                    forward_path, _ = reconstruct_path(forward_explored[state_str])
                    backward_path, _ = reconstruct_path(child)
                    backward_path.reverse()
                    
                    stats.solution_depth = forward_explored[state_str].depth + child.depth
                    stats.execution_time = time.time() - start_time
                    return forward_explored[state_str], stats
                
                if state_str not in backward_explored:
                    backward_frontier.append(child)
                    backward_explored[state_str] = child
                    stats.nodes_generated += 1
    
    stats.execution_time = time.time() - start_time
    return None, stats


def print_search_results(algorithm_name: str, result: SearchNode, stats: SearchStatistics):
    """Print formatted search results."""
    print(f"\n{'='*80}")
    print(f"{algorithm_name} Results")
    print(f"{'='*80}")
    
    if result:
        path, actions = reconstruct_path(result)
        print(f"\nSolution Found!")
        print(f"  Solution Depth: {stats.solution_depth}")
        print(f"  Path Length: {len(path)}")
        print(f"  Path Cost: {result.path_cost}")
        print(f"\nPath:")
        for i, state in enumerate(path):
            print(f"  Step {i}: {state}")
        if actions:
            print(f"\nActions: {' -> '.join(actions)}")
    else:
        print(f"\nNo Solution Found")
    
    print(f"\nStatistics:")
    print(f"  Nodes Expanded: {stats.nodes_expanded}")
    print(f"  Nodes Generated: {stats.nodes_generated}")
    print(f"  Max Frontier Size: {stats.max_frontier_size}")
    print(f"  Execution Time: {stats.execution_time:.6f} seconds")
    print()


if __name__ == "__main__":
    # Example: Simple graph traversal
    print("Uninformed Search Algorithms - BFS and DFS with Variants")
    print("This module provides the core search algorithms.")
    print("Run task3_problems.py to see these algorithms applied to specific problems.")
