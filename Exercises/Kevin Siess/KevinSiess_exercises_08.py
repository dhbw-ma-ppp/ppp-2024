# - Solve the exercise described at https://adventofcode.com/2021/day/15 using the data at `data/exercise_cave.txt` as input. Prepare a PR as usual.

import numpy as np

# def initiate_array():
#     with open("data/exercise_cave.txt", "r") as file:
#         row = file.readlines()
#         row_count = len(row)  # count rows
#         print(f"Count of Row: {row_count}")

#         columns = len(row[0].strip("\n"))  # count columns
#         print(f"Count of Column: {columns}")

#     arr = np.zeros((row_count, columns), dtype=int)

#     for i, element in enumerate(row):
#         arr[i] = np.array([int(x) for x in element.strip("\n")])

#     return arr

def initiate_array():
    # Test-Array definieren
    data = [
        [1, 1, 6, 3, 7, 5, 1, 7, 4, 2],
        [1, 3, 8, 1, 3, 7, 3, 6, 7, 2],
        [2, 1, 3, 6, 5, 1, 1, 3, 2, 8],
        [3, 6, 9, 4, 9, 3, 1, 5, 6, 9],
        [7, 4, 6, 3, 4, 1, 7, 1, 1, 1],
        [1, 3, 1, 9, 1, 2, 8, 1, 3, 7],
        [1, 3, 5, 9, 9, 1, 2, 4, 2, 1],
        [3, 1, 2, 5, 4, 2, 1, 6, 3, 9],
        [1, 2, 9, 3, 1, 3, 8, 5, 2, 1],
        [2, 3, 1, 1, 9, 4, 4, 5, 8, 1]
    ]

    # In ein NumPy-Array umwandeln
    arr = np.array(data, dtype=int)
    print(f"Array:\n{arr}")
    return arr

def check_values(arr, i, j, arr_path):
    rows, cols = arr.shape
    arr_right = float('inf')
    arr_down = float('inf')

    if j + 1 < cols:
        arr_right = arr[i, j + 1]

    if i + 1 < rows:
        arr_down = arr[i + 1, j]

    # check for smallest value
    if arr_right < arr_down:
        arr_path.append(arr_right)
        return i, j + 1
    
    elif arr_down < arr_right:
        arr_path.append(arr_down)
        return i + 1, j
    
    else:
        if j + 1 < cols:  # Wenn möglich, nach rechts gehen
            arr_path.append(arr_right)
            return i, j + 1
        
        elif i + 1 < rows:  # Wenn nicht, nach unten gehen
            arr_path.append(arr_down)
            return i + 1, j

def main():
    arr = initiate_array()
    arr_path = []  # save path

    i, j = 0, 0
    arr_path.append(arr[i, j])

    while i < arr.shape[0] - 1 or j < arr.shape[1] - 1:
        i, j = check_values(arr, i, j, arr_path)

    print(f"Path: {arr_path}")
    print(f"Sum: {sum(arr_path)}")

main()

#print(f'{arr.dtype.itemsize=}, {arr.dtype.byteorder=}, {arr.dtype.name=}')


# - Prepare for next Friday by forming groups of 2 (4 with task splitting), and deciding on the rough outline of the analytical app you'd like to build. 
#   - Take a look at the datasets available e.g. at
#     - https://www.kaggle.com/datasets
#     - https://archive.ics.uci.edu/datasets
#     - https://scikit-learn.org/1.5/datasets/toy_dataset.html
#   - Have some initial idea of what you want to achieve
#   - No need to prepare any code yet. You will have the entire lecture on Friday to start working.


