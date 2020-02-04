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
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
display_width = 400
display_height = 400
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
        self.learning_rate = 0.002
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
        if act == 2:
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
        data = [data1,data2,data3,data5,data6,binary_x]
    elif snake_obj.dir == "l":
        data = [data1,data2,data4,data6,data5,binary_x]
    elif snake_obj.dir == "d":
        data = [data1,data2,data5,data4,data3,binary_y]
    elif snake_obj.dir == "u":
        data = [data1,data2,data6,data3,data4,binary_y]
    return data
#define the main game loop

def GameLoop():
    state_size = 6
    action_size = 3
    agent = DQNAgent(state_size, action_size)
    print('state size:' ,state_size)
    print('action size: ', action_size)
    batch_size = 1024
    output_dir = 'C:/Users/subha/Desktop/python_codes/project4'
    for e in range(EPISODES):
        gameOver = False
        score = 0
        action_performed = 0
        snake_obj = Snake()
        apple_obj = Apple()
        C_state = get_state(snake_obj,apple_obj)
        C_state = np.array(C_state)
        C_state = np.reshape(C_state,[1,state_size])
        while not gameOver:
            reward = 0
            gameDisplay.fill(white)
            pygame.display.update()
            action_performed = agent.act(C_state)
            apple_obj.draw()
            snake_obj.draw(action_performed)
            apple_eaten(snake_obj,apple_obj)
            gameOver = collision(snake_obj)
            show_score(snake_obj)
            N_state = get_state(snake_obj,apple_obj)
            N_state = np.array(N_state)
            N_state = np.reshape(N_state,[1,state_size])
            #print(C_state[0],"->",N_state[0])
            if N_state[0][5] == 1:
                reward += 1000 / (N_state[0][1] + 1)
            if gameOver:
                reward -= 1000
            if N_state[0][5] == 0:
                reward -= N_state[0][1]
            agent.remember(C_state, action_performed, reward, N_state, gameOver)
            C_state = N_state
            score += reward
            clock.tick(fps)

        print("episode: {}/{}, score: {}, e: {:.2}".format(e, EPISODES, score, agent.epsilon))

        if len(agent.memory) > batch_size:
            print("replaying memory----------------->")
            agent.replay(batch_size)

        if e % 50 == 0:
            print('saving the model')
            agent.save(output_dir + "/" + str(e) + ".hdf5")

    pygame.quit()

GameLoop()
quit()
