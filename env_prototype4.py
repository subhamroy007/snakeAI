#import necessery modules
import pygame
import random
import math

#setup/initialize the environment
black = (20,20,20)
white = (230,230,230)
red = (230,0,0)
green = (0,230,0)
blue = (0,0,230)
display_width = 100
display_height = 100
clock = pygame.time.Clock()
fps = 15


pygame.init()

font = pygame.font.SysFont("Arial.ttf",30)

pygame.display.set_caption("snake environment for data fetch")

gameDisplay = pygame.display.set_mode((display_width,display_height))




#define snake class
class Snake():
    def __init__(self):
        self.length_counter = 1
        self.body_list = []
        self.head_x = display_width / 2
        self.head_y = display_height / 2
        self.head_x_change = 0
        self.head_y_change = 0
        self.body_thickness = 20
    def draw(self):
        self.head_x += self.head_x_change
        self.head_y += self.head_y_change
        self.body_list.append([self.head_x,self.head_y])
        if len(self.body_list) > self.length_counter:
            del self.body_list[0]
        for XnY in self.body_list[:-1]:
            pygame.draw.rect(gameDisplay,white,[XnY[0],XnY[1],self.body_thickness,self.body_thickness])
        pygame.draw.rect(gameDisplay,red,[self.body_list[-1][0],self.body_list[-1][1],self.body_thickness,self.body_thickness])
        pygame.display.update()

#define apple class
class Apple():
    def __init__(self):
        self.thickness = 20
        self.x_pos = round(random.randrange(0,display_width-self.thickness)/self.thickness)*self.thickness
        self.y_pos = round(random.randrange(0,display_height-self.thickness)/self.thickness)*self.thickness
    def draw(self):
        pygame.draw.rect(gameDisplay,blue,[self.x_pos,self.y_pos,self.thickness,self.thickness])
        pygame.display.update()

#define apple eaten function

def apple_eaten(snake_obj,apple_obj):
    if apple_obj.x_pos == snake_obj.head_x and apple_obj.y_pos == snake_obj.head_y:
        snake_obj.length_counter += 1
        apple_obj.x_pos = round(random.randrange(0,display_width-apple_obj.thickness)/apple_obj.thickness)*apple_obj.thickness
        apple_obj.y_pos = round(random.randrange(0,display_height-apple_obj.thickness)/apple_obj.thickness)*apple_obj.thickness
        while True:
            if (apple_obj.x_pos,apple_obj.y_pos) in snake_obj.body_list:
                apple_obj.x_pos = round(random.randrange(0,display_width-apple_obj.thickness)/apple_obj.thickness)*apple_obj.thickness
                apple_obj.y_pos = round(random.randrange(0,display_height-apple_obj.thickness)/apple_obj.thickness)*apple_obj.thickness
            else:
                break



#define game over function

def show_game_over_screen():
    gameOver = True
    gameExit = False
    text = "game over press p to play again or q to quit"
    text_to_screen = font.render(text,True,blue)
    text_rect = text_to_screen.get_rect()
    text_rect.center = display_width/2 , display_height/2
    while gameOver:
        gameDisplay.blit(text_to_screen,text_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = False
                gameExit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    GameLoop()
                    gameOver = False
                    gameExit = True
                elif event.key == pygame.K_q:
                    gameOver = False
                    gameExit = True
    return gameOver,gameExit


#define collision function

def collision(snake_obj):
    gameOver = False
    if snake_obj.head_x >= display_width or snake_obj.head_x < 0 or snake_obj.head_y >= display_height or snake_obj.head_y < 0:
        gameOver = True
    else:
        for XnY in snake_obj.body_list[:-1]:
            if XnY == snake_obj.body_list[-1]:
                gameOver = True
                break
    return gameOver


#define show score function

def show_score(snake_obj):
    text = str(snake_obj.length_counter-1)
    text_to_screen = font.render(text,True,green)
    gameDisplay.blit(text_to_screen,[0,0])
    pygame.display.update()


def mod(x):
    if x>=0:
        return x
    return -x

def get_action(act):
    print(act , "\n")



#defining get_state function
def get_state(snake_obj,apple_obj):
    data_u = snake_obj.head_y / snake_obj.body_thickness
    data_l = snake_obj.head_x / snake_obj.body_thickness
    data_r = (display_width - snake_obj.head_x - snake_obj.body_thickness)/snake_obj.body_thickness
    data_d = (display_height - snake_obj.head_y - snake_obj.body_thickness)/snake_obj.body_thickness
    data_ul = 0
    data_ur = 0
    data_dl = 0
    data_dr = 0
    if data_u > data_l:
        data_ul = data_l * 2 ** .5
    else:
        data_ul = data_u * 2 ** .5

    if data_u > data_r:
        data_ur = data_r * 2 ** .5
    else:
        data_ur = data_u * 2 ** .5

    if data_d > data_l:
        data_dl = data_l * 2 ** .5
    else:
        data_dl = data_d * 2 ** .5

    if data_d > data_r:
        data_dr = data_r * 2 ** .5 - (apple_obj.thickness/snake_obj.body_thickness) * 2 ** .5
    else:
        data_dr = data_d * 2 ** .5 - (apple_obj.thickness/snake_obj.body_thickness) * 2 ** .5

    data_ul = round(data_ul,2)
    data_ur = round(data_ur,2)
    data_dl = round(data_dl,2)
    data_dr = round(data_dr,2)

    bin_app_u = 0
    bin_app_d = 0
    bin_app_r = 0
    bin_app_l = 0
    bin_app_ul = 0
    bin_app_ur = 0
    bin_app_dl = 0
    bin_app_dr = 0

    if mod(apple_obj.x_pos - snake_obj.head_x) == mod(apple_obj.y_pos - snake_obj.head_y):
        if apple_obj.x_pos > snake_obj.head_x and apple_obj.y_pos > snake_obj.head_y:
            bin_app_dr = 1
        elif apple_obj.x_pos < snake_obj.head_x and apple_obj.y_pos < snake_obj.head_y:
            bin_app_ul = 1
        elif apple_obj.x_pos > snake_obj.head_x and apple_obj.y_pos < snake_obj.head_y:
            bin_app_ur = 1
        elif apple_obj.x_pos < snake_obj.head_x and apple_obj.y_pos > snake_obj.head_y:
            bin_app_dl = 1
    elif apple_obj.x_pos == snake_obj.head_x:
        if apple_obj.y_pos > snake_obj.head_y:
            bin_app_d = 1
        else:
            bin_app_u = 1
    elif apple_obj.y_pos == snake_obj.head_y:
        if apple_obj.x_pos > snake_obj.head_x:
            bin_app_r = 1
        else:
            bin_app_l = 1



    bin_bod_u = 0
    bin_bod_d = 0
    bin_bod_r = 0
    bin_bod_l = 0
    bin_bod_ul = 0
    bin_bod_ur = 0
    bin_bod_dl = 0
    bin_bod_dr = 0
    for XnY in snake_obj.body_list[:-1]:
        if mod(XnY[0] - snake_obj.head_x) == mod(XnY[1] - snake_obj.head_y):
            if XnY[0] > snake_obj.head_x and XnY[1] > snake_obj.head_y:
                bin_bod_dr = 1
            elif XnY[0] < snake_obj.head_x and XnY[1] < snake_obj.head_y:
                bin_bod_ul = 1
            elif XnY[0] > snake_obj.head_x and XnY[1] < snake_obj.head_y:
                bin_bod_ur = 1
            elif XnY[0] < snake_obj.head_x and XnY[1] > snake_obj.head_y:
                bin_bod_dl = 1
        elif XnY[0] == snake_obj.head_x:
            if XnY[1] > snake_obj.head_y:
                bin_bod_d = 1
            else:
                bin_bod_u = 1
        elif XnY[1] == snake_obj.head_y:
            if XnY[0] > snake_obj.head_x:
                bin_bod_r = 1
            else:
                bin_bod_l = 1



    state = [bin_bod_u,bin_bod_l,bin_bod_r,bin_bod_d,bin_bod_ul,bin_bod_ur,bin_bod_dl,bin_bod_dr]
    #state = [bin_app_u,bin_app_l,bin_app_r,bin_app_d,bin_app_ul,bin_app_ur,bin_app_dl,bin_app_dr]
    #state = [data_u,data_l,data_r,data_d,data_ul,data_ur,data_dl,data_dr]
    print(state)

def GameLoop():
    global display_width
    global display_height
    display_width += 100
    display_height += 100
    gameOver = False
    gameExit = False
    action_performed = 0
    snake_obj = Snake()
    apple_obj = Apple()
    while not gameExit:
        gameDisplay = pygame.display.set_mode((display_width,display_height))
        gameDisplay.fill(black)
        if gameOver:
            gameOver,gameExit = show_game_over_screen()
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake_obj.head_x_change = -snake_obj.body_thickness
                    snake_obj.head_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    snake_obj.head_x_change = snake_obj.body_thickness
                    snake_obj.head_y_change = 0
                elif event.key == pygame.K_UP:
                    snake_obj.head_y_change = -snake_obj.body_thickness
                    snake_obj.head_x_change = 0
                elif event.key == pygame.K_DOWN:
                    snake_obj.head_y_change = snake_obj.body_thickness
                    snake_obj.head_x_change = 0

        apple_obj.draw()
        snake_obj.draw()
        get_state(snake_obj,apple_obj)
        #get_action(action_performed)
        apple_eaten(snake_obj,apple_obj)
        gameOver = collision(snake_obj)
        show_score(snake_obj)
        clock.tick(fps)

    pygame.quit()


GameLoop()
quit()
