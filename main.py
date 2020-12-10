# Boulder Shower
# Game by Sulian Thual
# January 2020
# runs with pygame 1.9.4

##########################################################
##########################################################
# Import libraries

# install pygame (anaconda?): pip install pygame
import random
import pygame
from pygame import mixer#sound
# import math# not needed

##########################################################
##########################################################
# Initialize game and load data

pygame.mixer.pre_init(50000, -16, 2, 2048) # setup mixer, speed is approx
mixer.init()# initialize music
pygame.init()# Intialize the pygame
screen = pygame.display.set_mode((800, 600))# Define screen

font = pygame.font.Font('freesansbold.ttf', 15)# text fonts
fontbig = pygame.font.Font('freesansbold.ttf', 30)

imgstart = pygame.image.load('bouldershower_imgstart.png')# Load start image
imgbackground = pygame.image.load('bouldershower_imgbackground.png')# background image
imgmanual = pygame.image.load('bouldershower_imgmanual.png')# instructions image
imgdiedoverlay = pygame.image.load('bouldershower_imgdiedoverlay.png')# died overlay 

imgplayer_l= pygame.image.load('bouldershower_imgplayerleft.png')# player image(s)
imgplayer_r= pygame.image.load('bouldershower_imgplayerright.png')
imgplayer_u= pygame.image.load('bouldershower_imgplayerup.png')
imgplayer_d= pygame.image.load('bouldershower_imgplayerdown.png')
imgplayerhit = pygame.image.load('bouldershower_imgplayerhit.png')
imgplayerdead = pygame.image.load('bouldershower_imgplayerdead.png')
imgplayerarrow_l= pygame.image.load('bouldershower_imgplayerarrow_left.png')
imgplayerarrow_r= pygame.image.load('bouldershower_imgplayerarrow_right.png')
imgplayerarrow_u= pygame.image.load('bouldershower_imgplayerarrow_up.png')
imgplayerarrow_d= pygame.image.load('bouldershower_imgplayerarrow_down.png')
imgplayerarrow_gl= pygame.image.load('bouldershower_imgplayerarrow_grayleft.png')
imgplayerarrow_gr= pygame.image.load('bouldershower_imgplayerarrow_grayright.png')
imgplayerarrow_gu= pygame.image.load('bouldershower_imgplayerarrow_grayup.png')
imgplayerarrow_gd= pygame.image.load('bouldershower_imgplayerarrow_graydown.png')

imgboulder = pygame.image.load('bouldershower_imgboulder.png')# enemy image(s)
imgboulderwarning = pygame.image.load('bouldershower_imgboulderwarning.png')
imgbouldersmoke = pygame.image.load('bouldershower_imgbouldersmoke.png')
imgbouldercrack = pygame.image.load('bouldershower_imgbouldercrack.png')
imgboulderdestroy = pygame.image.load('bouldershower_imgboulderdestroy.png')

mixer.music.load("bouldershower_soundbackgroundmusic.mp3")# music and sounds
playersounddash = mixer.Sound("bouldershower_sounddash.wav")# when moving
playersoundbreak = mixer.Sound("bouldershower_soundbreak.wav")# when breaking
playersounddeath = mixer.Sound("bouldershower_sounddeath.wav")# when hit
playersounddeathfinal = mixer.Sound("bouldershower_sounddeathfinal.wav")# when dead

mixer.music.set_volume(0.6)# set volume (default=1?)
playersounddash.set_volume(1)
playersoundbreak.set_volume(0.4)   
playersounddeath.set_volume(0.6)               
##########################################################
##########################################################
# Game Functions

# Select Sound On/Off on start screen
def display_soundstate(state): 
    xdrawl=200
    ydrawl=250
    xdrawr=500
    ydrawr=250
    if state == 0:# sound on left 
        screen.blit(imgplayerarrow_l, (xdrawl,ydrawl))# blue left
        screen.blit(imgplayerarrow_gr, (xdrawr,ydrawr))# gray right
    if state == 1:# sound off right
        screen.blit(imgplayerarrow_r, (xdrawr,ydrawr))# blue right
        screen.blit(imgplayerarrow_gl, (xdrawl,ydrawl))# gray left

# Select difficulty on start screen
def display_difficulty(state): 
    xdrawu=350
    ydrawu=100
    xdrawd=350
    ydrawd=400
    if state == 0:# easy 
        screen.blit(imgplayerarrow_u, (xdrawu,ydrawu))# blue top
        screen.blit(imgplayerarrow_gd, (xdrawd,ydrawd))# gray bottom
    if state == 1:# hard
        screen.blit(imgplayerarrow_gu, (xdrawu,ydrawu))# gray top   
        screen.blit(imgplayerarrow_d, (xdrawd,ydrawd))# blue bottom
        
#display score and informations
def display_score(wave,beat,money,life, difficulty):
    screen.blit(font.render("Wave: " + str(wave), True, (255, 255, 255)), (715,50))
    beatinbpm=round(60/beat*1000)# convert beat in ms to beat per minutes
    screen.blit(font.render("Bpm: " + str(beatinbpm), True, (255, 255, 255)), (715,90))    
    if difficulty == 0:
            screen.blit(font.render("Easy", True, (255, 255, 255)), (715,130))
    if difficulty == 1:
        screen.blit(font.render("Hard", True, (255, 255, 255)), (715,130))
            
    screen.blit(fontbig.render("Life", True, (200, 0, 0)), (17,20))
    screen.blit(fontbig.render(str(life), True, (255, 255, 255)), (35,60))
    screen.blit(fontbig.render("Score", True, (0, 0, 255)), (2,100))
    screen.blit(fontbig.render(str(money), True, (255, 255, 255)), (35,140))
    
    if playing:        
        screen.blit(font.render("Menu: ", True, (255, 255, 255)), (725,450))
        screen.blit(font.render("Press", True, (255, 255, 255)), (725,490))
        screen.blit(font.render("Space ", True, (255, 255, 255)), (725,530)) 

# Display banners while playing: alternating red bands on left and right
def display_banner(state):   
    timebanner=pygame.time.get_ticks()# read time again
    yh=600*(timebanner-timeold)/beat
    if state == 1:
        xdraw1=90
        xdraw2=700
        ydraw1=600-yh
        ydraw2=0
    if state == -1:
        xdraw1=700
        xdraw2=90
        ydraw2=0
        ydraw1=600-yh
    screen.fill((200, 0, 0), rect=(xdraw1,ydraw1,10,yh))
    screen.fill((200, 0, 0), rect=(xdraw2,ydraw2,10,yh))
        
# Display player (x=1,2,3 left to right, y=1,2,3 bottom to top)
def display_player(x,y,state,hit):
    xdraw=x*200-100
    ydraw=600-y*200
    if state == 1:# left pressed
        screen.blit(imgplayer_l, (xdraw,ydraw))
    if state == 2:# right pressed
        screen.blit(imgplayer_r, (xdraw,ydraw))
    if state == 3:# up (default state)
        screen.blit(imgplayer_u, (xdraw,ydraw))
    if state == 4:# down
        screen.blit(imgplayer_d, (xdraw,ydraw))        
    if state == 5:# dead state
        screen.blit(imgplayerdead, (xdraw,ydraw))
    # if player was hit and is not dead add hit image overlay 
    if hit == 1:
        if state != 5:
            screen.blit(imgplayerhit, (xdraw,ydraw)) 
        
# Display player arrows (direction=0,1,2,3,4 for nothing left right up down)
def display_playerarrow(x,y,direction):
    xdraw=x*200-100
    ydraw=600-y*200
    # Display nothing if direction=0
    if direction == 1:    # Left
        xdraw=xdraw-50
        ydraw=ydraw+50
        screen.blit(imgplayerarrow_l, (xdraw,ydraw))
    if direction == 2:    # Right
        xdraw=xdraw+150
        ydraw=ydraw+50
        screen.blit(imgplayerarrow_r, (xdraw,ydraw))        
    if direction == 3:    # Up
        xdraw=xdraw+50
        ydraw=ydraw-50
        screen.blit(imgplayerarrow_u, (xdraw,ydraw))   
    if direction == 4:    # Down
        xdraw=xdraw+50
        ydraw=ydraw+150
        screen.blit(imgplayerarrow_d, (xdraw,ydraw)) 

# Display boulder changes (warning X, or decaying boulder XO)
def display_boulderchanges(grid,bgrid):
    for i in range(9):          
        if grid[i]==1:# warning X here
            if bgrid[i]==1:# boulder O here. 
                screen.blit(imgboulderdestroy, (draw_coordx(i),draw_coordy(i)))# XO
            else:# X: add new boulder
                screen.blit(imgboulderwarning, (draw_coordx(i),draw_coordy(i)))# X                  
        
# Display boulder (O)
def display_boulder(grid):
    for i in range(9):
        if grid[i]==1: screen.blit(imgboulder, (draw_coordx(i),draw_coordy(i)))  

# Display boulder smoke (X->smoke when boulder just falled)
def display_bouldersmoke(grid):
    for i in range(9):
        if grid[i]==1: screen.blit(imgbouldersmoke, (draw_coordx(i),draw_coordy(i))) 

# Display cracked boulder  (when boulder just destroyed by player)
def display_bouldercrack(grid):
    for i in range(9):
        if grid[i]==1: screen.blit(imgbouldercrack, (draw_coordx(i),draw_coordy(i))) 
        
# Return drawing coordinates for enemies from index
# Grid:
# 0 1 2
# 3 4 5
# 6 7 8
def draw_coordx(index):
    return([100,300,500,100,300,500,100,300,500][index])
def draw_coordy(index):
    return([0,0,0,200,200,200,400,400,400][index])

# return grid index i=0-8 from position x=1,2,3 and y=1,2,3
def get_indexfromcoords(x,y):
    return(x-1)+(3-y)*3                

# Get index list of neighbors for one spot
def get_neighbors(index):    
    if index == 0: return([1,3])# top left
    if index == 1: return([0,2,4])# top                     
    if index == 2: return([1,5])# top right                
    if index == 3: return([0,4,6])# middle left
    if index == 4: return([1,3,5,7])# middle                    
    if index == 5: return([2,4,8])# middle right                  
    if index == 6: return([3,7])# bottom left
    if index == 7: return([4,6,8]) # bottom                   
    if index == 8: return([5,7])# bottom right
                
              
##########################################################
##########################################################
##########################################################
##########################################################
# HYPER GAME LOOP
# cycle trough start page, instruction page, playing, dead page
    
# Hyper game loop initial conditions
ingame= True # in the game 
starting= True# start menu            
playing = False # playing the game
died = False# has died now
manual = False# reading the manual

# Initial settings (can be changed during hyper game loop)
playermute= 1 # muted sound on-off (default on)
playerdifficulty= 0 # difficulty level (default easy)


while ingame: # start Hyper Game Loop
            
    ##########################################################
    ##########################################################
    # (Re)Set Game Initial Conditions
    
    #Informations
    playerlife=7# starting life (how many hits before dying)
    playermoney=0# number of broken boulders
    playerscore=0# number of waves survived
    
    # Timer
    bpmstart=40# Initial bpm
    bpmmax=60# Max bpm
    bpminc=0.5# bpm increment
    beat=60000/bpmstart# starting beat value in milliseconds
    beatmax=60000/bpmmax# max beat value in milliseconds
    timeold=pygame.time.get_ticks()# read current game time in milliseconds
    newbeat= False # new beat or not
    
    # Player
    playerstate=3# player stance=1,2,3,4,5 for left,right,up,down,dead
    playerhit=0# if player was hit this beat
    playerkey=0# pressed key=0,1,2,3,4 for none, left,right,up,down
    playerx=2# initial x position (center)
    playery=2# initial y position (center)
    playerdx=0# initial position increment
    playerdy=0# initial position increment
     
    # Player arrows
    playerarrowdirection=0# arrow direction=0,1,2,3,4 for none, left,right,up,down
    playerax=playerx# initial arrow position (same as player)
    playeray=playery# initial arrow position (same as player)

    # Enemies
    bouldermin = 1 # min boulder that can fall each wave
    bouldermax = 4 # max boulder that can fall each wave
    boulderwarninggrid = [0,0,0,0,0,0,0,0,0]# =1 if a boulder warning
    bouldertheregrid   = [0,0,0,0,0,0,0,0,0]# =1 if a boulder is there
    bouldersmokegrid   = [0,0,0,0,0,0,0,0,0]# =1 if a boulder was destroyed by other boulder
    bouldercrackgrid   = [0,0,0,0,0,0,0,0,0]# =if a boulder was destroyed by player
    boulderdestroygrid   = [0,0,0,0,0,0,0,0,0]# =1 if a boulder will fall on other one
    
    # Banner state (for red color bands that show beat)
    bannerstate=1# starts at 1, alternates between 1 and -1 each beat
    
    #Music
    if playermute == 0: mixer.music.play(-1)# (Re)Start Background Music    

        
    ##########################################################
    ##########################################################
    ##########################################################
    ##########################################################
    # GAME START PAGE
    
    
    while starting:
          
        ############################
        #Check for button/key press
        
        for event in pygame.event.get():
            
            # Close the window (quit game)
            if event.type == pygame.QUIT:
                ingame = False
                starting = False
                
            # if keystroke is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    manual = True# go to instructions
                    starting = False# exit start page
                if event.key == pygame.K_LEFT:
                    mixer.music.play(-1)# restart music
                    playermute=0
                if event.key == pygame.K_RIGHT:# mute sound
                    playermute=1
                    pygame.mixer.music.stop()                      
                if event.key == pygame.K_UP:# easy
                    playerdifficulty=0
                if event.key == pygame.K_DOWN:# hard
                    playerdifficulty=1
        
        ############################
        # Change Difficulty
                    
        if playerdifficulty == 0: # easy
            playerlife=5# 10 lifes
            bouldermax=3# max boulders
            bpmstart=50# slow beat
            beat=60000/bpmstart
            bpmmax=75
            beatmax=60000/bpmmax
            bpminc=0.5
        if playerdifficulty == 1: # hard
            playerlife=3# 5 lifes
            bouldermax=5# max boulders
            bpmstart=75# fast beat
            beat=60000/bpmstart
            bpmmax=100
            beatmax=60000/bpmmax
            bpminc=0.5  
                
        ############################
        # Display 
            
        screen.fill((255, 255, 255))# fill screen with RGB (range 0-255)
        screen.blit(imgstart, (0, 0))# Display start image     
        display_player(playerx,playery,playerstate,playerhit) # display player 
        display_soundstate(playermute)# display sound selection
        display_difficulty(playerdifficulty)# display difficulty selection
        display_score(playerscore,beat,playermoney,playerlife,playerdifficulty)# display infos
        pygame.display.update()# Update Screen during Game Loop


    ##########################################################
    ##########################################################
    ##########################################################
    ##########################################################
    # INSTRUCTIONS PAGE

    
    while manual:    

        ############################
        #Check for button/key press
        
        for event in pygame.event.get():
            
            # Close the window (quit game)
            if event.type == pygame.QUIT:
                ingame = False# exit hyperloop
                manual = False# exit instructions

            # if keystroke is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = True
                    manual = False  
        
        ############################
        # Display 
                    
        screen.fill((255, 255, 255))# fill screen with RGB (range 0-255)
        screen.blit(imgmanual, (0, 0))# display instructions image      
        display_score(playerscore,beat,playermoney,playerlife,playerdifficulty)# display infos        
        pygame.display.update() # Update Screen during Game Loop  
 
       
    ##########################################################
    ##########################################################
    ##########################################################
    ##########################################################        
    # PLAYING PAGE


    while playing:
                                
        ############################
        #Check for button/key press
                
        for event in pygame.event.get():
            
            # Close the window (quit game)
            if event.type == pygame.QUIT:
                ingame = False# exit hyperloop
                playing = False# exit playing
            
            # if keystroke is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    starting = True# go to start page
                    playing = False# exit playing                  
                if event.key == pygame.K_LEFT:
                    playerkey=1
                if event.key == pygame.K_RIGHT:
                    playerkey=2
                if event.key == pygame.K_UP:
                    playerkey=3
                if event.key == pygame.K_DOWN:
                    playerkey=4
    
            # Behavior for key press
            if playerkey == 1:# left
                playerdx=-1# position increment
                playerdy=0# cancel to avoid moving diagonally
                playerax=playerx# reset arrows
                playeray=playery
                playerstate=1# player image
            if playerkey == 2:# right
                playerdx=1
                playerdy=0
                playerax=playerx
                playeray=playery
                playerstate=2
            if playerkey == 3:# up
                playerdy=1
                playerdx=0
                playerax=playerx
                playeray=playery
                playerstate=3
            if playerkey == 4:# down
                playerdy=-1
                playerdx=0
                playerstate=4
                playerax=playerx
                playeray=playery            

        ############################
        # Timer and Beat
        
        timenew=pygame.time.get_ticks()# measure current time
        newbeat = False# reset previous new beat if any
        if timenew > timeold+beat:# New beat detected
            newbeat = True
            timeold = timenew# reset time     
            if beat > beatmax:# increase beat if below max value
                beat=60000*beat/(60000+bpminc*beat)
                
        ##############################
        # Update and Clean on New Beat
                
        if newbeat:
            bannerstate=-bannerstate# change banner score
            playerscore=playerscore+1# playerscore is number of waves
            bouldercrackgrid = [0,0,0,0,0,0,0,0,0]# remove previous cracked boulders
            bouldersmokegrid=[0,0,0,0,0,0,0,0,0]# remove previous boulder smoke
            boulderdestroygrid=[0,0,0,0,0,0,0,0,0]# remove previous boulder destroy
                
        ##############################
        # Player Moves or Breaks a Boulder
            
        if newbeat:
                        
            # Cancel Player movement if going outside of grid
            if playerx == 1 and playerdx == -1: playerdx = 0# left edge
            if playerx == 3 and playerdx ==  1: playerdx = 0# right edge
            if playery == 3 and playerdy ==  1: playerdy = 0# top edge
            if playery == 1 and playerdy == -1: playerdy = 0# bottom edge
            
            # Determine Moving or Breaking a Boulder
            if playerdx != 0 or playerdy != 0:# if player wants to move
                iplaynew=get_indexfromcoords(playerx+playerdx,playery+playerdy)# index of desired spot
                boulderisblocking=bouldertheregrid[iplaynew]-boulderwarninggrid[iplaynew]
                
                if boulderisblocking==1:# boulder is blocking (O but not XO), destroy boulder
                    
                    bouldertheregrid[iplaynew] = 0# remove boulder
                    bouldercrackgrid[iplaynew] = 1# add cracked boulder
                    playerarrowdirection = 0# reset player arrow
                    playermoney = playermoney+1# increase score
                    if playermute == 0: playersoundbreak.play()# play break sound
                
                else: # nothing is blocking (or X), move player
                    
                    playerx=playerx+playerdx# update coordinates
                    playery=playery+playerdy
                    if playerx < 1:# restrict if going out of grid 
                        playerx=1 
                    elif playerx > 3:
                        playerx=3       
                    if playery < 1: 
                        playery=1 
                    elif playery > 3:
                        playery=3             
                    if playermute == 0: playersounddash.play()# play move sound
                
                # Reset player position increment
                playerdx=0
                playerdy=0 
                
                

        
        ##############################
        # Update Player Arrows direction (any beat)
        
        playerarrowdirection=0# reset arrow direction    
        if playerdx == -1 and playerx > 1: playerarrowdirection=1 # left
        if playerdx ==  1 and playerx < 3: playerarrowdirection=2  # right  
        if playerdy ==  1 and playery < 3: playerarrowdirection=3 # up
        if playerdy == -1 and playery > 1: playerarrowdirection=4# down
        
        ############################        
        # Update falled boulders (use current boulder and previous warnings)
                
        if newbeat:
            bouldersmokegrid = boulderwarninggrid# add smoke to falled boulders (except XO)
            bouldertheregrid=[x + y for x, y in zip(bouldertheregrid, boulderwarninggrid)]        
            for i in range(9):
                if bouldertheregrid[i] > 1:# Remove boulder and smoke if spot was XO
                    bouldertheregrid[i]=0
                    bouldersmokegrid[i]=0
                    
        ############################
        # Update boulder changes
            
        if newbeat:
            
            # Compute new boulder changes (warning X, or decay XO if boulder there)
            boulderwarninggrid = [0,0,0,0,0,0,0,0,0]# reset boulder warnings
            nwarnings=random.randint(bouldermin,bouldermax)# random select number
            for i in range(nwarnings):# random select locations
                iwarn=random.choice(range(9))
                boulderwarninggrid[iwarn]=1
            
            # Remove warnings if cause certain death
            # e.g. player has incoming X and is surrounded by X or O (but not XO)                
            iplaynew=get_indexfromcoords(playerx,playery)# player position index    
            if boulderwarninggrid[iplaynew]==1:# if incoming X on player
                neighbors=get_neighbors(iplaynew)# get index list of neighbors
                i1=[bouldertheregrid[i] for i in neighbors]
                i2=[boulderwarninggrid[i] for i in neighbors]
                neighborsunsafe=[x + y for x, y in zip(i1, i2)]# unsafe spots: X,O but not XO
                for i in range(len(neighborsunsafe)):
                    if neighborsunsafe[i]>1:
                        neighborsunsafe[i]=0
                if sum(neighborsunsafe)/len(neighborsunsafe) == 1:# all neighbors unsafe
                    iflip=random.choice(neighbors)# make one random neighbor safe (flip warning)
                    if boulderwarninggrid[iflip]==1:
                        boulderwarninggrid[iflip]=0
                    else:
                        boulderwarninggrid[iflip]=1

        ############################
        # Compute boulder that will fall on others (and destroy them)
                    
        if newbeat:
            boulderdestroygrid=[x + y for x, y in zip(bouldertheregrid, boulderwarninggrid)] 
            for i in range(9):
                if boulderdestroygrid[i] == 1:# will not destroy
                    boulderdestroygrid[i]=0  
                if boulderdestroygrid[i] == 2:# will destroy
                    boulderdestroygrid[i]=1
                     
        ############################
        # If player hit last wave, remove blocks for additional wave
                    
        if newbeat:
            if playerhit == 1:
                boulderwarninggrid = [0,0,0,0,0,0,0,0,0]# remove everything
                bouldertheregrid   = [0,0,0,0,0,0,0,0,0]
                bouldersmokegrid   = [0,0,0,0,0,0,0,0,0] 
                bouldercrackgrid   = [0,0,0,0,0,0,0,0,0]
                boulderdestroygrid = [0,0,0,0,0,0,0,0,0]
                playerhit=0# erase previous hit if any
                
        ############################
        #  Check if player has been hit or died           
        if newbeat:            
            iplay=get_indexfromcoords(playerx,playery)# player position index 
            if bouldertheregrid[iplay]==1:# hit by boulder
                playerlife=playerlife-1# remove one life

                # Update to Dead or Just Hit
                if playerlife <1: # Dead                    
                    bouldertheregrid[iplay]=0# remove everything from player spot
                    boulderwarninggrid[iplay]=0
                    bouldersmokegrid[iplay]=0
                    bouldercrackgrid[iplay]=0
                    boulderdestroygrid[iplay]=0      
                    died = True
                    playing = False
                    
                else: # Hit but alive
                    playerhit=1# change to hit state
                    beat=60000/bpmstart# lower hit back to minimum
                    boulderwarninggrid = [0,0,0,0,0,0,0,0,0]# remove everything
                    bouldertheregrid   = [0,0,0,0,0,0,0,0,0]
                    bouldersmokegrid   = [0,0,0,0,0,0,0,0,0] 
                    bouldercrackgrid   = [0,0,0,0,0,0,0,0,0]
                    boulderdestroygrid = [0,0,0,0,0,0,0,0,0]
                    if playermute == 0: playersounddeath .play()# play pain sound   
                
        ############################
        # Display 
                    
        screen.fill((255, 255, 255))# fill screen with RGB (range 0-255)
        screen.blit(imgbackground, (0, 0)) # Display background image 
        display_banner(bannerstate)# Display banner
        display_bouldercrack(bouldercrackgrid)# Display cracked boulders
        display_boulder(bouldertheregrid)# Display boulders 
        display_boulderchanges(boulderwarninggrid, bouldertheregrid)# Display boulder warnings 
        display_bouldersmoke(bouldersmokegrid)# Display boulder smoke 
        display_player(playerx,playery,playerstate,playerhit)# Display player  
        display_playerarrow(playerax,playeray,playerarrowdirection)# Display player arrows
        display_score(playerscore,beat,playermoney,playerlife,playerdifficulty)# Display infos
        pygame.display.update()# Update Screen during Game Loop
    
    
    ##########################################################
    ##########################################################
    
    ##########################################################
    ##########################################################
    # DEATH PAGE
      

    while died:
        
        ############################
        # Initiate Death event
        
        if playerstate != 5:# just not dead yet
            if playermute == 0: playersounddeathfinal.play()# play dead sound
            pygame.mixer.music.fadeout(3000)# fadeout music (3000 ms)
            playerarrowdirection=0# remove arrow
            playerstate=5# set player state to dead
        
        ############################
        #Check for button/key press
            
        for event in pygame.event.get():
            
            # Close the window (quit game)
            if event.type == pygame.QUIT:
                ingame = False# exit hyperloop
                died = False# exit death page
            
            # if keystroke is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    starting = True# go to start page
                    died = False# exit death page
                    
        ############################
        # Display         
                    
        screen.fill((255, 255, 255))# fill screen with RGB (range 0-255) 
        screen.blit(imgbackground, (0, 0)) # Display background image 
        display_boulder(bouldertheregrid)# Display boulders 
        display_bouldercrack(bouldercrackgrid)# Display cracked boulders          
        display_bouldersmoke(bouldersmokegrid)# Display boulder smoke         
        display_player(playerx,playery,playerstate,playerhit)# Display player  
        # display_playerarrow(playerax,playeray,playerarrowdirection)# Display player arrows (remove)
        display_score(playerscore,beat,playermoney,playerlife,playerdifficulty)# Display infos       
        screen.blit(imgdiedoverlay, (0, 0))# Display death overlay        
        pygame.display.update()# Update Screen during Game Loop


# End of Hyper Game Loop    
##########################################################
##########################################################
##########################################################
##########################################################
                
# Quit Game 
pygame.display.quit()
pygame.mixer.music.stop()
pygame.quit()

