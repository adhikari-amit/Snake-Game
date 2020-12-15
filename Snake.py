import pygame
import random
import os

pygame.mixer.init()
pygame.init()

#colors
white=(255,255,255)
red=(255,0,0)
black=(0,0,0)
blue=(40,240,180)
green=(40,240,120)

#creating window
screen_hight=650
screen_width=400
gamewindow=pygame.display.set_mode((screen_hight,screen_width))
pygame.display.update()
background=pygame.image.load('background.jpg')
background=pygame.transform.scale(background,(screen_hight,screen_width)).convert_alpha()
welcome_screen=pygame.image.load('welcome.jpg')
welcome_screen=pygame.transform.scale(welcome_screen,(screen_hight,screen_width)).convert_alpha()
game_over_screen=pygame.image.load('Gameover.jpg')
game_over_screen=pygame.transform.scale(game_over_screen,(screen_hight,screen_width)).convert_alpha()

#set Title   
pygame.display.set_caption("Snakey")
pygame.display.update()

#Game specific variable
clock=pygame.time.Clock()
font =pygame.font.SysFont(None,25)
def text_screen(text,color,x,y):
    screen_text=font.render(text,True,color)
    gamewindow.blit(screen_text,[x,y])

def plot_snake(gamewindow,color,snake_list,snake_size):
    for x,y in snake_list:
        pygame.draw.ellipse(gamewindow,color,[x,y,snake_size,snake_size])    

def apple_plot(x,y):
    apple=pygame.image.load('apple.png')
    gamewindow.blit(apple,(x,y))        

def welcome():
    exit_game=False
    while not exit_game:
        
        gamewindow.blit(welcome_screen,(0,0))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit_game=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    gameloop()
        pygame.display.update()
        clock.tick(60)                
#Game loop
def gameloop():
    pygame.mixer.music.load('pirates-of-the-caribbean-hes-a-pirate-extended.mp3')
    pygame.mixer.music.play()
    exit_game=False
    game_over=False
    snake_x=45
    snake_y=45
    snake_size=13
    velocity_x=0
    velocity_y=0
    init_velocity=5
    fps=25
    score=0
    apple_x=random.randint(20,screen_hight-20)
    apple_y=random.randint(20,screen_width-20)
    snake_list=[]
    snake_length=1
    #check if highscore file exist
    if(not os.path.exists("Highscore.txt")):
        with open("Highscore.txt","w")as f:
            f.write("0")
    with open ("Highscore.txt","r") as f:
        Highscore=f.read()    

    while not exit_game:
        if game_over:
            with open("Highscore.txt","w") as f:
                f.write(str(Highscore))
            gamewindow.blit(game_over_screen,(0,0)) 
        
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        gameloop()    
        else:    
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game=True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x=init_velocity
                        velocity_y=0
                    if event.key == pygame.K_LEFT:
                        velocity_x=-init_velocity
                        velocity_y=0 
                    if event.key == pygame.K_UP:
                        velocity_y=-init_velocity
                        velocity_x=0
                    if event.key == pygame.K_DOWN:
                        velocity_y=init_velocity
                        velocity_x=0
                        #cheat code
                    if event.key==pygame.K_q:
                        score+=20             

            snake_x+=velocity_x
            snake_y+=velocity_y
            if abs(snake_x-apple_x)<8 and abs(snake_y-apple_y)<8:
                # pygame.mixer.music.load('beep.mp3')
                # pygame.mixer.music.play()
                score+=10
                apple_x=random.randint(20,screen_hight-20)
                apple_y=random.randint(20,screen_width-20)
                snake_length+=3
                if score>int(Highscore):
                    Highscore=score
       
            gamewindow.blit(background,(0,0))  
            text_screen("Score:"+str(score),black,500,1) 
            text_screen("High Score:"+str(Highscore),black,500,15)    
            # pygame.draw.rect(gamewindow,red,[apple_x,apple_y,snake_size,snake_size]) 
            apple_plot(apple_x,apple_y)
            head=[]
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)
            if len(snake_list)>snake_length:
                del snake_list[0]
        
            if snake_x<=0 or snake_x>=screen_hight or snake_y<=0 or snake_y>=screen_width:
                game_over=True
                pygame.mixer.music.load('coffin-dance-piano.mp3')
                pygame.mixer.music.play()

            if head in snake_list[:-1]:
                game_over=True
                pygame.mixer.music.load('coffin-dance-piano.mp3')
                pygame.mixer.music.play()

            plot_snake(gamewindow,(255,70,70),snake_list,snake_size)
        pygame.display.update()
        clock.tick(fps)    
        
    pygame.quit()
    quit()
welcome()    
