import time
import copy
import os
import ast

from random import shuffle


def validate(board):
    ''' Sudoku board solver function '''

    # Initalising a row, col, and num array for each section within a sudoku puzzle
    # The index value will represent the number, so if index 2 is set to false then the number 3 is being used for the specific section of the puzzle
    row = [[[True] for i in range(9)] for j in range(9)]
    col = [[[True] for i in range(9)] for j in range(9)]
    box = [[[True] for i in range(9)] for j in range(9)]
    empty = []
    nums = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    for i in range(9):
            for j in range(9):
                if board[i][j] != '.':
                    num = int(board[i][j]) - 1
                    row[i][num] = col[j][num] = box[i//3*3+j//3][num] = False
                else:
                    empty.append((i, j))

    # Recusrive function solves the sudoku through checking all possible values avilable between 1-9 untill every value is filled
    def backtrack():
        # Return when there is no more coordinates left
        if not empty: 
            return True

        # Extract the coordiantes from the empty array
        i, j = empty.pop()
        # Shuffle the nums value to get a random order rather than a standard incremental order
        shuffle(nums)
        for num in nums:
            # If the num value is True in the three arrays row, col, and num then placing the number in that space would be a valid sudoku move
            if row[i][num] and col[j][num] and box[i//3*3+j//3][num]:
                # Edits the board value and sets the arrays to False
                board[i][j] = str(num+1)
                row[i][num] = col[j][num] = box[i//3*3+j//3][num] = False
                # Recurssively calls itself
                if backtrack():
                    return True
                # If the program backtracks then it indicates that all other moves following this one were unsucessfull so this will have to be altered
                board[i][j] = '.'
                row[i][num] = col[j][num] = box[i//3*3+j//3][num] = True
        
        # If none of the other number in the for loop are validate, then the program will add the coordinates back to the empty array and backtrack further
        empty.append((i, j))
        return False
    if backtrack():
        return True


def find_valid_solution(remove_amount, nums, amount_removed, sudoku_board, solution_count, puzzle):
    ''' Sudoku puzzle generator '''

    # When the amount of numbers removed from the board matches the amount required the program will back out
    if amount_removed == remove_amount:
        puzzle.append(sudoku_board)
        return True
    
    if not nums:
        # All of the nums have been used without matching the remove amount, then just return to try backtrack to other possibilities
        return

    # A random value from the scrambled nums array (0-80) will be removed from the board to test for a valid sudoku
    n = nums[0]
    row = n // 9
    col = n % 9
    val = sudoku_board[row][col]
    sudoku_board[row][col] = "."

    # Solution count will be set to 0, and as a list it can be manipulated and maintained when recursively calling
    solution_count[0] = 0
    # If this function returns True then multiple solutions have been found for the board
    if validate_multiple_solutions(sudoku_board.copy(), solution_count):
        # The value will be added back and will call the function again skipping it
        sudoku_board[row][col] = val
        if find_valid_solution(remove_amount, nums[1:].copy(), amount_removed, sudoku_board.copy(), solution_count, puzzle):
            return True
    else:
        # If there is only one solution recursively call with removing that value, and with keeping that value
        if find_valid_solution(remove_amount, nums[1:].copy(), amount_removed+1, sudoku_board.copy(), solution_count, puzzle):
            return True
        sudoku_board[row][col] = val
        if find_valid_solution(remove_amount, nums[1:].copy(), amount_removed, sudoku_board.copy(), solution_count, puzzle):
            return True



def validate_multiple_solutions(board, solution_count):
    ''' Validates the sudoku board ensuring there is only 1 valid solution '''

    row = [[[True] for i in range(9)] for j in range(9)]
    col = [[[True] for i in range(9)] for j in range(9)]
    box = [[[True] for i in range(9)] for j in range(9)]
    empty = []

    for i in range(9):
            for j in range(9):
                if board[i][j] != '.':
                    num = int(board[i][j]) - 1
                    row[i][num] = col[j][num] = box[i//3*3+j//3][num] = False
                else:
                    empty.append((i, j))

    def backtrack_multiple_solutions():
        # If the empty array has no value then a sucessfull solution has been found
        if not empty: 
            solution_count[0] += 1
            # If the solution count is 2 then it indicates that the board has multiple valid solutions and is not a valid sudoku puzzle
            if solution_count[0] == 2:
                return True
            else:
                return 

        i, j = empty.pop()
        # Solves the sudoku board using a standard recursive backtracking approach
        for num in range(9):
            if row[i][num] and col[j][num] and box[i//3*3+j//3][num]:
                board[i][j] = str(num+1)
                row[i][num] = col[j][num] = box[i//3*3+j//3][num] = False
                if backtrack_multiple_solutions():
                    return True
                board[i][j] = '.'
                row[i][num] = col[j][num] = box[i//3*3+j//3][num] = True

        empty.append((i, j))
        # If the final return is False then it indicates that all possibilities have been tested any only 1 valid sudoku has been found
        # As each board started as a completed sudoku puzzle there is not a possibility that 0 solutions were found
        return False

    return backtrack_multiple_solutions()


def make_board(remove_amount, solved_game_full_name, fresh_game_full_name):
    ''' Creator function of full sudoku puzzle  '''

    # Variables track the fully solved board and amount of numbers removed
    amount_removed = 0
    solved_board = []

    # While the currrent amount removed is not equal to amount needed it will continue to remove numbers
    while amount_removed != remove_amount:
        amount_removed = 0

        nums = [i for i in range(81)]
        solution_count = [0]
        shuffle(nums)
        puzzle = []
        # Initial board is generated blank
        board = [[".",".",".",".",".",".",".",".","."],
                [".",".",".",".",".",".",".",".","."],
                [".",".",".",".",".",".",".",".","."],
                [".",".",".",".",".",".",".",".","."],
                [".",".",".",".",".",".",".",".","."],
                [".",".",".",".",".",".",".",".","."],
                [".",".",".",".",".",".",".",".","."],
                [".",".",".",".",".",".",".",".","."],
                [".",".",".",".",".",".",".",".","."]]
        
        # This function will generate a fully complted sudoku puzzle
        validate(board)

        # This function will create a playable version of the game with the amount of removed numbers specified
        find_valid_solution(remove_amount, nums, 0, board, solution_count, puzzle)

        # Tracks the amount of digits removed from the board
        for i in puzzle:
            for j in i:
                for dig in j:
                    if not dig.isdigit():
                        amount_removed += 1

    # A deep copy of the board is made to prevent later mutation of the solved copy
    solved_board = copy.deepcopy(board)

    # Ensures that the board is valid
    if not validate(solved_board):
        validate(solved_board)
    
    # Writes the unsolved version of the board to a file
    with open(fresh_game_full_name, "a") as file:
        file.write(str(board))
        file.write("\n")

    # Writes the solved verson of the board to a file
    with open(solved_game_full_name, "a") as file:
        file.write(str(solved_board))
        file.write("\n")

    # Calls the play game function with the unsolved and solved versions of the board
    play_game(solved_board, board)

def play_game(solved_board, board):
    ''' User playing function of sudoku board '''

    print("Would you like to set time limit to complete the board? (1-Yes, 2-No)")
    time_limit = None

    # Loop untill an accepted value is input
    while True:
        set_time_limit = input("Enter value: ")
        # Quits the program
        if set_time_limit == "quit":
            print("Quitting")
            time.sleep(5)
            quit()

        # Checks the value is a digit and within boundaries
        if not set_time_limit.isdigit() or (int(set_time_limit) < 1 or int(set_time_limit) > 2):
            print("Please enter a valid number (1-Yes 2-No)")
            continue
        
        if set_time_limit == "1":
            print("How long would you like to set the timer for (minutes)")
            while True:
                time_limit = input("Enter value: ")
                if not time_limit.isdigit():
                    print("Please enter a valid number")
                    continue
                else:
                    break
            break

        elif set_time_limit == "2":
            print("No time limit set")
            break
    
    # If a time limit has been specified the current time will be evaluated and an end time will be calculated
    if time_limit:
        start_time = time.time()
        end_time = start_time + (int(time_limit) * 60)

    # Prints the inital board for the user to solve
    for i in board:
        print(i)

    # Initalises list for the undo and redo features
    prev_moves = []
    redo_moves = []

    # The loop will continue while the current board is not equal to the fully solved board
    while solved_board != board:
        # Gets the row number
        while True:
            # Checks if time limit is valid
            if time_limit:
                if time.time() > end_time:
                    print("Out of time!")
                    time.sleep(5)
                    quit()

            edit_row = input("Enter the row: ")
            # Quits the program
            if edit_row == "quit":
                print("Quitting")
                time.sleep(5)
                quit()

            # Undo
            if edit_row == "undo":
                # Checks for previous moves
                if prev_moves:
                    print("Undoing pervious move")
                    undo_edit_row, undo_edit_col, undo_edit_num = prev_moves.pop()

                    # Stores info on effected cell increase it needs to be redone later
                    redo_num = board[undo_edit_row][undo_edit_col]
                    redo_moves.append([undo_edit_row, undo_edit_col, redo_num])

                    # Updates the board to undo value
                    board[undo_edit_row][undo_edit_col] = undo_edit_num
                    for i in board:
                        print(i)
                    continue
                else:
                    print("No previous move to undo")
                    continue

            # Redo
            if edit_row == "redo":
                # Checks for any redo moves
                if redo_moves:
                    print("Redoing pervious move")

                    redo_edit_row, redo_edit_col, redo_edit_num = redo_moves.pop()

                    # Stores the current cell for a later undo if needed
                    prev_num = board[redo_edit_row][redo_edit_col]
                    prev_moves.append([redo_edit_row, redo_edit_col, prev_num])

                    # Updates the board to the redo value
                    board[redo_edit_row][redo_edit_col] = redo_edit_num
                    for i in board:
                        print(i)
                    continue
                else:
                    print("No previous move to redo")
                    continue
            
            # Checks if the input is not a valid number
            if not edit_row.isdigit() or (int(edit_row) < 1 or int(edit_row) > 9):
                print("Please enter a valid row number (1-9)")
            # If valid then it sets the input for the row
            else:
                edit_row = int(edit_row)-1
                break

        # Gets the column number
        while True:
            # Checks if time limit is valid
            if time_limit:
                if time.time() > end_time:
                    print("Out of time!")
                    time.sleep(5)
                    quit()

            edit_col = input("Enter the column: ")
            # Quits the program
            if edit_col == "quit":
                print("Quitting")
                time.sleep(5)
                quit()

            # Undo
            if edit_col == "undo":
                # Checks for previous moves
                if prev_moves:
                    print("Undoing pervious move")
                    undo_edit_row, undo_edit_col, undo_edit_num = prev_moves.pop()

                    # Stores info on effected cell increase it needs to be redone later
                    redo_num = board[undo_edit_row][undo_edit_col]
                    redo_moves.append([undo_edit_row, undo_edit_col, redo_num])

                    # Updates the board to undo value
                    board[undo_edit_row][undo_edit_col] = undo_edit_num
                    for i in board:
                        print(i)
                    continue
                else:
                    print("No previous move to undo")
                    continue

            # Redo
            if edit_col == "redo":
                # Checks for any redo moves
                if redo_moves:
                    print("Redoing pervious move")

                    redo_edit_row, redo_edit_col, redo_edit_num = redo_moves.pop()

                    # Stores the current cell for a later undo if needed
                    prev_num = board[redo_edit_row][redo_edit_col]
                    prev_moves.append([redo_edit_row, redo_edit_col, prev_num])

                    # Updates the board to the redo value
                    board[redo_edit_row][redo_edit_col] = redo_edit_num
                    for i in board:
                        print(i)
                    continue
                else:
                    print("No previous move to redo")
                    continue
            
            # Checks if the input is not a valid number
            if not edit_col.isdigit() or (int(edit_col) < 1 or int(edit_col) > 9):
                print("Please enter a valid column number (1-9)")
            # If valid then it sets the input for the row
            else:
                edit_col = int(edit_col)-1
                break
        
        # Gets the value number
        while True:
            # Checks if time limit is valid
            if time_limit:
                if time.time() > end_time:
                    print("Out of time!")
                    time.sleep(5)
                    quit()

            edit_num = input("Enter the new number: ")
            # Quits the program
            if edit_num == "quit":
                print("Quitting")
                time.sleep(5)
                quit()
            
            # Undo
            if edit_num == "undo":
                # Checks for previous moves
                if prev_moves:
                    print("Undoing pervious move")
                    undo_edit_row, undo_edit_col, undo_edit_num = prev_moves.pop()

                    # Stores info on effected cell increase it needs to be redone later
                    redo_num = board[undo_edit_row][undo_edit_col]
                    redo_moves.append([undo_edit_row, undo_edit_col, redo_num])

                    # Updates the board to undo value
                    board[undo_edit_row][undo_edit_col] = undo_edit_num
                    for i in board:
                        print(i)
                    continue
                else:
                    print("No previous move to undo")
                    continue

            # Redo
            if edit_num == "redo":
                # Checks for any redo moves
                if redo_moves:
                    print("Redoing pervious move")

                    redo_edit_row, redo_edit_col, redo_edit_num = redo_moves.pop()

                    # Stores the current cell for a later undo if needed
                    prev_num = board[redo_edit_row][redo_edit_col]
                    prev_moves.append([redo_edit_row, redo_edit_col, prev_num])

                    # Updates the board to the redo value
                    board[redo_edit_row][redo_edit_col] = redo_edit_num
                    for i in board:
                        print(i)
                    continue
                else:
                    print("No previous move to redo")
                    continue

            # Checks if the input is not a valid number
            if not edit_num.isdigit() or (int(edit_num) < 1 or int(edit_num) > 9):
                print("Please enter a valid column number (1-9)")
            else:
                break
        
        # Sets the previous move if needed to undo later
        prev_num = board[edit_row][edit_col]
        prev_moves.append([edit_row, edit_col, prev_num])

        # Edits the board with the new num at the new row and col
        board[edit_row][edit_col] = edit_num

        # Reset redo moves as a new move has been made
        redo_moves.clear()

        # Prints new version of the board
        for i in board:
            print(i)

    # Displays message as the board is completed
    print("Well Done! Board Complete!")
    time.sleep(5)


def make_dir():
    ''' Established directory and files for saving prior games '''

    # Gets the current directory of the program
    cwd = os.getcwd()
    dir = os.path.join(cwd, "Games")

    # If the directory doesn't already exists it will be created
    if not os.path.isdir(dir):
        os.mkdir(dir)
    
    # Creates file for solved games in directory if it doesn't exist
    solved_games_file_name = "solved_games.txt"
    solved_games_full_name = os.path.join(dir, solved_games_file_name)
    if not os.path.exists(solved_games_full_name):
        file = open(solved_games_full_name, "a")
        file.close()

    # Creates file for fresh games in directory if it doesn't exist
    fresh_games_file_name = "fresh_games.txt"
    fresh_games_full_name = os.path.join(dir, fresh_games_file_name)
    if not os.path.exists(fresh_games_full_name):
        file = open(fresh_games_full_name, "a")
        file.close()

    # Returns full paths for solved and fresh games
    return solved_games_full_name, fresh_games_full_name

def setup():
    ''' Beginning of the program contains information needed during the setup process '''

    # Welcome messages
    print("Welcome to Sudoku!\n")
    print("Type \'undo\' to undo your previous move")
    print("Type \'redo\' to revert your previous undo")
    print("Type \'quit\' to quit the game\n")
    
    def select_game():
        print("Please enter if you would like to play a new game or repeat an old game")
        print("New game - 1")
        print("Old game - 2")

        # Loops untill a valid input
        while True:
            game_choice = input("Select game type: ")
            # Quits game
            if game_choice == "quit":
                print("Quitting")
                time.sleep(5)
                quit()
            # Checks input is within boundaries
            if not game_choice.isdigit() or (int(game_choice) <1 or int(game_choice) > 2):
                print("Please enter a valid number")
                continue
            else:
                if game_choice == '1':
                    return 1
                elif game_choice == '2':
                    return 2
    
    def new_game(solved_game_full_name, fresh_game_full_name):
        print("A puzzle will be generated depending on your chosen difficulty \n")
        print("Please enter the number for the difficulty of puzzle you would like to solve")
        print("Easy - 1")
        print("Medium - 2")
        print("Hard - 3")

        remove_amm = 0

        while True:
            difficulty = input("Select difficulty: ")
            # Quits game
            if difficulty == "quit":
                print("Quitting")
                time.sleep(5)
                quit()
            # Checks input is within boundaries
            if not difficulty.isdigit() or (int(difficulty) <1 or int(difficulty) > 3):
                print("Please enter a valid number")
                continue
            # Sets the amount of cells to remove based on the selected difficulty
            else:
                if difficulty == '1':
                    remove_amm = 15
                elif difficulty == '2':
                    remove_amm = 30
                elif difficulty == '3':
                    remove_amm = 40
                break
        # Calls function to create board
        make_board(remove_amm, solved_game_full_name, fresh_game_full_name)
    
    def old_game(solved_game_full_name, fresh_game_full_name):
        # Read the number of games saved in the file
        file = open(fresh_game_full_name, "r")
        file_len = len(file.readlines())
        file.close()

        # If no games are saved then the program will exit out
        if file_len == 0:
            print("No previous games to replay")
            time.sleep(5)
            quit()
        # If only 1 game is saved then that will be played automatically
        elif file_len == 1:
            print("Only 1 previous game recorded")
            game_no = 1
        # If multiple games are saved then the user will be allowed to select which game to play
        else:
            print(f"Which previous game would you like to play? (1-{file_len})")
            game_no = ""
            while True:
                game_no = input("Select game: ")
                # Quit game
                if game_no == "quit":
                    print("Quitting")
                    time.sleep(5)
                    quit()
                # Checks if input is a valid number
                if not game_no.isdigit() or (int(game_no) <1 or int(game_no) > file_len):
                    print("Please enter a valid number")
                    continue
                else:
                    break
        
        
        # Variables for retreiving the unsolved and solved version of the game are initalised
        game = []
        solved_game = []

        game_board = ""
        solved_game_board = ""

        # Reads the unplayed version of the selected game
        with open(fresh_game_full_name, "r") as file:
            for i, line in enumerate(file):
                # When the counter (i) is equal to the game then that line will be used
                if i == int(game_no)-1:
                    game.append(line)

            # Edits the string and removes the \n command at the ending
            replay_game = game[0]
            replay_game = replay_game[0:-1]
            game_board = replay_game
        
        # Reads the solved version of the selected game
        with open(solved_game_full_name, "r") as file:
            for i, line in enumerate(file):
                # When the counter (i) is equal to the game then that line will be used
                if i == int(game_no)-1:
                    solved_game.append(line)
            
            # Edits the string and removes the \n command at the ending
            replay_solved_game = solved_game[0]
            replay_solved_game = replay_solved_game[0:-1]
            solved_game_board = replay_solved_game

        # Evaluates both games as a list rather than a string so they can be manipulated and played
        list_game_board = ast.literal_eval(game_board)
        list_solved_game_board = ast.literal_eval(solved_game_board)

        # Calls function to play game with the solved and unsolved version of the game
        play_game(list_solved_game_board, list_game_board)
    
    # File paths of solved and unsolved games are returned from the function
    solved_game_full_name, fresh_game_full_name = make_dir()

    # The new or old game is dependent on the user selected value
    difficulty_choice = select_game()
    if difficulty_choice == 1:
        new_game(solved_game_full_name, fresh_game_full_name)
    else:
        old_game(solved_game_full_name, fresh_game_full_name)

# Boiler plate  
if __name__ == "__main__":
    setup()