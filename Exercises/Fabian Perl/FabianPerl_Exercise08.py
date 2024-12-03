import random

class Node:
    def __init__(self, id, value) -> None:
        self.id = id
        self.value = value
        self.distance = float("inf")
        
    def return_info(self):
        return (self.id, self.value)

def make_array(path):
    output = []
    with open(path, "r") as file:
        for line in file:
            line_arr = []
            for i in line:
                try:
                    line_arr.append(int(i))
                except:
                    continue
            output.append(line_arr)
    return output

def make_node_array(array):
    output = []
    count = 0
    for i in array:
        row = []
        for j in i:
            row.append(Node(count, j))
            count += 1
        output.append(row)
    return output
        
def make_adjazensliste(node_array):     #make list of connections between the nodes in the directions given in the comments
    output = [] 
    
    for row_index in range(len(node_array)):     
        for node_index in range(len(node_array[row_index])):
            
            current_node = node_array[row_index][node_index]
            current_node_id = current_node.id
            len_row = len(node_array[0])
            
            if current_node_id == len_row - 1:                                                                               #down
                output.append([node_array[row_index + 1][node_index].return_info()])
            
            elif (current_node_id % len_row == 0 and row_index != (len(node_array) - 1)) or current_node_id < len_row - 1:  #right, down
                output.append([node_array[row_index][node_index + 1].return_info(), node_array[row_index + 1][node_index].return_info()])

            elif ((current_node_id + 1) % len_row) == 0 and row_index != (len(node_array) - 1) and row_index != 0:                       #left, down
                output.append([node_array[row_index][node_index - 1].return_info(), node_array[row_index + 1][node_index].return_info()])
            
            elif current_node_id == (len(node_array) - 1) * len_row:                                                              #right
                output.append([node_array[row_index][node_index + 1].return_info()])
                
            elif current_node_id > (len(node_array) - 1) * len_row and node_index < len_row - 1:    #right, up
                output.append([node_array[row_index][node_index + 1].return_info(), node_array[row_index - 1][node_index].return_info()])
                
            elif current_node_id == len(node_array) * len_row - 1:           #end --> no directions
                 output.append([node_array[row_index][node_index].return_info()])
                 
            else:                                                                               #up, down, left, right
                output.append([node_array[row_index][node_index - 1].return_info(), node_array[row_index][node_index + 1].return_info(), node_array[row_index - 1][node_index].return_info(), node_array[row_index + 1][node_index].return_info()])
    return output

def node_array_to_dict(node_array):
    output = {}
    for row in node_array:
        for node in row:
            output.update({node.id: node})
    
    return output
    
def dijkstra_algorithm(node_array):
    adjazensliste = make_adjazensliste(node_array)
    node_dict = node_array_to_dict(node_array)
    
    S = node_dict[0] 
    optimal = [S]
    node_dict_copy = node_dict.copy()
    node_dict_copy.pop(0)
    rest = node_dict_copy

    for node_index in rest:
        for connection in adjazensliste[S.id]:
            node_dict[connection[0]].distance = connection[1]
            
    while len(rest) > 0:

        K = random.choice(list(rest.items()))[1]        #choose random node in rest
          
        for node_index in rest:
            if rest[node_index].distance < K.distance:
                K = node_dict[rest[node_index].id]
                        
        optimal.append(K)
        rest.pop(K.id)
        
        for kante in adjazensliste[K.id]:
            if kante[0] in rest:
                node_dict[kante[0]].distance = min(node_dict[kante[0]].distance, node_dict[K.id].distance + kante[1])
    
    return node_dict[len(node_array) * len(node_array[0]) - 1].distance  
        
print(dijkstra_algorithm(make_node_array(make_array("data/exercise_cave.txt")))) 