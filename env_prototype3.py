#this is the final prototype of the snake game environment where at each iteration the snake will choose random action between three actions
#those are do nothing or rotate clockwise 90 or rotate anti clockwise 90 and return the state after each actions
#import necessery modules
import pygame
import random

#setup/initialize the environment
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
display_width = 400
display_height = 400
clock = pygame.time.Clock()
fps = 30

pygame.init()

font = pygame.font.SysFont("Arial.ttf",15)

pygame.display.set_caption("snake environment for data fetch")

gameDisplay = pygame.display.set_mode((display_width,display_height))




#define snake class
class Snake():
    def __init__(self):
        self.dir = "r"
        self.length_counter = 1
        self.body_list = []
        self.body_thickness = 20
        self.head_x = display_width / 2
        self.head_y = display_height / 2
        self.head_x_change = self.body_thickness
        self.head_y_change = 0
    def draw(self,act):
        if act == 1:
            if self.dir == "r":
                self.dir = "d"
                self.head_x_change = 0
                self.head_y_change = self.body_thickness
            elif self.dir == "l":
                self.dir = "u"
                self.head_x_change = 0
                self.head_y_change = -self.body_thickness
            elif self.dir == "u":
                self.dir = "r"
                self.head_x_change = self.body_thickness
                self.head_y_change = 0
            elif self.dir == "d":
                self.dir = "l"
                self.head_x_change = -self.body_thickness
                self.head_y_change = 0
        if act == -1:
            if self.dir == "r":
                self.dir = "u"
                self.head_x_change = 0
                self.head_y_change = -self.body_thickness
            elif self.dir == "l":
                self.dir = "d"
                self.head_x_change = 0
                self.head_y_change = self.body_thickness
            elif self.dir == "u":
                self.dir = "l"
                self.head_x_change = -self.body_thickness
                self.head_y_change = 0
            elif self.dir == "d":
                self.dir = "r"
                self.head_x_change = self.body_thickness
                self.head_y_change = 0
        else:
            pass
        self.head_x += self.head_x_change
        self.head_y += self.head_y_change
        self.body_list.append([self.head_x,self.head_y])
        if len(self.body_list) > self.length_counter:
            del self.body_list[0]
        for XnY in self.body_list:
            pygame.draw.rect(gameDisplay,green,[XnY[0],XnY[1],self.body_thickness,self.body_thickness])
        pygame.display.update()

#define apple class
class Apple():
    def __init__(self):
        self.thickness = 20
        self.x_pos = round(random.randrange(0,display_width-self.thickness)/self.thickness)*self.thickness
        self.y_pos = round(random.randrange(0,display_height-self.thickness)/self.thickness)*self.thickness
    def draw(self):
        pygame.draw.rect(gameDisplay,red,[self.x_pos,self.y_pos,self.thickness,self.thickness])
        pygame.display.update()




#define apple eaten function

def apple_eaten(snake_obj,apple_obj):
    if apple_obj.x_pos == snake_obj.head_x and apple_obj.y_pos == snake_obj.head_y:
        snake_obj.length_counter += 1
        apple_obj.x_pos = round(random.randrange(0,display_width-apple_obj.thickness)/apple_obj.thickness)*apple_obj.thickness
        apple_obj.y_pos = round(random.randrange(0,display_height-apple_obj.thickness)/apple_obj.thickness)*apple_obj.thickness




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
    return gameExit


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
    text_to_screen = font.render(text,True,black)
    gameDisplay.blit(text_to_screen,[0,0])
    pygame.display.update()


def mod(x):
    if x>=0:
        return x
    return -x


#defining get_state function
def get_state(snake_obj,apple_obj):
    data1 = snake_obj.length_counter
    data2 = mod(snake_obj.head_x - apple_obj.x_pos)/10 + mod(snake_obj.head_y - apple_obj.y_pos)/apple_obj.thickness
    data3  = (display_width - snake_obj.head_x - snake_obj.body_thickness)/apple_obj.thickness
    for XnY in snake_obj.body_list[:-1]:
        if XnY[1] == snake_obj.head_y and XnY[0] >= snake_obj.head_x + apple_obj.thickness and (XnY[0] - snake_obj.head_x-apple_obj.thickness) < data3:
            data3 = XnY[0] - snake_obj.head_x - apple_obj.thickness
    data4  = snake_obj.head_x / apple_obj.thickness
    for XnY in snake_obj.body_list[:-1]:
        if XnY[1] == snake_obj.head_y and XnY[0] + apple_obj.thickness <= snake_obj.head_x and (snake_obj.head_x - XnY[0] - apple_obj.thickness) < data4:
            data4 = snake_obj.head_x - XnY[0] - apple_obj.thickness
    data5  = (display_height - snake_obj.head_y - snake_obj.body_thickness)/apple_obj.thickness
    for XnY in snake_obj.body_list[:-1]:
        if XnY[0] == snake_obj.head_x and XnY[1] >= snake_obj.head_y + apple_obj.thickness and (XnY[1] - snake_obj.head_y - apple_obj.thickness) < data5:
            data5 = XnY[1] - snake_obj.head_y
    data6  = snake_obj.head_y / apple_obj.thickness
    for XnY in snake_obj.body_list[:-1]:
        if XnY[0] == snake_obj.head_x and XnY[1] + apple_obj.thickness <= snake_obj.head_y and (snake_obj.head_y - XnY[1] - apple_obj.thickness) < data6:
            data6 = snake_obj.head_y - XnY[1] - apple_obj.thickness
    binary_x = 0
    binary_y = 0
    if snake_obj.head_x == apple_obj.x_pos:
        binary_x = 1
    if snake_obj.head_y == apple_obj.y_pos:
        binary_y = 1


    if snake_obj.dir == "r":
        data = (data1,data2,data3,data5,data6,binary_x)
    elif snake_obj.dir == "l":
        data = (data1,data2,data4,data6,data5,binary_x)
    elif snake_obj.dir == "d":
        data = (data1,data2,data5,data4,data3,binary_y)
    elif snake_obj.dir == "u":
        data = (data1,data2,data6,data3,data4,binary_y)
    return data

#define the main game loop

def GameLoop():
    gameExit = False
    while not gameExit:
        gameOver = False
        action_performed = 0
        snake_obj = Snake()
        apple_obj = Apple()
        print(get_state(snake_obj,apple_obj),"\t",gameOver)
        while not gameOver:
            gameDisplay.fill(white)
            pygame.display.update()
            action_performed = random.randrange(-1,1)
            apple_obj.draw()
            snake_obj.draw(action_performed)
            apple_eaten(snake_obj,apple_obj)
            gameOver = collision(snake_obj)
            show_score(snake_obj)
            print(get_state(snake_obj,apple_obj),"\t",gameOver)
            clock.tick(fps)

        gameExit = show_game_over_screen()

    pygame.quit()

GameLoop()
quit()
