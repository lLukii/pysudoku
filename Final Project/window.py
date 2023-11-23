# General pygame gui code
# Written by Lucas Yichen Jiao, although some parts were taken from CS50 AI's week zero project

# Module imports
import pygame
import generator

# Pygame window setup
pygame.init()
screen = pygame.display.set_mode((720, 720))
pygame.display.set_caption("Pysudoku")
clock = pygame.time.Clock()

white = (255,255,255)
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
dynamic_board = [] # dynamic board that keeps track of current player progress
io = False
inited = False
mistakes = False
ind_i, ind_j = 0, 0 # used for tracking which num_pos event.key needs to fill
TILE_SIZE = 60
TILE_ORIGIN = 120 # 720/8

# Functions
def generate_title(text, center):
    title = nums.render(text, True, white)
    titlehitbox = title.get_rect()
    titlehitbox.center = center
    screen.blit(title, titlehitbox)

# Pygame mainloop
gameOn = True
tck = 0
time = 0
while gameOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOn = False
        
        if event.type == pygame.KEYDOWN and io:
            if event.key > pygame.K_0 and event.key <= pygame.K_9:
                overriderect = pygame.Rect(num_pos[9*ind_i + ind_j][0]-TILE_SIZE/3, num_pos[9*ind_i + ind_j][1]-TILE_SIZE/3, 2*TILE_SIZE/3, 2*TILE_SIZE/3)
                pygame.draw.rect(screen, black, overriderect)
                dynamic_board[ind_i][ind_j] = event.key-48
                # check if placed tile is valid
                num = 0
                overriderect = pygame.Rect(0, 0, 720, 100)
                pygame.draw.rect(screen, black, overriderect)
                if generator.check(ind_i, ind_j, dynamic_board):
                    num = nums.render(str(event.key-48), True, white)
                    generate_title("Everything looks good!", (250, 50))
                
                else:
                    num = nums.render(str(event.key-48), True, red)
                    generate_title(f"Oops! You have a mistake at row {ind_i+1} column {ind_j+1}", (400, 50))
                    mistakes = True
                
                numbox = num.get_rect()
                numbox.center = num_pos[9*ind_i + ind_j]
                screen.blit(num, numbox)

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
                screen.fill((0,0,0))
        
    elif gamestate == "GAMEPLAY":
        tck += 1
        if tck == 24:
            tck = 0
            time += 1
        
        if not inited:
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


    pygame.display.update() 
    clock.tick(24)

outtime = ""
if time//60 < 10:
    outtime += "0" + str(time//60)

else:
    outtime += str(time//60)

outtime += ":"
if time%60 < 10:
    outtime += "0" + str(time%60)

else:
    outtime += str(time%60)

print(outtime)


        





