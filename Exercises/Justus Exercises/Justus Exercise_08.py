import heapq
from typing import List
import os
import time


def load_grid_from_file(file_path: str) -> List[List[int]]:
    """Load and parse the grid from a file."""
    try:
        with open(file_path, 'r') as file:
            content = file.read().strip()
            # Split by newline to handle grid rows
            rows = content.split('\n')
            return [[int(char) for char in row] for row in rows]
    except FileNotFoundError:
        raise FileNotFoundError(f"Grid file not found: {file_path}")
    except ValueError:
        raise ValueError("Invalid grid file format: each row must contain integers only.")


def lowest_total_risk(grid: List[List[int]]) -> int:
    """Find the lowest total risk from the top-left to the bottom-right of the grid."""
    # Define directions for movement (up, down, left, right)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    rows, cols = len(grid), len(grid[0])
    
    # Priority queue for Dijkstra's algorithm
    pq = [(0, 0, 0)]  # (risk, row, col)
    visited = set()
    risk_levels = {(0, 0): 0}
    
    while pq:
        current_risk, row, col = heapq.heappop(pq)
        
        # If we found tne bottom-right corner, return the risk
        if (row, col) == (rows - 1, cols - 1):
            return current_risk
        
        if (row, col) in visited:
            continue
        visited.add((row, col))
        
        # Check all neighbors
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < rows and 0 <= new_col < cols:
                new_risk = current_risk + grid[new_row][new_col]
                if (new_row, new_col) not in risk_levels or new_risk < risk_levels[(new_row, new_col)]:
                    risk_levels[(new_row, new_col)] = new_risk
                    heapq.heappush(pq, (new_risk, new_row, new_col))

def main():
    timer = time.time()
    file_path = os.path.join(os.path.dirname(__file__), "cave.txt")
    grid = load_grid_from_file(file_path)
    result = lowest_total_risk(grid)
    print(f"The lowest total risk is: {result}")
    print(time.time()-timer)

if __name__ == "__main__":
    main()
