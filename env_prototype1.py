#this is the first prototype for snake game environment to configure manual control in the game
import random
import pygame
import time


white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

block_size = 20
fps = 15
display_width = 800
display_height = 600

clock = pygame.time.Clock()

pygame.init()

font = pygame.font.SysFont("Helvatica",25)




gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("snake game environment 1")


#pygame.display.update()
def score(snake_length):
    score_text = str(snake_length-1)
    screen_text = font.render(score_text,True,black)
    gameDisplay.blit(screen_text,[1,1])
def snake(snake_list):
    for XnY in snake_list:
        pygame.draw.rect(gameDisplay,black,[XnY[0],XnY[1],block_size,block_size])


def messege_to_screen(msg,color):
    text_to_screen = font.render(msg,True,color)
    gameDisplay.blit(text_to_screen,[display_width/2,display_height/2])


def GameLoop():
    gameExit = False
    lead_x = display_width/2
    lead_y = display_height/2
    lead_x_change = 0
    lead_y_change = 0
    snake_list = []
    snake_length = 1
    randAppleX = round(random.randrange(0,display_width-block_size) / block_size)*block_size
    randAppleY = round(random.randrange(0,display_height-block_size) / block_size)*block_size
    gameOver = False

    while not gameExit:

        while gameOver:
            messege_to_screen("you loose press p to play again or q to quit",red)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        GameLoop()
                    elif event.key == pygame.K_q:
                        gameOver = False
                        gameExit = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and lead_x_change == 0:
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT and lead_x_change == 0:
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP and lead_y_change == 0:
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN and lead_y_change == 0:
                    lead_y_change = block_size
                    lead_x_change = 0
            #print(event.type)
        lead_x += lead_x_change
        lead_y += lead_y_change
        if lead_x >= display_width or lead_y >= display_height or lead_x < 0 or lead_y <0:
            gameOver = True
        gameDisplay.fill(white)
        score(snake_length)
        snake_list.append([lead_x,lead_y])
        if len(snake_list) > snake_length:
            del snake_list[0]
        snake(snake_list)
        for XnY in snake_list[:-1]:
            if XnY == snake_list[snake_length-1]:
                gameOver = True
                break
        pygame.draw.rect(gameDisplay,red,[randAppleX,randAppleY,block_size,block_size])
        #gameDisplay.fill(red,rect = [200,200,20,20])
        pygame.display.update()
        if lead_x == randAppleX and lead_y == randAppleY:
            snake_length += 1
            randAppleX = round(random.randrange(0,display_width-block_size) / block_size)*block_size
            randAppleY = round(random.randrange(0,display_height-block_size) / block_size)*block_size

        clock.tick(fps)

    pygame.quit()
GameLoop()
quit()
