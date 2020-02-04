import random
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense, Activation,Dropout
from keras.optimizers import Adam
from keras import backend as K
import matplotlib.pyplot as plt
import pygame
import random

#setup/initialize the environment
black = (20,20,20)
white = (230,230,230)
red = (230,0,0)
green = (0,230,0)
blue = (0,0,230)
display_width = 100
display_height = 100
clock = pygame.time.Clock()
fps = 30
EPISODES = 10000


class DQNAgent:

    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.999539589
        self.learning_rate = 0.001
        self.model = self._build_model()
        #self.target_model = self._build_model()
        #self.update_target_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(128, input_dim=self.state_size))
        model.add(Activation('relu'))

        model.add(Dense(128))
        model.add(Activation('relu'))

        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss="mean_squared_error",
                      optimizer=Adam(lr=self.learning_rate))
        return model

    #def update_target_model(self):
        # copy weights from model to target_model
     #   self.target_model.set_weights(self.model.get_weights())

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = self.model.predict(state)
            if done:
                target[0][action] = reward
            else:
                Q_future  = self.model.predict(next_state)[0]
                target[0][action] = reward + self.gamma * np.amax(Q_future)
            self.model.fit(state, target, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self,name):
        self.model.load_weights(name)

    def save(self,name):
        self.model.save_weights(name)



pygame.init()

font = pygame.font.SysFont("Arial.ttf",30)

pygame.display.set_caption("snake environment for data fetch")

gameDisplay = pygame.display.set_mode((display_width,display_height),pygame.RESIZABLE)




#define snake class
class Snake():
    def __init__(self):
        self.length_counter = 1
        self.body_list = []
        self.body_thickness = 20
        self.head_x = round(display_width / 2 / self.body_thickness) * self.body_thickness
        self.head_y = round(display_height / 2 / self.body_thickness) * self.body_thickness
        self.head_x_change = 0
        self.head_y_change = 0
    def draw(self,act):
        if act == 0 and self.head_x_change == 0:
            self.head_x_change = -self.body_thickness
            self.head_y_change = 0
        if act == 1 and self.head_x_change == 0:
            self.head_x_change = self.body_thickness
            self.head_y_change = 0
        if act == 2 and self.head_y_change == 0:
            self.head_y_change = -self.body_thickness
            self.head_x_change = 0
        if act == 3 and self.head_y_change == 0:
            self.head_y_change = self.body_thickness
            self.head_x_change = 0
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
    x = False
    if apple_obj.x_pos == snake_obj.head_x and apple_obj.y_pos == snake_obj.head_y:
        x = True
        snake_obj.length_counter += 1
        apple_obj.x_pos = round(random.randrange(0,display_width-apple_obj.thickness)/apple_obj.thickness)*apple_obj.thickness
        apple_obj.y_pos = round(random.randrange(0,display_height-apple_obj.thickness)/apple_obj.thickness)*apple_obj.thickness
        while True:
            if (apple_obj.x_pos,apple_obj.y_pos) in snake_obj.body_list:
                apple_obj.x_pos = round(random.randrange(0,display_width-apple_obj.thickness)/apple_obj.thickness)*apple_obj.thickness
                apple_obj.y_pos = round(random.randrange(0,display_height-apple_obj.thickness)/apple_obj.thickness)*apple_obj.thickness
            else:
                break
    return x


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

    state = [data_l,bin_app_l,bin_bod_l,data_ul,bin_app_ul,bin_bod_ul,data_u,bin_app_u,bin_bod_u,data_ur,bin_app_ur,bin_bod_ur,data_r,bin_app_r,bin_bod_r,data_dr,bin_app_dr,bin_bod_dr,data_d,bin_app_d,bin_bod_d,data_dl,bin_app_dl,bin_bod_dl]
    #state = [data_u,data_l,data_r,data_d,data_ul,data_ur,data_dl,data_dr,bin_app_u,bin_app_l,bin_app_r,bin_app_d,bin_app_ul,bin_app_ur,bin_app_dl,bin_app_dr,bin_bod_u,bin_bod_l,bin_bod_r,bin_bod_d,bin_bod_ul,bin_bod_ur,bin_bod_dl,bin_bod_dr]
    return state


def GameLoop():
    #global gameDisplay
    global display_width
    global display_height
    state_size = 24
    action_size = 4
    agent = DQNAgent(state_size, action_size)
    print('state size:' ,state_size)
    print('action size: ', action_size)
    batch_size = 256
    output_dir = 'C:/Users/subha/Desktop/python_codes/project4'
    for e in range(EPISODES):
        gameDisplay = pygame.display.set_mode((display_width,display_height),pygame.RESIZABLE)
        gameOver = False
        score = 0
        counter = 0
        action_performed = 0
        snake_obj = Snake()
        apple_obj = Apple()
        C_state = get_state(snake_obj,apple_obj)
        C_state = np.array(C_state)
        C_state = np.reshape(C_state,[1,state_size])
        while not gameOver:
            reward = -1
            gameDisplay.fill(black)
            pygame.display.update()
            action_performed = agent.act(C_state)
            apple_obj.draw()
            snake_obj.draw(action_performed)
            temp = apple_eaten(snake_obj,apple_obj)
            gameOver = collision(snake_obj)
            show_score(snake_obj)
            N_state = get_state(snake_obj,apple_obj)
            N_state = np.array(N_state)
            N_state = np.reshape(N_state,[1,state_size])
            #print(C_state[0],"->",N_state[0])
            if gameOver == True:
                reward -= 100
            if temp == True:
                counter = 0
                reward += 100
            agent.remember(C_state, action_performed, reward, N_state, gameOver)
            C_state = N_state
            score += reward
            counter+=1
            if counter == (display_width / snake_obj.body_thickness) * (display_height / snake_obj.body_thickness)+1:
                break
            clock.tick(fps)

        print("episode: {}/{}, score: {}, e: {:.2}".format(e, EPISODES, score, agent.epsilon))

        if len(agent.memory) > batch_size:
            print("replaying memory----------------->")
            agent.replay(batch_size)

        if e % 50 == 0:

            print('saving the model')
            agent.save(output_dir + "/" + str(e) + ".hdf5")
        if e%1000 == 0 and e > 0:
            print("hello")
            display_width += 100
            display_height += 100


    pygame.quit()

GameLoop()
quit()
