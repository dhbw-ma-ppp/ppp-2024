#--- Day 15: Chiton ---

#You've almost reached the exit of the cave, but the walls are getting closer together. Your submarine can barely still fit, though; the main problem is that the walls of the cave are covered in chitons, and it would be best not to bump any of them.

#The cavern is large, but has a very low ceiling, restricting your motion to two dimensions. The shape of the cavern resembles a square; a quick scan of chiton density produces a map of risk level throughout the cave (your puzzle input). For example:

#1163751742
#1381373672
#2136511328
#3694931569
#7463417111
#1319128137
#1359912421
#3125421639
#1293138521
#2311944581
#You start in the top left position, your destination is the bottom right position, and you cannot move diagonally. The number at each position is its risk level; to determine the total risk of an entire path, add up the risk levels of each position you enter (that is, don't count the risk level of your starting position unless you enter it; leaving it adds no risk to your total).

#Your goal is to find a path with the lowest total risk. In this example, a path with the lowest total risk is highlighted here:

#1163751742
#1381373672
#2136511328
#3694931569
#7463417111
#1319128137
#1359912421
#3125421639
#1293138521
#2311944581
#The total risk of this path is 40 (the starting position is never entered, so its risk is not counted).

#What is the lowest total risk of any path from the top left to the bottom right?
import sys
import numpy as np
import heapq

sys.path.append('/Users/hannah/Desktop/Ppp/ppp-2024/Exercises/HannahGedler')
with open('/Users/hannah/Desktop/Ppp/ppp-2024/Exercises/HannahGedler/exercise_cave.txt', 'r') as file: 
    matrix_all_lines = []
    matrix_input = file.read()
    lines = matrix_input.splitlines()
 
    for line in lines:
        matrix_all_lines.append([int(x) for x in line]) # das int das jede zahl einzeln als zahl gesehten wird
    #print (matrix_all_lines)

    matrix = np.array(matrix_all_lines)
    


directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
#directions = [ (0, 1), (1,0),(0,-1)] -> result: 510



def min_path_sum(matrix):
    if matrix.size == 0:
        return 0

    rows, cols = matrix.shape

    risks = [(matrix[0, 0], 0, 0)]  #(priorityqueue mit riskhöhe (= priorität), row, column)
    lowest_risk_matrix = np.full((rows, cols), float('inf')) #inf weil die unbekannten werte noch keinen wert haben ->unendlich sind
    lowest_risk_matrix[0, 0] = matrix[0, 0]

    while risks:
        find_risk = heapq.heappop(risks)
        risk = find_risk[0]
        row_kor = find_risk[1]
        col_kor = find_risk[2]

        if row_kor == rows - 1 and col_kor == cols - 1: #wenn man durch ist
            return risk
        
        for neighbours in directions:
            possible_row_kor, possible_col_kor = neighbours
            next_row = possible_row_kor + row_kor
            next_col = possible_col_kor + col_kor
        
            if 0 <= next_row < rows and 0 <= next_col < cols: #schaun ob die zahlen auch in der matrix sind
                new_risk = risk + matrix[next_row, next_col]
                
                if new_risk < lowest_risk_matrix[next_row, next_col]:
                    lowest_risk_matrix[next_row, next_col] = new_risk
                    heapq.heappush(risks, (new_risk, next_row, next_col))

    return lowest_risk_matrix[rows - 1, cols - 1]  

print("the lowest risk is:" ,min_path_sum(matrix) - matrix[0,0])


