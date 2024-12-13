import heapq
import time

def parse_input(input_data):
    return [list(map(int, line.strip())) for line in input_data.splitlines()]

def dijkstra(grid): #use of dijkstra as the perfect algrithm
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    min_risks = [[float('inf')] * cols for _ in range(rows)]
    min_risks[0][0] = 0

    # Priority queue to store (current risk, x, y)
    pq = [(0, 0, 0)]
    
    while pq:
        current_risk, x, y = heapq.heappop(pq)

        # If we reached the bottom-right corner, return the risk
        if (x, y) == (rows - 1, cols - 1):
            return current_risk

        # Skip if we found a better path to (x, y) already
        if current_risk > min_risks[x][y]:
            continue

        # neighbors
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                new_risk = current_risk + grid[nx][ny]
                if new_risk < min_risks[nx][ny]:
                    min_risks[nx][ny] = new_risk
                    heapq.heappush(pq, (new_risk, nx, ny))

    return float('inf')  # If no path is found (should not happen in this problem)

# main
def main():
    start_time = time.time()  # Start
    with open('c:/Users/langg/Documents/GitHub/ppp-2024/Exercises/Elias Becker/exercise_cave.txt') as f:
        input_data = f.read()
    grid = parse_input(input_data)
    result = dijkstra(grid)
    print("Lowest total risk:", result)
    end_time = time.time()  # End
    
    # Laufzeit berechnen
    print(f"Time: {end_time - start_time:} seconds")

if __name__ == "__main__":
    main()
