# to solve todays exercise you will need a fully functional int-computer,
# including relative offset features. If you did not complete the last exercise
# please ask one of the other students to share their implementation of the
# int-computer with you.
#
#
# We will run 'breakout' -- the arcade game -- on our simulated computer. 
# (https://en.wikipedia.org/wiki/Breakout_(video_game))
# The code for the computer will be provided under data/breakout_commands.txt
# the code will produce outputs in triplets. every triplet that is output
# specifies (x-position, y-position, tile_type).
# tiles can be of the following types:
# 0: empty tile
# 1: wall. walls are indestructible
# 2: block. blocks can be destroyed by the ball
# 3: paddle. the paddle is indestructible
# 4: ball. the ball moves diagonally and bounces off objects
# 
# EXAMPLE:
# a sequence of output values like 1, 2, 3, 6, 5, 4 would
#  - draw a paddle (type 3) at x=1, y=2
#  - draw the ball (type 4) at x=6, y=5
#
#
# PART 1:
# run the game until it exits. Analyse the output produced during the run, and create
# a visual representation (matplotlib or ascii-art are possibilities here...) of the screen display.
# mark the different tile types as different colors or symbols. Upload the picture with your PR.
#
# PART 2:
# The game didn't actually run in part 1, it just drew a single static screen.
# Change the first instruction of the commands from 1 to 2. Now the game will actually run.
# when the game actually runs you need to provide inputs to steer the paddle. whenever the computer
# requests you to provide an input, you can chose to provide
# -  0: the paddle remains in position
# - -1: move the paddle to the left
# - +1: move the paddle to the right
#
# the game also outputs a score. when an output triplet is in position (-1, 0) the third value of
# the triplet is not a tile type, but your current score.
# You need to beat the game by breaking all tiles without ever letting the ball cross the bottom 
# edge of the screen. What is your high-score at the end of the game? provide the score as part of your PR.
#
# BONUS: (no extra points, just for fun)
# make a movie of playing the game :)

# if game should be played automatically import computerSHauto; for my computer import computerAE
from computerSH import ExecutionManager, automated
from random import randint, seed
from colorama import Fore, Style
import os
from time import sleep

class GameManager():
    empty_tile = Fore.BLACK + "   " + Style.RESET_ALL
    block_colors = [Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX, Fore.CYAN]
    block_strings = ["███"]
    def __init__(self) -> None:
        self.board = [[self.empty_tile]]
        self.x_max = 0
        self.y_max = 0
        # only neccessary for automated playing
        self.ball_x_pos = 0
        self.paddle_x_pos = 0
        return
    
    def expandBoardX(self, max_index_x: int) -> None:
        expand_with = []
        for n in range(max_index_x - self.x_max):
            expand_with.append(self.empty_tile)
        for i in range(self.y_max + 1):
            row = self.board[i]
            row = row + expand_with.copy()
            self.board[i] = row
        self.x_max = max_index_x
        return
    
    def expandBoardY(self, max_index_y: int) -> None:
        row = []
        for n in range(self.x_max+1):
            row.append(self.empty_tile)
        for i in range(max_index_y - self.y_max):
            self.board.append(row.copy())
        self.y_max = max_index_y
        return
    
    def inputTriple(self, triplet: list[int, int, int]):
        if triplet[0] == -1:
            return
        match triplet[2]:
            case 0: # empty tile
                tile = self.empty_tile
            case 1: # wall
                tile = Fore.WHITE + "███" + Style.RESET_ALL
            case 2: # block
                color = self.block_colors[randint(0, len(self.block_colors)-1)]
                block = self.block_strings[randint(0, len(self.block_strings)-1)]
                tile = color + block + Style.RESET_ALL
            case 3: # paddle
                tile = Fore.MAGENTA + "███" + Style.RESET_ALL
                self.paddle_x_pos = triplet[0]
            case 4: # ball
                tile = Fore.YELLOW + " ● " + Style.RESET_ALL
                self.ball_x_pos = triplet[0]
            case _:
                return
        if triplet[0] > self.x_max:
            self.expandBoardX(triplet[0])
        if triplet[1] > self.y_max:
            self.expandBoardY(triplet[1])
        self.board[triplet[1]][triplet[0]] = tile
        return
    
    def printBoard(self) -> None:
        os.system('cls' if os.name=='nt' else 'clear')
        #print(self.board)
        for row in self.board:
            for tile in row:
                print(tile, end="")
            print()
        sleep(1/60) # match 60Hz display rate to minimize flickering
    
    def getBestMovement(self): # only for automated playing
        if self.ball_x_pos < self.paddle_x_pos:
            return -1
        elif self.ball_x_pos == self.paddle_x_pos:
            return 0
        elif self.ball_x_pos > self.paddle_x_pos:
            return 1


script_dir = os.path.dirname(os.path.abspath(__file__))
sequence_path = os.path.join(
    script_dir, "breakout_commands.txt"
)

with open(sequence_path) as file:
    memorylist = []
    for line in file:
        memorylist.append(int(line.rstrip()))
    memory_executer = ExecutionManager(memorylist)
game = GameManager()

if automated is True:
    triplet = memory_executer.computeToNextTriplet(0)
else:
    triplet = memory_executer.computeToNextTriplet()
# seed(42)

while True:
    game.inputTriple(triplet)
    game.printBoard()
    if automated is True:
        triplet = memory_executer.computeToNextTriplet(game.getBestMovement())
    else:
        triplet = memory_executer.computeToNextTriplet()
    if triplet == []: # if game is finished empty triplets are outputed
        break
    if triplet[0] == -1:
        score = triplet[2]
print(score)
# highscore: 17159
