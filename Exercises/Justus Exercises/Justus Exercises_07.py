
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple, Optional
import matplotlib.colors as mcolors

class BreakoutGame:
    # Tile type constants
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4

    def __init__(self, memory_file: str):
        """Initialize the Breakout game with the provided memory file."""
        self.memory = self.load_memory_from_file(memory_file)
        self.screen: Dict[Tuple[int, int], int] = {} #create dict with key x,y and values tile_id 
        self.score = 0
        self.ball_x: Optional[int] = None
        self.paddle_x: Optional[int] = None
        self.outputs: List[int] = []
        
        # Color mapping
        self.colors = {
            self.BALL: "white",       # Ball remains white
            self.EMPTY: "black",      # Empty space remains black
            self.BLOCK: {            # Blocks in classic arcade colors
                0: "#FF0000",        # Top row: Red
                1: "#FF7F00",        # Second row: Orange
                2: "#FFFF00",        # Third row: Yellow
                3: "#00CC00",        # Fourth row: Green
                4: "#0000FF",        # Bottom row: Blue
                5: "#4B0082",        # Additional row: Indigo
                6: "#9400D3"         # Additional row: Violet
            },
            self.PADDLE: "green",    # Paddle remains green
            self.WALL: "white"       # Walls remain white
        }

    @staticmethod
    def load_memory_from_file(file_path: str) -> List[int]:
        """Load and parse the memory from a file."""
        try:
            with open(file_path, 'r') as file:
                content = file.read().strip()
                # Handle both comma-separated and newline-separated inputs if the input changes again 
                content = content.replace('\n', ',')
                return [int(x) for x in content.split(',')]
        except FileNotFoundError:
            raise FileNotFoundError(f"Memory file not found: {file_path}")
        except ValueError:
            raise ValueError("Invalid memory file format: must contain comma-separated integers")


    def joystick_input(self) -> int:
        """Determine paddle adjustment based on ball and paddle positions."""
        if self.ball_x is None or self.paddle_x is None:
            return 0
        if self.ball_x > self.paddle_x:
            return 1
        elif self.ball_x < self.paddle_x:
            return -1
        return 0


    def handle_output(self, value: int) -> None:
        """Process output values from the computer."""
        self.outputs.append(value)#Adds the latest output value to a temporary list,
        if len(self.outputs) == 3:# Checks if self.outputs has accumulated three values.
            x, y, tile_id = self.outputs #Extracts the three values into variables
            self.outputs = []  # Reset for next triplet
            
            if x == -1 and y == 0: #check if the tuple is for the score 
                self.score = tile_id
            else: 
                self.screen[(x, y)] = tile_id # updates dict with tile id at position x,y
                if tile_id == self.BALL:
                    self.ball_x = x #updates the ball x position for auto playing 
                elif tile_id == self.PADDLE:
                    self.paddle_x = x #upates pedal position for auto playing 


    def draw_screen(self) -> None:
        """Draw the current game state using matplotlib with multi-colored blocks and faster rendering."""
        if not self.screen:
            raise ValueError("No screen data to display")

        
        plt.clf() #without clf mpl would keep layering plots on top of each other making the game really slow, it clears the figure without actually deleting it like close would so it can be reused. 
        
        # Create the game grid
        max_x = max(x for x, _ in self.screen.keys())
        max_y = max(y for _, y in self.screen.keys())
        grid = np.zeros((max_y + 1, max_x + 1), dtype=int) #create array filled wiht zeros, adding plus 1 nsures that the array can include all possible positions from0,0 to max,max

        # Prepare color mapping
        base_colors = [
            self.colors[self.EMPTY],    # Black (background)
            self.colors[self.WALL],     # White (wall)
            "#FF0000",                  # Red (default block)
            self.colors[self.PADDLE],   # Green (paddle)
            self.colors[self.BALL]      # White (ball)
        ]
        
        # Add color gradient for blocks
        block_colors = [
            self.colors[self.BLOCK].get(i, "#FF0000") 
            for i in range(7)
        ]
        
        # Combine color lists
        full_color_list = base_colors + block_colors
        custom_cmap = mcolors.ListedColormap(full_color_list)
        
        # Populate grid
        for (x, y), tile_id in self.screen.items():
            if tile_id == self.BLOCK:
                # Use row number to determine block color
                grid[y][x] = 5 + (y % 7)  # Offset to block color section
            else:
                grid[y][x] = tile_id 

       
        plt.imshow(grid, cmap=custom_cmap, interpolation='nearest', origin="upper") #Each number in the gris is replaced with it's corresponding color from the custom color map, interploation nearest removes any spaces between neighbouring blocks 
        plt.title(f"Breakout Game - Score: {self.score}")
        plt.axis('off')  # Turn off axis for cleaner view
        plt.tight_layout(pad=5)
        plt.draw()
        plt.pause(0.000000001) # forcing mpl to refresh the scene as quickly as possible 


    @staticmethod
    def parse_instruction(instruction: int) -> Tuple[int, List[int]]:
        """Parse an instruction into opcode and parameter modes."""
        opcode = instruction % 100
        modes = [(instruction // 10 ** i) % 10 for i in range(2, 5)]
        return opcode, modes


    def run_game(self):
        """Run the game with optional interactivity and frame saving."""
        memory = defaultdict(int, enumerate(self.memory))
        relative_base = 0
        pointer = 0
       

        def get_value(param: int, mode: int) -> int:
            if mode == 0:  # Position mode
                return memory[param]
            elif mode == 1:  # Immediate mode
                return param
            elif mode == 2:  # Relative mode
                return memory[relative_base + param]
            raise ValueError(f"Invalid parameter mode: {mode}")


        def write_value(param: int, mode: int, value: int) -> None:
            if mode == 0:  # Position mode
                memory[param] = value
            elif mode == 2:  # Relative mode
                memory[relative_base + param] = value
            else:
                raise ValueError(f"Invalid parameter mode for writing: {mode}")

        while True:
            instruction = memory[pointer]
            opcode, modes = self.parse_instruction(instruction)
            mode1, mode2, mode3 = modes

            if opcode == 99:  # Halt
                break

            if opcode in [1, 2, 7, 8]:  # Arithmetic and comparison operations
                param1, param2, param3 = (memory[pointer + i] for i in range(1, 4))
                val1 = get_value(param1, mode1)
                val2 = get_value(param2, mode2)

                if opcode == 1:
                    result = val1 + val2
                elif opcode == 2:
                    result = val1 * val2
                elif opcode == 7:
                    result = int(val1 < val2)
                else:  # opcode == 8
                    result = int(val1 == val2)

                write_value(param3, mode3, result)
                pointer += 4

            elif opcode == 3:  # Input
                param1 = memory[pointer + 1]
                write_value(param1, mode1, self.joystick_input())
                pointer += 2

            elif opcode == 4:  # Output
                param1 = memory[pointer + 1]
                output = get_value(param1, mode1)
                self.handle_output(output)
                
                if len(self.outputs) == 0:  
                    self.draw_screen() # Update game state 
                pointer += 2

            elif opcode in [5, 6]:  # Jump instructions
                param1, param2 = memory[pointer + 1], memory[pointer + 2]
                val1 = get_value(param1, mode1)
                val2 = get_value(param2, mode2)

                if (opcode == 5 and val1 != 0) or (opcode == 6 and val1 == 0):
                    pointer = val2
                else:
                    pointer += 3

            elif opcode == 9:  # Adjust relative base
                param1 = memory[pointer + 1]
                relative_base += get_value(param1, mode1)
                pointer += 2

            else:
                raise ValueError(f"Unknown opcode {opcode} at position {pointer}")

        return self.screen, self.score


def main():
    try:
      
        game = BreakoutGame("breakout_commands.txt")
        print("\nStarting interactive gameplay...")
        game = BreakoutGame("breakout_commands.txt")
        game.memory[0] = 2  # Set to interactive mode
        final_score = game.run_game()
        print(f"Final Score: {final_score}")
        
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
