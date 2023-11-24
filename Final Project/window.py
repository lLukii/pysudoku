# General pygame gui code
# Written by Lucas Yichen Jiao, although some parts were taken from CS50 AI's week zero project

# Module imports
import pygame
import generator
from time import perf_counter
from pathlib import Path
import recordscore

# Pygame window setup
pygame.init()
screen = pygame.display.set_mode((720, 720))
pygame.display.set_caption("Pysudoku")
clock = pygame.time.Clock()

white = (255,255,255)
grey = (210,210,210)
black = (0,0,0)
red = (255,0,0)

heading = pygame.font.Font("OpenSans-Regular.ttf", 50)
subheading = pygame.font.Font("OpenSans-Regular.ttf", 40)
nums = pygame.font.Font("OpenSans-Regular.ttf", 28)

gamestate = "TITLE_SCREEN"

# Game variables/data structures
tiles = []
num_pos = []
answer_board = []
player_board = [] # initial layout board given to player
dynamic_board = []
errors = [[False for i in range(9)] for i in range(9)] # Checks if the current tile number is valid based on the situation of the board. 

io = False
inited = False
ind_i, ind_j = 0, 0 # used for tracking which num_pos event.key needs to fill
TILE_SIZE = 60
TILE_ORIGIN = 120 # 720/8

# Functions
def generate_title(text, center):
    title = nums.render(text, True, white)
    titlehitbox = title.get_rect()
    titlehitbox.center = center
    screen.blit(title, titlehitbox)

def check_win():
    nonzero = 0
    for row in dynamic_board:
        for num in row:
            if num != 0:
                nonzero += 1
    
    if nonzero == 81:
        trues = 0
        for row in errors:
            for err in row:
                if not err:
                    trues += 1
        
        if trues == nonzero:
            return True
    
    return False


# Pygame mainloop
gameOn = True
start_time, end_time = 0, 0

while gameOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOn = False
        
        if event.type == pygame.KEYDOWN and io:
            if event.key > pygame.K_0 and event.key <= pygame.K_9:
                overriderect = pygame.Rect(num_pos[9*ind_i + ind_j][0]-TILE_SIZE/3, num_pos[9*ind_i + ind_j][1]-TILE_SIZE/3, 2*TILE_SIZE/3, 2*TILE_SIZE/3)
                pygame.draw.rect(screen, black, overriderect)
                # update board position with the pressed number, and override the number on pygame window. 
                dynamic_board[ind_i][ind_j] = event.key-48
                # check if placed tile is valid
                num = 0
                overriderect = pygame.Rect(0, 0, 720, 100)
                pygame.draw.rect(screen, black, overriderect)
                if generator.check(ind_i, ind_j, dynamic_board):
                    num = nums.render(str(event.key-48), True, grey)
                    generate_title("Everything looks good!", (250, 50))
                    errors[ind_i][ind_j] = False
                
                else:
                    num = nums.render(str(event.key-48), True, red)
                    generate_title(f"Oops! You have a mistake at row {ind_i+1} column {ind_j+1}", (400, 50))   
                    errors[ind_i][ind_j] = True
                
                numbox = num.get_rect()
                numbox.center = num_pos[9*ind_i + ind_j]
                screen.blit(num, numbox)

                if check_win():
                    gamestate = "VICTORY"
                    screen.fill(black)
                    io = False
                    inited = False

    if gamestate == "TITLE_SCREEN":
        title = heading.render("Welcome to pysudoku!", True, white)
        titlehitbox = title.get_rect()
        titlehitbox.center = (360, 75)
        screen.blit(title, titlehitbox)

        playGame = pygame.Rect(220, 360, 280, 75)
        playText = subheading.render("Play the game", True, black)
        playhitbox = playText.get_rect()
        playhitbox.center = playGame.center
        pygame.draw.rect(screen, white, playGame)
        screen.blit(playText, playGame)

        click, _0, _1 = pygame.mouse.get_pressed()
        if click:
            mpos = pygame.mouse.get_pos()
            if playGame.collidepoint(mpos):
                gamestate = "GAMEPLAY"
                screen.fill(black)
        
    elif gamestate == "GAMEPLAY":
        
        if not inited:
            start_time = perf_counter()
            for i in range(9):
                row = []
                for j in range(9):
                    rect = pygame.Rect(TILE_ORIGIN + j*TILE_SIZE, TILE_ORIGIN + i*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, white, rect, 2)
                    row.append(rect)
                tiles.append(row)
            
            answer_board = generator.main()
            # creating initial player board
            while True:
                cpy = []
                for i in range(9):
                    cpy.append([num for num in answer_board[i]])
                player_board = generator.player_board(cpy, 1)
                if player_board != None:
                    break
            
            dynamic_board = [row for row in player_board]
            # display default board nums
            for i in range(9):
                for j in range(9):
                    x, y = TILE_ORIGIN + j*TILE_SIZE + TILE_SIZE/2, TILE_ORIGIN + i*TILE_SIZE + TILE_SIZE/2
                    if player_board[i][j] != 0:
                        num = nums.render(str(player_board[i][j]), True, white)
                        numbox = num.get_rect()
                        numbox.center = (x, y)
                        screen.blit(num, numbox)
                    num_pos.append([x,y])
            
            # displaying defualt text
            generate_title("Make your first move: ", (250, 50))
            print(answer_board)
            inited = True

        # set the position in which the number is placed
        click, _0, _1 = pygame.mouse.get_pressed()
        if click:
            mouse = pygame.mouse.get_pos()
            for i in range(9):
                for j in range(9):
                    if tiles[i][j].collidepoint(mouse) and player_board[i][j] == 0:
                        io = True
                        ind_i = i
                        ind_j = j
        
    elif gamestate == "VICTORY":  
        if not inited: 
            end_time = perf_counter()
            title = heading.render("Congratulations!\n You completed the puzzle!", True, white)
            titlehitbox = title.get_rect()
            titlehitbox.center = (360, 75)
            screen.blit(title, titlehitbox)
            highscore = recordscore.file_io(end_time-start_time)
            generate_title(f"This round: {end_time-start_time} seconds", (300,300))
            generate_title(f"Your best: {highscore} seconds", (200,200))
            inited = True

    pygame.display.update() 
    clock.tick(24)

        





