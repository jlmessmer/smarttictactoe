#Tic Tac Toe program using basic machine learning.
#It works by saving each board state throughout every game played on it
#and recording the responding move made every time. Once the computer gets enough
#data, then ideally wisdom of the masses will kick in and the bot will
#be virtually unbeatable.

#(C) 2015 Jimmy Messmer

import os
import collections
import random

#These will represent the tic tac toe board
row1 = ['#', '#', '#']
row2 = ['#', '#', '#']
row3 = ['#', '#', '#']

#This array will store all the moves that have been made in the game
moves = []

#These are all the possible moves to make in the game
possible_moves = ["11", "12", "13", "21", "22", "23", "31", "32", "33"]

#Keeps track of who's turn it is.
human_turn = True

#Keeps track of the last human move
last_human_move = ''

def cls():
    os.system(['clear','cls'][os.name == 'nt'])

#This updates the board arrays and saves each human move for the computer to learn from.
def update(x, y, val):
    
    #If it's a human turn, then we should save the move that they just made.
    if(human_turn == True):
        last_human_move = str(x) + str(y)
        line_num = None
        data = None
        #Figure out which piece the human is playing as.
        if(player_piece == 'X'):
            with open("x.txt") as myFile:
                data = myFile.readlines()
            try:
                #Find if this exact board layout has been saved before
                #If it has, then save this new move as a possible choice for the computer
                line_num = data.index(str(moves) + "\n")
                data_to_write = str(data[line_num+1])[:-2] + "," + last_human_move + ",\n"
                data[line_num+1] = data_to_write
                with open('x.txt', 'w') as memFile:
                    memFile.writelines(data)
            except:
                #If this board layout hasn't been saved before
                #Then save it and keep track of what move was made
                data.append(str(moves) + "\n")
                data.append(last_human_move + ",\n")
                with open('x.txt', 'w') as memFile:
                    memFile.writelines(data)
        #Same process, just with the other piece
        else:
            with open("o.txt") as myFile:
                data = myFile.readlines()
            try:
                line_num = data.index(str(moves) + "\n")
                data_to_write = str(data[line_num+1])[:-2] + "," + last_human_move + ",\n"
                data[line_num+1] = data_to_write
                with open('o.txt', 'w') as memFile:
                    memFile.writelines(data)
            except:
                data.append(str(moves) + "\n")
                data.append(last_human_move + ",\n")
                with open('o.txt', 'w') as memFile:
                    memFile.writelines(data)
    #Save the move
    moves.append(str(x)+str(y))
    
    #Update the Board
    if(int(y) == 1):
        row1[int(x)-1] = val
    elif(int(y) == 2):
        row2[int(x)-1] = val
    else:
        row3[int(x)-1] = val
    #display()
    #print "Row 1: " + str(row1)

def isGameOver():
    #Get an array for each column
    col1 = [row1[0], row2[0], row3[0]]
    col2 = [row1[1], row2[1], row3[1]]
    col3 = [row1[2], row2[2], row3[2]]
    
    #Get an array for each diagonal
    diag1 = [row1[0], row2[1], row3[2]]
    diag2 = [row1[2], row2[1], row3[0]]
    
    #A bunch of if statements to check each possible case for the game being over
    if(row1[0] == row1[1] and row1[0] == row1[2] and row1[0] != '#'):
        return True
    elif(row2[0] == row1[1] and row2[0] == row2[2] and row2[0] != '#'):
        return True
    elif(row3[0] == row2[1] and row3[0] == row3[2] and row3[0] != '#'):
        return True
    elif(col1[0] == col1[1] and col1[0] == col1[2] and col1[0] != '#'):
        return True
    elif(col2[0] == col2[1] and col2[0] == col2[2] and col2[0] != '#'):
        return True
    elif(col3[0] == col3[1] and col3[0] == col3[2] and col3[0] != '#'):
        return True
    elif(diag1[0] == diag1[1] and diag1[0] == diag1[2] and diag1[0] != '#'):
        return True
    elif(diag2[0] == diag2[1] and diag2[0] == diag2[2] and diag2[0] != '#'):
        return True
    elif('#' not in row1 and '#' not in row2 and '#' not in row3):
        return True
    else:
        return False

def think(state):
    if(player_piece == 'O'):
        with open("x.txt") as myFile:
            data = myFile.readlines()
        try:
            line_num = data.index(state + "\n")
            #Find if the computer remembers this from before
            previous_knowledge = str(data[line_num + 1])[:-2]
            knowledge_arr = previous_knowledge.split(",")
            move = collections.Counter(knowledge_arr).most_common(1)
            #If he does then find what is the most common move in this situation
            move = str(move[0])[2:4]
            return move
        except:
            #If not, then we'll choose a random move
            return "No Memory"
    else:
        #Same thing, but for the other piece (again)
        with open("o.txt") as myFile:
            data = myFile.readlines()
        try:
            line_num = data.index(state + "\n")
            previous_knowledge = str(data[line_num + 1])[:-2]
            knowledge_arr = previous_knowledge.split(",")
            move = collections.Counter(knowledge_arr).most_common(1)
            move = str(move[0])[2:4]
            return move
        except:
            return "No Memory"
def make_move(board):
    #Get the move
    move = think(str(board))
    if(str(move) == "No Memory"):
        #If we don't remember the move, then choose a random space to put a piece in
        move = random.choice(possible_moves)
        while(move in board):
            move = random.choice(possible_moves)
    #Update the board
    update(move[0], move[1], cpu_piece)

def main():
    #Define the player piece and cpu piece
    
    #***There were some problems with these pieces not being defined when I defined them up with the***
    #***rest of the variables. I need to figure out why that was.***
    global player_piece
    global cpu_piece
    
    #Ask if the human wants to go first
    resp = raw_input("Would you like to go first? [y/n]")
    if(resp == 'y'):        
        #If yes, then define the pieces and get the human move and update the board.
        human_turn = True
        cpu_piece = 'O'
        player_piece = 'X'
        move = str(raw_input("Alright, please make your move"))
        update(move[0], move[1], 'X')
        human_turn = False
    else:
        #If not then still define the pieces and also set it to the computer's turn
        human_turn = False
        cpu_piece = 'X'
        player_piece = 'O'
        print "Good luck, then"
        
    #Main game loop 
    while(isGameOver() == False):
        #If it's the computer's turn, then it makes it's move
        if(human_turn == False):
            make_move(moves);
            human_turn = True
        #Otherwise the human plays
        else:
            move = str(raw_input("Make a move: "))
            while(move in moves):
                move = str(raw_input("You can't go there. Choose somewhere else."))
            update(move[0], move[1], player_piece)
            human_turn = False
            
        #Display the board again and clear the screen.
        
        #***This also wasn't working as it's own method. I need to figure that out as well.***
        
        cls()
        print row1[0] + "|" + row1[1] + "|" + row1[2]
        print "------"
        print row2[0] + "|" + row2[1] + "|" + row2[2]
        print "------"
        print row3[0] + "|" + row3[1] + "|" + row3[2]
    #Once the game is over, then print this:
    print "The game is over"
    
if __name__ == "__main__":
    main()
