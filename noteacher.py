import random
import copy
import numpy as np

### Generates new reset Boards for fresh games 
def board_generator():
    board = [[None, None, None],
             [None, None, None],
             [None, None, None]]
    return board


### Printing the layout for viewing the board states
def print_board(board):               
    for i in range(3):
        print(f"{board[i][0]}\t|{board[i][1]}\t|{board[i][2]}")
        

### Fetching rows, colums and diagnals
def fetcher(board):
    rows = []                         # a list of collections of individual rows
    columns = []                      # a list of collections of individual columns
    diagnals  = []                    # a list of collections of individual diagonals 
    
    row1 = []
    row2 = []
    row3 = []
    
    column1 = []
    column2 = []
    column3 = []
    
    diagnal1 = []
    diagnal2 = []
    for i in range(3):
        row1.append(board[0][i])
        row2.append(board[1][i])
        row3.append(board[2][i])
        
        column1.append(board[i][0])
        column2.append(board[i][1])
        column3.append(board[i][2])
        
        diagnal1.append(board[i][i])
        diagnal2.append(board[i][2-i])
    rows.append(row1)   
    rows.append(row2)
    rows.append(row3)
    columns.append(column1)
    columns.append(column2)
    columns.append(column3)
    diagnals.append(diagnal1)
    diagnals.append(diagnal2)
    win_pos = []
    win_pos = rows + columns + diagnals
    return rows, columns, diagnals, win_pos

### Determining whether a game is finished or done playing
def finish(board):                   # Checking whether the game is finished(win, lose, draw) or still continuing 
    fin = True
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                fin = False          # The game isn't finished if the places in the game grid is not filled
                # print("None detected")
                break
    
    _, _, _, w = fetcher(board)      # w: The collection of rows, columns and diagonals 
    nones = 0                        # nones: Will contain the number of places left to fill with 'x' or 'o' in a certain row, column or diagonal
    xs = 0                           # xs: Will contain the number of 'x' in a certain row, column, or diagonal
    os = 0                           # os: Will contain the number of 'o' in a certain row, column, or diagonal
    for items in w:
        # print(items)
        for i in items:
            if i == None:
                nones += 1
            elif i == 'x':
                xs += 1
            elif i == 'o':
                os += 1

        if xs == 3:      # If there is 3 'x's or 3 'o's in a row, column or diagonal, The game is won, hence fin =  True
            fin = True
            return [fin, 'x']
        elif os == 3:
            fin  = True
            return [fin, 'o']
        nones = 0
        xs = 0
        os = 0
    return [fin, ""]


### Determining the parameters for the target function or actual function representation
#-------------------------------------------------------------------#
#The following parameters are used to make the target function
#1) x1 = When there is only an 'x' in the entire row, column or diagonal
#2) x2 = When there is only an 'o' in the entire row, column or diagonal
#3) x3 = When there are 2 'x's in the row, column or diagonal
#4) x4 = When there are 2 'o's in the row, column or diagonal
#5) x5 = When there are 3 'x's in the row, column or diagonal
#6) x6 = When there are 3 'o's in the row, column or diagonal
def parameters(board):
    _, _, _, w = fetcher(board)
    nones = 0                        # nones: Will contain the number of places left to fill with 'x' or 'o' in a certain row, column or diagonal
    xs = 0                           # xs: Will contain the number of 'x' in a certain row, column, or diagonal
    os = 0                           # os: Will contain the number of 'o' in a certain row, column, or diagonal
    x1, x2, x3, x4, x5, x6 = 0,0,0,0,0,0
    for items in w:
        # print(items)
        for i in items:
            if i == None:
                nones += 1
            elif i == 'x':
                xs += 1
            elif i == 'o':
                os += 1
        # print(nones, xs, os)
        if xs == 1 and nones == 2:
            x1 += 1
        if os == 1 and nones == 2:
            x2 += 1
        if xs == 2 and nones == 1:
            x3 += 1
        if os == 2 and nones == 1:
            x4 += 1
        if xs == 3 and nones == 0:
            x5 += 1
        if os == 3 and nones == 0:
            x6 += 1
        nones = 0
        xs = 0
        os = 0
    return x1, x2, x3, x4, x5, x6     # Getting the parameter values 

### Defining the play function for both the computer(Bot)  and user
def play(board, player, smart, weights, user_mode=False):
    if smart:                                       # The argument for the computer is to be Smart: smart= True
        best_board = smart_move(board, player, weights)
        return best_board
    elif not smart and not user_mode:                                    # The argument for the user is to be Weak: smart= False
        random_board = random_move(board, player)
        return random_board
    elif not smart and user_mode:
        user_board = user_in(board, player)        
        return user_board


## Gives us all possible next board states 
def get_next_states(board, player):                         #
    options = []
    board_possibilities = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                options.append((i,j))
    for i in options:
        bb = copy.deepcopy(board)
        bb[i[0]][i[1]] = player
        board_possibilities.append(bb)
    return board_possibilities                              # Returns a list containing all the possible next board states for that state


### Determines the best possible next state
def get_best_next_state(board_possibilities, weights, player):
    best_val = -float('inf')
    for board_idx in range(len(board_possibilities)):
        v = v_calculate(board_possibilities[board_idx], weights)
        if v > best_val:
            best_val = v
            best_board_idx = board_idx  
    return board_possibilities[best_board_idx]              # Returns the best next board out of all the possible next state boards 
    

### Defines How the player can make ramdom moves to play(Not used, just implemented to check how the computer improves)
def random_move(board, player):
    board_states = get_next_states(board, player)
    # print(len(board_states))
    i = np.random.choice(len(board_states))
    board_chosen = board_states[i]
    return board_chosen
    

### Getting the User to play with the computer    
def user_in(board, player):                                 
    options = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                options.append((i,j))
    
    print(f"Please select index of the tuple you want to choose as your position.\n {options}\n")
    while True:
        try:
            row = int(input("Row # ->"))
            col = int(input("Col # ->"))
    
            if (row, col) in options:
                break
            else:
                print("Invalid input, try again\n")    
        except ValueError:
            print("Invalid input, try again\n")

    # print(options[ent][0])            # Now will assign 'x' or 'o' to the chosen place in the board
    board[row][col] = player
    return board
    
### Getting the computer to play with the user
def smart_move(board, player, weights):
    board_states = get_next_states(board, player)
    best_board = get_best_next_state(board_states, weights, player)
    return best_board


### Calculates the value of the current board states given the weights
def v_calculate(board, weights):
    x1, x2, x3, x4, x5, x6 = parameters(board=board)
    v = weights[0] + x1*weights[1] + x2*weights[2] + x3*weights[3] + x4*weights[4] + x5*weights[5] + x6*weights[6]
    return v


def generate_training_data(history, weights, player):
    training_data = []
    
    for i in range(len(history)):
        done, winner = finish(history[i])
        x1, x2, x3, x4, x5, x6 = parameters(board=history[i])
        
        if player == "x":
            # Data and their corresponding target values for all the intermediate board states in history
            if not done:
                if i+1 < len(history):
                    x1_next, x2_next, x3_next, x4_next, x5_next, x6_next = parameters(board=history[i+1]) # Value of next best states (history+1 since they are stored sequentially)
                    v = weights[0] + x1_next*weights[1] + x2_next*weights[2] + \
                        x3_next*weights[3] + x4_next*weights[4] + \
                        x5_next*weights[5] + x6_next*weights[6]
            # Data and their corresponding target values for all the terminal board states in history
            elif done:
                if winner == 'x':
                    v = 100
                elif winner == 'o':
                    v = -100
                else:
                    v = 0
            training_data.append([[x1, x2, x3, x4, x5, x6], v])
            
        elif player == "o":
            # Data and their corresponding target values for all the intermediate board states in history
            if not done:
                if i+1 < len(history):
                    x1_next, x2_next, x3_next, x4_next, x5_next, x6_next = parameters(board=history[i+1]) # Value of next best states (history+1 since they are stored sequentially)
                    v = weights[0] + x1_next*weights[1] + x2_next*weights[2] + \
                        x3_next*weights[3] + x4_next*weights[4] + \
                        x5_next*weights[5] + x6_next*weights[6]
            # Data and their corresponding target values for all the terminal board states in history
            elif done:
                if winner == 'o':
                    v = 100
                elif winner == 'x':
                    v = -100
                else:
                    v = 0
            training_data.append([[x1, x2, x3, x4, x5, x6], v])
    return training_data


def weights_update(training_data, history, weights, learning_rate):
    # para_list = [1, x1, x2, x3, x4, x5, x6]
    # print(len(training_data))
    # print(len(history))
    
    for i in range(len(history)):
        x1, x2, x3, x4, x5, x6 = parameters(history[i])
        
        # The actual values are calculated here and subtracted from the target values, after which they are incorporated in the LMS update rule
        weights[0] += learning_rate * ( training_data[i][1] - v_calculate(history[i], weights) )   
        weights[1] += learning_rate * ( training_data[i][1] - v_calculate(history[i], weights) ) * x1
        weights[2] += learning_rate * ( training_data[i][1] - v_calculate(history[i], weights) ) * x2
        weights[3] += learning_rate * ( training_data[i][1] - v_calculate(history[i], weights) ) * x3
        weights[4] += learning_rate * ( training_data[i][1] - v_calculate(history[i], weights) ) * x4
        weights[5] += learning_rate * ( training_data[i][1] - v_calculate(history[i], weights) ) * x5
        weights[6] += learning_rate * ( training_data[i][1] - v_calculate(history[i], weights) ) * x6
        
    return weights

### To reset the board after every episode(end of the game)      
def board_reset():
    board = board_generator()
    return board


###################################################################################################################################

def train_teacher():
    ### We will initialize variables to start playing the game
    player1 = 'x'
    player2 = 'o'   
    board = board_generator()   
    history = []
    wins = 0
    loses = 0
    draws = 0
    updated_weights1 = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]       # Intinially set the updated weights same as the initial weights
    updated_weights2 = [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]       # Intinially set the updated weights same as the initial weights
  
    toggler = True                                              # To toggle between players(so that one player does not get to play first always)


    ### Here the game starts 
    for episodes in range(10000):
        board = board_reset()                       # Resetting the board at the start of the game
        history = [copy.deepcopy(board)]            # Copying the first board state to the history
        
        # weights = [-73.47595694692075, -41.649746786866984, 22.638553051230602, -25.827020883461447, 67.03781313982053, 250.5271661068686, -129.3618938930254]
        weights1 = updated_weights1
        weights2 = updated_weights2
        
        while True:
            if toggler:
                board = play(board, player = player1, smart = toggler, weights = weights1, user_mode=False)  # Computer is playing
                history.append(copy.deepcopy(board))
                
                # print("Bot played")
                # print_board(board)
                # print()
                if finish(board)[0]:
                    break
                
                board = play(board, player = player2, smart = toggler, weights = weights2, user_mode=False)  # User is playing
                history.append(copy.deepcopy(board))
                # print("User played")
                # print_board(board)
                if finish(board)[0]:
                    break
            else:
                board = play(board, player = player2, smart = toggler, weights = weights2, user_mode=False)  # Computer is playing
                history.append(copy.deepcopy(board))
                
                # print("Bot played")
                # print_board(board)
                # print()
                if finish(board)[0]:
                    break
                
                board = play(board, player = player1, smart = toggler, weights = weights1, user_mode=False)  # User is playing
                history.append(copy.deepcopy(board))
                # print("User played")
                # print_board(board)
                if finish(board)[0]:
                    break
        
        toggler = not toggler                                                          # Condition to toggel between the computer and the user 
        # if toggler == False:
        #     player1 = 'o'
        #     player2 = 'x'
        # else:
        #     player1 = 'x'
        #     player2 = 'o'
        
        print(f"Episode [{episodes}] finished")
        if finish(board)[1] == 'x':
            print("playerX won")
            wins += 1
        elif finish(board)[1] == 'o':
            print("playerO won")
            loses += 1
        else:
            print("It's a draw")
            draws += 1   

        training_data1 = generate_training_data(history, weights1, player1)             # Generating target value for each board state
        training_data2 = generate_training_data(history, weights2, player2)             # Generating target value for each board state
        
        # history_data = history_data(history)
        updated_weights1 = weights_update(training_data1, history, weights1, learning_rate= 0.1)   # Updating the weights
        updated_weights2 = weights_update(training_data2, history, weights2, learning_rate= 0.1)   # Updating the weights
        
    print(f"X-Wins: {wins} | X-Loses: {loses} | Draws: {draws}")
    print("Weights1: ", updated_weights1)
    print("Weights2: ", updated_weights2)
    return weights1
    
def testNoTeacher():
    ## Read data file
    # with open("/Users/nitish/Documents/Aishwarya/Machine_Learning/ttt_data.txt") as file:
    #     for line in file:
    #         print(line.split(', '))
    #         break
    # exit()
    
    ### We will initialize variables to start playing the game
    player1 = 'x'
    player2 = 'o'   
    board = board_generator()   
    history = []
    wins = 0
    loses = 0
    draws = 0
    updated_weights1 = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]       # Intinially set the updated weights same as the initial weights
  
    toggler = True                                              # To toggle between players(so that one player does not get to play first always)


    ### Here the game starts 
    for episodes in range(20):
        board = board_reset()                       # Resetting the board at the start of the game
        history = [copy.deepcopy(board)]            # Copying the first board state to the history
        
        weights1 = updated_weights1
        
        play_inp = input("Do you want to play first? [y/n] : ")
        if play_inp in "yY":
            toggler = False     # Condition to toggle between the computer and the user 
            player1 = 'o'
            player2 = 'x'
        else:
            toggler = True
            player1 = 'x'
            player2 = 'o'
        
        while True:
            board = play(board, player = player1, smart = toggler, weights = weights1, user_mode=True)  # Computer is playing
            history.append(copy.deepcopy(board))
            
            print("Bot played")
            print_board(board)
            print()
            if finish(board)[0]:
                break
            
            board = play(board, player = player2, smart = not toggler, weights = weights1, user_mode=True)  # User is playing
            history.append(copy.deepcopy(board))
            print("User played")
            print_board(board)
            if finish(board)[0]:
                break
        
        
        print(f"Episode [{episodes}] finished")
        if finish(board)[1] == 'x':
            print("playerX won")
            wins += 1
        elif finish(board)[1] == 'o':
            print("playerO won")
            loses += 1
        else:
            print("It's a draw")
            draws += 1   

        training_data1 = generate_training_data(history, weights1, player1)             # Generating target value for each board state
        
        # history_data = history_data(history)
        updated_weights1 = weights_update(training_data1, history, weights1, learning_rate= 0.1)   # Updating the weights
        
    print(f"X-Wins: {wins} | X-Loses: {loses} | Draws: {draws}")
    print("Weights1: ", updated_weights1)
            
testNoTeacher()