# General pygame gui code
# Written by Lucas Yichen Jiao, although some parts were taken from CS50 AI's week zero project

# Module imports
import pygame, sys
import generator
from time import perf_counter
import recordscore

# Pygame window setup
pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
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

mistakes = 0
io = False
inited = False
fullscreen = False
update_mistake_c = False
ind_i, ind_j = 0, 0 # used for tracking which num_pos event.key needs to fill
TILE_SIZE = 60
TILE_ORIGIN = width/8 

# Functions
def generate_title(text, center):
    title = nums.render(text, True, white)
    titlehitbox = title.get_rect()
    titlehitbox.center = center
    screen.blit(title, titlehitbox)

def generate_heading(text, center):
    title = heading.render(text, True, white)
    titlehitbox = title.get_rect()
    titlehitbox.center = center
    screen.blit(title, titlehitbox)

def generate_button(text, rect):
    txt = subheading.render(text, True, black)
    hitbox = txt.get_rect()
    hitbox.center = rect.center
    pygame.draw.rect(screen, white, rect)
    screen.blit(txt, hitbox)

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
difficulty = 0

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
                    mistakes += 1
                    update_mistake_c = True
                
                numbox = num.get_rect()
                numbox.center = num_pos[9*ind_i + ind_j]
                screen.blit(num, numbox)

                if check_win():
                    gamestate = "VICTORY"
                    screen.fill(black)
                    io = False
                    inited = False
                
                elif mistakes == 5:
                    gamestate = "DEFEAT"
                    screen.fill((0,0,0))
                    io = False

    if gamestate == "TITLE_SCREEN":
        generate_heading("Welcome to pysudoku!", (width/2, height/10))
        playGame = pygame.Rect(width/2-140, height/3, 280, 75)
        gameQuit = pygame.Rect(width/2-140, height/2, 280, 75)
        generate_button("Play the game", playGame)
        generate_button("Quit", gameQuit)
        click, _0, _1 = pygame.mouse.get_pressed()
        if click:
            mpos = pygame.mouse.get_pos()
            if playGame.collidepoint(mpos):
                gamestate = "SELECT_DIFF"
                screen.fill(black)
            
            elif gameQuit.collidepoint(mpos):
                sys.exit() # exits directly out of code
    
    elif gamestate == "SELECT_DIFF":
        generate_heading("Select difficlty: ", (width/2, height/10))
        easy, hard = pygame.Rect(width/6, 360, 200, 75), pygame.Rect(2*width/3, 360, 200, 75)
        generate_button("Easy", easy)
        generate_button("Hard", hard)
        click, _0, _1 = pygame.mouse.get_pressed()
        if click:
            mpos = pygame.mouse.get_pos()
            if easy.collidepoint(mpos):
                gamestate = "GAMEPLAY"
                difficulty = 1
                screen.fill(black)
                inited = False
            
            elif hard.collidepoint(mpos):
                gamestate = "GAMEPLAY"
                difficulty = 2
                screen.fill(black)
                inited = False
        
    elif gamestate == "GAMEPLAY":
        if not inited:
            mistakes = 0
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
                cpy = [[num for num in row] for row in answer_board]
                player_board = generator.player_board(cpy, difficulty)
                if player_board != None:
                    break
            
            dynamic_board = [[num for num in row] for row in player_board]
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
            generate_title("Make your first move: ", (width/3, height/12))
            mist_text = generate_title(f"Mistakes: 0/5", (2*width/3+140, height/2))
            inited = True
        
        quit_b = pygame.Rect(2*width/3, 2*height/3, 280, 75)
        generate_button("Quit game", quit_b)

        if update_mistake_c:
            overriderect = pygame.Rect(2*width/3, height/2-75/2, 300, 80)
            pygame.draw.rect(screen, black, overriderect)
            mist_text = generate_title(f"Mistakes: {mistakes}/5", (2*width/3+140, height/2))
            update_mistake_c = False
        
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
            
            if quit_b.collidepoint(mouse):
                sys.exit()
    
    elif gamestate == "DEFEAT":
        generate_title("Game over!", (width/2, height/10))
        generate_title("You made too many mistakes!", (width/2, height/10+80))
        replay = pygame.Rect(width/2-100, height/2, 200, 75)
        generate_button("Play again!", replay)
        click, _0, _1 = pygame.mouse.get_pressed()
        if click:
            mpos = pygame.mouse.get_pos()
            if replay.collidepoint(mpos):
                gamestate = "SELECT_DIFF"
                screen.fill((0,0,0))
    else:  
        if not inited: 
            end_time = perf_counter()
            generate_heading("Congratulations!", (width/2, height/10))
            generate_title("You beat the game!", (width/2, height/10+40))
            highscore = recordscore.file_io(round(end_time-start_time, 2))
            generate_title(f"This round: {round(end_time-start_time, 2)} seconds", (width/2,height/4))
            generate_title(f"Your best: {highscore} seconds", (width/2,height/4+height/15))
            inited = True
        
        replay = pygame.Rect(width/2-100, 3*height/4, 200, 75)
        generate_button("Play again!", replay)
        click, _0, _1 = pygame.mouse.get_pressed()

        if click:
            mpos = pygame.mouse.get_pos()
            if replay.collidepoint(mpos):
                gamestate = "SELECT_DIFF"
                screen.fill((0,0,0))

    pygame.display.flip() 
    clock.tick(24)






