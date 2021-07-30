import random

def sliding_puzzle_ini(dim):
    '''
    Initializing the sliding puzzle game.

    dim: the dimension of puzzle game, in range of 3 to 10

    the return value is the list of dim lists which as a whole includes numbers from 0 to dim**2 - 1, 
same as the order when the user is successfully pass the puzzle
    '''
    puzzle_boarding=[]
    counter = 0
    numbers = range(1, dim ** 2)
    
    for column_num in range(dim):
        row=[]
        for row_num in range(dim):
            if (column_num != dim - 1 or row_num != dim -1 ):
                row.append(numbers[counter])
            else:
                row.append(0)
            counter += 1
        puzzle_boarding.append(row)
    return puzzle_boarding    
    
def puzzle_print(dim, puzzle_boarding):
    '''
    Print the puzzle_boarding
    
    Modify the printed version of puzzle boarding with \t and replace 0 with space
    '''
    for column_num in range(dim):
        row = ''
        for row_num in range(dim):
            if (puzzle_boarding[column_num][row_num] != 0):
                row += str(puzzle_boarding[column_num][row_num]) + '\t'
            else:
                row += '' + '\t'
        print(row)
    
def get_blank_place(dim, puzzle_boarding):
    '''
    To get the blank place in the puzzle board

    simplify the process by finding the place of 0

    return the column and row number of the position of 0
    '''
    for column_num in range(dim):
        for row_num in range(dim):
            if puzzle_boarding[column_num][row_num] == 0:
                return (column_num , row_num)

def move(direction, puzzle_boarding, move_blank):
    '''
    move_blank is the parameter

    to exchange the blank position with its neighboring numbers

    return the puzzle_boarding after replacement
    '''
    zero_column , zero_row=get_blank_place(g_dim , puzzle_boarding)
    if (direction in move_blank):
        if zero_column != g_dim - 1:
            if (direction == up):
                puzzle_boarding[zero_column][zero_row] = puzzle_boarding[zero_column + 1][zero_row]
                puzzle_boarding[zero_column + 1][zero_row] = 0
                zero_column += 1
        if zero_column != 0:
            if (direction == down):
                puzzle_boarding[zero_column][zero_row]=puzzle_boarding[zero_column - 1][zero_row]
                puzzle_boarding[zero_column - 1][zero_row] = 0
                zero_column -= 1
        if zero_row != g_dim - 1:
            if (direction == left):
                puzzle_boarding[zero_column][zero_row] = puzzle_boarding[zero_column][zero_row + 1]
                puzzle_boarding[zero_column][zero_row + 1] = 0
                zero_row += 1
        if zero_row != 0:
            if (direction == right):
                puzzle_boarding[zero_column][zero_row] = puzzle_boarding[zero_column][zero_row-1]
                puzzle_boarding[zero_column][zero_row - 1]= 0
                zero_row -= 1
    return puzzle_boarding

def available_movement(puzzle_boarding):
    '''
    to get the available movement of the blank 

    return a list to show the available move direction
    '''
    available_move = []
    zero_column , zero_row = get_blank_place(g_dim , puzzle_boarding)
    if (zero_column == 0):
        available_move.append(up)
        available_move.append('-up  ')
        if (zero_row == 0):
            available_move.append(left)
            available_move.append('-left  ')
        elif (zero_row == g_dim - 1):
            available_move.append(right)
            available_move.append('-right  ')
        else:
            available_move.append(left)
            available_move.append('-left  ')
            available_move.append(right)
            available_move.append('-right  ')
    elif (zero_column == g_dim - 1):
        available_move.append(down)
        available_move.append('-down  ')
        if (zero_row == 0):
            available_move.append(left)
            available_move.append('-left  ')
        elif (zero_row == g_dim - 1):
            available_move.append(right)
            available_move.append('-right  ')
        else:
            available_move.append(left)
            available_move.append('-left  ')
            available_move.append(right)
            available_move.append('-right  ')
    else:
        available_move.append(up)
        available_move.append('-up  ')
        available_move.append(down)
        available_move.append('-down  ')
        if (zero_row == 0):
            available_move.append(left)
            available_move.append('-left  ')
        elif (zero_row == g_dim - 1):
            available_move.append(right)
            available_move.append('-right  ')
        else:
            available_move.append(left)
            available_move.append('-left  ')
            available_move.append(right)
            available_move.append('-right  ')

    return available_move


def check_success(puzzle_boarding):
    '''
    check wether the user pass the puzzle game

    True to indicates pass, False to indicates not pass
    '''
    counter = 0
    if (puzzle_boarding[g_dim - 1][g_dim - 1] != 0):
        return False
    for column_num in range(g_dim):
        for row_num in range(g_dim):
            counter += 1
            while (counter % g_dim != 0 ): 
            #when the counter will not change the column to get its successor
                if (puzzle_boarding[column_num][row_num] + 1 != puzzle_boarding[column_num][row_num + 1] 
                and counter != g_dim**2 - 1):
                    return False
                else:
                    break
            while (counter % g_dim == 0 and counter != g_dim ** 2):
                if (puzzle_boarding[column_num][row_num] + 1 != puzzle_boarding[column_num + 1][0]):
                # to goes to the successor it needs to change the column 
                    return False
                else:
                    break
            if (counter == g_dim**2):
            # counter goes to the end of the game
                return True
                

def key_press(keyword_press):
    '''
    to examine wether the user input the correct form of keyword

    return the list of keyword characters
    '''
    keywords=[]
    count = 0
    for char_selected in keyword_press:
        if ((ord(char_selected)>= 65 and ord(char_selected) <= 90) 
        or (ord(char_selected)>= 97 and ord(char_selected) <= 122)
        and count <= 3):
            keywords.append(char_selected)
            count += 1
    return keywords


# main program 
while True:
    while True:
        try:
            g_dim = int(input('Enter the desired dimension of the puzzle >'))
            if g_dim >= 3 and g_dim <= 10:
                g_puzzle_boarding = sliding_puzzle_ini(g_dim)
                break 
            else:
                print ('dimension have to be at this range:[3,10]')
        except:
            print('dimension should be integer')
    g_keyword_press = input('Enter the four letters used for left, right, up and down directions >' )
    g_keyword_list = key_press(g_keyword_press)
    # for directions initialized
    left = g_keyword_list[0]
    right = g_keyword_list[1]
    up = g_keyword_list[2]    
    down = g_keyword_list[3]
    #randomly move the blank to make it puzzle for 12 times
    g_direction_list = [left, right, up, down, left, right, up, down, left, right, up, down]
    random.shuffle(g_direction_list)
    for number_of_move in range(len(g_direction_list)):
        move(g_direction_list[number_of_move], g_puzzle_boarding, g_direction_list)
    

    puzzle_print(g_dim, g_puzzle_boarding)
    # print the randomized puzzle
    g_count = 0 
    # count is used to count how many round are expirenced to pass the game
    while(check_success(g_puzzle_boarding) == False):
        g_count += 1
        g_available_move = available_movement(g_puzzle_boarding)
        for position in range(len(g_available_move)):
            print(g_available_move[position] ,end='',)
        print()
        g_direction = input('enter your move >')
        g_puzzle_boarding = move(g_direction , g_puzzle_boarding, g_available_move)
        puzzle_print(g_dim , g_puzzle_boarding)

    print('congratulation! You solved puzzle in', g_count, 'step')
    print()
    print()
    print()
    
    final_press = input('Enter n to start a new game or enter q to end the game >')
    if (final_press == 'q'):
        print('this is the end of the game')
        break
    elif (final_press == 'n'):
        continue





    