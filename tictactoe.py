'''
TicTacToe game using Pygame
Computer plays using Minimax Alpha-Beta Pruning Algorithm

Andrei C. Radu
20/06/2020

'''

#Import libraries, start the pygame instance and initialize colors, font and the main windows

import pygame
import random
import math


pygame.init()

background_color = 123,188,182
blue = 87,95,138
green = 244, 232, 208
grey =128,128,128
dark_blue = 92,116,194


title_font = pygame.font.SysFont('comicsans', 80)
main_font = pygame.font.SysFont('arial', 70)
smaller_font = pygame.font.SysFont('arial', 50)
win = pygame.display.set_mode((729,729))
pygame.display.set_caption('tictactoe')


def add_symbol(window,symbol, x_coord, y_coord):

    if symbol == 'X': #draws 2 lines to form an X
        pygame.draw.line(window, (blue), [x_coord+20, y_coord+20], [x_coord+223,y_coord+223], 7)
        pygame.draw.line(window, (blue), [x_coord+223, y_coord+20], [x_coord+20,y_coord+223], 7)
    else:
        pygame.draw.arc(window, (green),[x_coord+10,y_coord+10, 223, 223], 0, 2*math.pi, 7) #draws an arc to form an O

def game_won(positions, window): #checks whether there's a win if yes, and draws a line
    if '' != positions[0] == positions[1] == positions[2]:
        pygame.draw.line(window, (grey), [729, 121], [0,121], 7)
    elif '' != positions[3] == positions[4] == positions[5]:
        pygame.draw.line(window, (grey), [729, 121+242], [0,121+242], 7)
    elif '' != positions[6] == positions[7] == positions[8]:
        pygame.draw.line(window, (grey), [729, 121+242*2], [0,121+242*2], 7)
    elif '' != positions[0] == positions[3] == positions[6]:
        pygame.draw.line(window, (grey), [121, 0], [121,729], 7)
    elif '' != positions[1] == positions[4] == positions[7]:
        pygame.draw.line(window, (grey), [121+242, 0], [121+242,729], 7)
    elif '' != positions[2] == positions[5] == positions[8]:
        pygame.draw.line(window, (grey), [121+242*2, 0], [121+242*2,729], 7)
    elif '' != positions[0] == positions[4] == positions[8]:
        pygame.draw.line(window, (grey), [0, 0], [729,729], 7)
    elif '' != positions[2] == positions[4] == positions[6]:
        pygame.draw.line(window, (grey), [0, 729], [729,0], 7)
    else:
        return False
    return True

#this will be used for the minmax function, the reason why we need a different function is so to avoid drawing the lines on the board
def solved(positions): 
    for i in range(0, 7, 3): #checks rows
        if ''!= positions[i] == positions[i+1] == positions[i+2]:
            return positions[i]
    for i in range(3): #checks columns
        if ''!= positions[i] == positions[i+3] == positions[i+6]:
            return positions[i]
    #checks diagonals:        
    if '' != positions[0] == positions[4] == positions[8]:
        return positions[0]
    elif '' != positions[2] == positions[4] == positions[6]:
        return positions[2]

    return False

def board_full(positions): #checks if the board is full
    if '' in positions: return False
    return True


def random_move(rectangles,computer_symbol, positions):# this makes the computer pick a random move
    branches = [i for i, sym in enumerate(positions) if sym == ''] #get all available locations
    i = random.choice(branches)
    add_symbol(win, computer_symbol, rectangles[i].x, rectangles[i].y)
    positions[i] = computer_symbol#update the positions list accordingly



def best_move(positions, rectangles, computer_symbol,difficulty):
    bestScore = float('-inf') #we are maximising(looking for highest score), so initialize the max score as -infinity
    positions_copy = positions.copy()
    bestMove = 1
    max_depth = 3 if difficulty == 'Normal' else 10 #if the difficulty selected is normal, only look 3 moves ahead

    for i,pos in enumerate(positions_copy): #check all positions
        if  pos =='': #if one is empty
            positions_copy[i] = computer_symbol #check what the board would be if we added a symbol here
            score = minimax(positions_copy, computer_symbol, False, 0, -10, 10, max_depth) #get a score using minimax
            positions_copy[i] = '' #revert the position to be empty again
            if (score > bestScore): # if we have a new score, update the score and best move
                bestScore = score
                bestMove = i
    add_symbol(win, computer_symbol, rectangles[bestMove].x, rectangles[bestMove].y)
    positions[bestMove] = computer_symbol#update the rectangles list accordingly


def minimax(positions, computer_symbol, is_computer_turn, depth, alpha, beta, max_depth):
    #base case
    state = solved(positions)
    if state and is_computer_turn: return -10 + depth #using depth to make sure the computer chooses the quickest path to victory
    elif state : return 10 - depth
    elif board_full(positions): return 0

    if depth >= max_depth: return 0 

    #recursive case
    if is_computer_turn: symbol = computer_symbol
    else: symbol = 'X' if computer_symbol =='O' else 'O' #if it's the player's turn, the mark is the opposite one
    best_score = float('-inf') if is_computer_turn else float('inf') #check whether we're maximising or minimising

    for i,pos in enumerate(positions):
        if pos =='':
            positions[i] = symbol
            score = minimax(positions, computer_symbol, not is_computer_turn, depth+1, alpha, beta, max_depth)
            positions[i] = ''
            best_score = max(best_score, score) if is_computer_turn else min(best_score, score) #minimise or maximise accordingly

            # Alpha Beta Pruning. Drastically reduces the amount of times minimax is called 
            if is_computer_turn: 
              alpha = max(alpha, best_score)  
            else:
              beta = min(beta, best_score)  
            if beta <= alpha:  
                break

    return best_score



def play_again(window): #draw the box that'll appear after the game is over
    ask = pygame.draw.rect(win, (0,0,0),pygame.Rect(60,150,580,400),3) 
    win.fill((dark_blue), ask)

    yes_btn = pygame.draw.rect(win, (255,255,255),pygame.Rect(90,420,220,110),3)
    yes_text = smaller_font.render('Yes', 1, (255,255,255))
    win.blit(yes_text, (100, 430))

    no_btn = pygame.draw.rect(win, (255,255,255),pygame.Rect(390,420,220,110),3)
    no_text = smaller_font.render('No', 1, (255,255,255))
    win.blit(no_text, (400, 430))
 
    return yes_btn, no_btn #return the buttons to check whether they are pressed


def pick_difficulty(window): #will be called in the main menu
    Easy = pygame.draw.rect(win, (255,255,255),pygame.Rect(50,320,180,90),3)
    Easy_text = smaller_font.render('Easy', 1, (255,255,255))
    win.blit(Easy_text, (80, 330))

    Normal = pygame.draw.rect(win, (255,255,255),pygame.Rect(265,320,180,90),3)
    Normal_text = smaller_font.render('Normal', 1, (255,255,255))
    win.blit(Normal_text, (275, 330))

    Hard = pygame.draw.rect(win, (255,255,255),pygame.Rect(480,320,180,90),3)
    Hard_text = smaller_font.render('Hard', 1, (255,255,255))
    win.blit(Hard_text, (510, 330))

    End = pygame.draw.rect(win, (255,255,255),pygame.Rect(190,510,320,110),3)
    End_text = main_font.render('Exit Game', 1, (255,255,255))
    win.blit(End_text, (210, 525))


 
    return Easy, Normal, Hard, End #return the buttons to check whether they are pressed


def main(difficulty):

    run = True
    symbol = random.choice(['X','O']) # assign the player a random symbol
    computer_symbol = 'X' if symbol =='O' else 'O'
    player_turn = random.choice([True,False]) # randomly decide who starts
    win.fill(background_color)

    #sets up the board as 9 squares; also to hold the symbol in each rectangle:
    rectangles = [pygame.draw.rect(win, (0,0,0),pygame.Rect(x,y,243,243),3) for y in [0, 243, 486] for x in [0, 243, 486]]
    positions =['' for _ in range(9)] #keeps track of the board
    

    while run:
        pygame.display.update()

        if not player_turn: #This sets up how the computer places the symbol
            if difficulty == 'Easy':
                random_move(rectangles,computer_symbol, positions)
            else: 
                best_move(positions, rectangles, computer_symbol, difficulty)

            player_turn = True #once the computer moved, it's the player's turn
            

        for event in pygame.event.get():
            if player_turn :
                if event.type == pygame.MOUSEBUTTONDOWN:

                    for i,rectangle in enumerate(rectangles):#check all rectangles until fond the one clicked
                        click = rectangle.collidepoint(pygame.mouse.get_pos())

                        if click and positions[i] =='': #if the corresponding position of the rectangle is empty
                            add_symbol(win, symbol, rectangle.x, rectangle.y)
                            positions[i] = symbol
                            player_turn = False


            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        #check whether someone has made a line
        a=game_won(positions, win)
        if a:
            symbol = computer_symbol if player_turn  else symbol
            game_over = main_font.render(f'Game Over! {symbol} wins',1,(255,255,255))
            run = False
            
        if board_full(positions) and not a: #if the board is full but no winners
            game_over = main_font.render(f'Game Over! Draw!',1,(255,255,255))
            run = False

        
    #the end of game display
    yes ,no  = play_again(win)
    ask_player = smaller_font.render('Would you like to play again ?', 1, (255,255,255))
    win.blit(game_over, (80, 220))
    win.blit(ask_player,(80, 340))
    pygame.display.update()

    while True:
        #ask the player if they'd like to play again
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes.collidepoint(pygame.mouse.get_pos()):
                    main(difficulty)
                elif no.collidepoint(pygame.mouse.get_pos()):
                    menu()

#main menu function
def menu():

    while True:
        # draw the main menu
        win.fill(background_color)

        title = title_font.render('TicTacToe', 1, (dark_blue))
        win.blit(title, (230, 50))

        difficulty_ask = title_font.render('Choose Difficulty: ', 1, (255,255,255))
        win.blit(difficulty_ask, (120, 180))
        easy, normal, hard, end = pick_difficulty(win)

        pygame.display.update() #update the display
        for event in pygame.event.get(): #get player input
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if end.collidepoint(pygame.mouse.get_pos()):
                    exit()
                elif easy.collidepoint(pygame.mouse.get_pos()):
                    main('Easy')
                elif normal.collidepoint(pygame.mouse.get_pos()):
                    main('Normal')
                elif hard.collidepoint(pygame.mouse.get_pos()):
                    main('Hard')


if __name__ == '__main__':
    menu()