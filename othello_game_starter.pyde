from board import Board
from disk import Disk
from game_controller import GameController
from player import Player
from ai import AI


WIDTH = 800
HEIGHT = 800
CELL_SIZE = 100
N = HEIGHT / CELL_SIZE
lock = False # if the player or AI is setting a disk, lock the board
prompt_flag = True

gc = GameController(WIDTH, HEIGHT)
board = Board(WIDTH, HEIGHT, CELL_SIZE, N, gc)
player = Player(board)
ai = AI(board)


def setup():
    size(WIDTH, HEIGHT)
    print("------------------------------------------------------")
    print("When the game ends, press any key to record your score")
    print("------------------------------------------------------")
    print("It's your turn")


def draw():
    # draw lines
    background(9, 105, 31)
    strokeWeight(3)
    for i in range(N - 1):
        line(0, CELL_SIZE * (i + 1), WIDTH, CELL_SIZE * (i + 1))
        line(CELL_SIZE * (i + 1), 0, CELL_SIZE * (i + 1), HEIGHT)

    # display the disks
    board.display()
    gc.update()

        
def keyPressed():
    #press any key to record your score

    if (game_end and prompt_flag):
        record_score()

def mousePressed():
    # click the mouse to place your disk

    global lock
    if (game_end() or lock):
        return
    if board.if_disk_black:
        lock = True
        if (player.set_disk(mouseX, mouseY)):
            if (board.if_disk_black):
                print("It's your turn")
            else:
                print("It's AI's turn")
        lock = False
        
    


def mouseReleased():
    # release the mouse for AI to place the disk

    global lock
    if (game_end() or lock):
        return
    if not board.if_disk_black:
        lock = True

        # produce a delay to mimic the thinking process of AI
        delay = 50000000
        while(delay > 0):
            delay -=1
        best_step = ai.find_best_legal_step()
        if (ai.set_disk(best_step[0], best_step[1])):
            print("It's your turn")

        lock = False

    

def record_score():
    # record the score only once

    global prompt_flag

    prompt_flag = not prompt_flag
    try:
        filename = "scores.txt"
        file = open(filename, "r")
    except FileNotFoundError as e:
        print("cannot open", filename)
        return
    
    name = input("enter your name")
    while (not name):
        name = input("enter your name")

    first_line = file.readline()
    file.close()
    name_score = first_line.strip().split(" ")
    max_score = 0
    if (name_score[-1]):
        max_score = int(name_score[-1])

    new_record = name + " " + str(gc.black_cnt)
    if(gc.black_cnt > max_score):
        file = open(filename, "r+")
        first_line = file.read()
        file.seek(0, 0)
        file.write(new_record + "\n" + first_line)
    else:
        file = open(filename, "a")
        file.write(new_record + "\n")
    file.close()


def game_end():
    # return True if game ends, False otherwise
    return gc.white_win or gc.black_win or gc.draw


def input(message=''):
    from javax.swing import JOptionPane
    return JOptionPane.showInputDialog(frame, message)
