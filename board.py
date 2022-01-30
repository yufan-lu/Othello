from disk import Disk


class Board:
    """Board class(singleton)"""
    def __init__(self, WIDTH, HEIGHT, CELL_SIZE, N, game_controller):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.CELL_SIZE = CELL_SIZE
        # disks of N x N
        self.disks = [[None for _ in range(N)] for _ in range(N)]
        # current color of the disk to be placed at the board
        self.if_disk_black = True
        # init number of disks
        self.disk_cnt = 4
        # init number of black disks
        self.blk_cnt = 2
        # init number of white disks
        self.wht_cnt = 2
        # number of cells per row/column
        self.N = N
        # game controller, singleton
        self.gc = game_controller
        # if no_legal_step_cnt == 2(no legal step for both AI and player),
        # the game ends
        self.no_legal_step_cnt = 0
        # 8 directions to search
        self.dirs = [[-1, 0], [1, 0], [0, -1], [0, 1],
                     [-1, -1], [-1, 1], [1, -1], [1, 1]]

        # init disks, filling the central tiles with 2 blk and 2 wht disks
        if (self.N >= 2):
            init_idx = self.N // 2 - 1
            self.disks[init_idx][init_idx] =\
                Disk(False, init_idx, init_idx, self.CELL_SIZE)
            self.disks[init_idx][init_idx + 1] =\
                Disk(True, init_idx, init_idx + 1, self.CELL_SIZE)
            self.disks[init_idx + 1][init_idx + 1] = \
                Disk(False, init_idx + 1, init_idx + 1, self.CELL_SIZE)
            self.disks[init_idx + 1][init_idx] = \
                Disk(True, init_idx + 1, init_idx, self.CELL_SIZE)

    def set_disk(self, x, y):
        """
        1. Given a coordinate(x, y) of the board, transform it
        to (row, col) and check if this is a legal step.
        2. Return False if not legal; otherwise, place this disk at the board,
        and flip the disks with inverse color accoring to the rule.
        3. Check if there exist legal steps for the rival. If not, switch back
        to the current player.
        4. Check if there exist legal steps for the current player
        5. Call check_winner() to verify if the game reach the end
        6. Return True if this operation is legal.
        """
        col = x // self.CELL_SIZE
        row = y // self.CELL_SIZE
        if (not self.legal(row, col)):
            return False
        self.no_legal_step_cnt = 0
        self.disks[row][col] = Disk(self.if_disk_black,
                                    row, col, self.CELL_SIZE)
        self.disk_cnt += 1
        if (self.if_disk_black):
            self.blk_cnt += 1
        else:
            self.wht_cnt += 1
        self.flip(row, col)
        if (not self.legal_steps):
            self.no_legal_step_cnt += 1
        self.if_disk_black = not self.if_disk_black
        if (not self.legal_steps):
            self.no_legal_step_cnt += 1
            print("no more step for " +
                  ("you" if self.if_disk_black else "AI"))
            self.if_disk_black = not self.if_disk_black
            if(self.no_legal_step_cnt != 2 and self.if_disk_black is False):
                print("Please click to wake up AI")
        self.check_winner()
        return True

    def flip(self, row, col):
        """flip all the disks with inverse color at 8 directions
        accoring to the rule"""
        for dir in self.dirs:
            self.flip_helper(row + dir[0], col + dir[1], dir[0], dir[1])

    def flip_helper(self, row, col, row_add, col_add):
        """a helper method for flip(), using recursion"""
        if (self.out_of_idx(row, col) or not self.disks[row][col]):
            return False
        if (self.disks[row][col].if_black == self.if_disk_black):
            return True
        next_row = row + row_add
        next_col = col + col_add
        if (self.flip_helper(next_row, next_col, row_add, col_add)):
            self.disks[row][col].flip()
            blk_add = -1
            if (self.if_disk_black):
                blk_add = 1
            self.blk_cnt += blk_add
            self.wht_cnt -= blk_add
            return True
        return False

    def legal(self, row, col):
        """determine if a set_disk operation is legal"""
        legal_steps = self.legal_steps
        if ((row, col) in legal_steps and self.disks[row][col] is None):
            return True
        return False

    @property
    def legal_steps(self):
        """return a set of all current legal steps"""
        steps = set()
        for row in range(self.N):
            for col in range(self.N):
                disk = self.disks[row][col]
                if (disk is None):
                    for dir in self.dirs:
                        row_add = dir[0]
                        col_add = dir[1]
                        next_row = row + row_add
                        next_col = col + col_add
                        if self.out_of_idx(next_row, next_col):
                            continue
                        if self.disks[next_row][next_col]:
                            if self.if_disk_black !=\
                             self.disks[row + row_add][col + col_add].if_black:
                                if(self.legal_steps_helper(next_row, next_col,
                                   row_add, col_add)):
                                    steps.add((row, col))
                                    break
        return steps

    def legal_steps_helper(self, row, col, row_add, col_add):
        """a helper method for legal_steps(), using recursion"""
        if (self.out_of_idx(row, col) or self.disks[row][col] is None):
            return False
        if (self.disks[row][col].if_black == self.if_disk_black):
            return True
        return self.legal_steps_helper(row + row_add, col + col_add,
                                       row_add, col_add)

    @property
    def best_legal_step(self):
        """return the best legal step currently.
        Best means largest number of disks to flip"""
        legal_steps = self.legal_steps
        best_step = None
        max_cnt = 0
        for step in legal_steps:
            cnt = 0
            for dir in self.dirs:
                row = step[0] + dir[0]
                col = step[1] + dir[1]
                if (self.legal_steps_helper(row, col, dir[0], dir[1])):
                    cnt += self.best_legal_step_helper(row, col,
                                                       dir[0], dir[1])
            if (cnt > max_cnt):
                max_cnt = cnt
                best_step = step
        return best_step

    def best_legal_step_helper(self, row, col, row_add, col_add):
        """a helper method for best_legal_step(), using recursion"""
        if (self.disks[row][col].if_black == self.if_disk_black):
            return 0
        return 1 + self.best_legal_step_helper(row + row_add, col + col_add,
                                               row_add, col_add)

    def out_of_idx(self, row, col):
        """given a pair of index(row, col),
        return True if it is illegal to
        access self.disks[row][col] with them"""
        return row < 0 or col < 0 or row >= self.N or col >= self.N

    def check_winner(self):
        """check if the game reachs the end"""
        if (self.disk_cnt == self.N * self.N or (self.no_legal_step_cnt == 2)):
            self.gc.black_cnt = self.blk_cnt
            self.gc.white_cnt = self.wht_cnt
            if (self.blk_cnt > self.wht_cnt):
                self.gc.black_win = True
            elif (self.blk_cnt < self.wht_cnt):
                self.gc.white_win = True
            else:
                self.gc.draw = True

    def display(self):
        """display all the disks at the board"""
        for disk_line in self.disks:
            for disk in disk_line:
                if (disk):
                    disk.display()
