import pygame
from pygame.locals import *
import time
import random
SIZE = 40
BACKGROUND_COLOR = (110,110,5)

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        #Since the length of the window is 1000px, 1000 / 40 = 25
        self.x = random.randint(0, 24)* SIZE
        self.y = random.randint(0, 19)*SIZE

class Snake:
    def __init__(self, surface, length):
        self.length = length
        self.parent_screen = surface
        #load image from resources folder
        self.block = pygame.image.load("resources/block.jpg").convert()

        self.x = [SIZE]*length #x-axis
        self.y = [SIZE]*length #y-axis
        self.direction = ''

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        
        #Reset the display
        #Place the block in the new coordinate
        #Set background color: green
        #parent_screen represents the surface attribute
        self.parent_screen.fill((110,110,5))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()
    
    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'
    
    def move_down(self):
        self.direction = 'down'

    def walk(self):
        for i in range(self.length -1,0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        
        self.draw()
        

class Game:
    def __init__(self):
        #Initialize the module
        pygame.init()

        pygame.mixer.init()
        #start playing background music once the game starts
        self.play_background_music()

        #Initialize a window or screen for display: size of the window
        self.surface = pygame.display.set_mode((1000, 800))
        #Set background color: green
        self.surface.fill((110,110,5))
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.snake.draw()

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (255,255,255))
        self.surface.blit(score, (880, 40))

    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()


    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        
        pygame.mixer.Sound.play(sound)



    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        #Snake colliding with the apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.apple.move()
            #increase the length of snake by 1
            self.snake.increase_length()

        #Snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Game over"
    
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True

    def show_game_over(self):
        #Clear the surface
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255,255,255))
        self.surface.blit(line1, (200,300))
        line2 = font.render("Hit Enter to play again!", True, (255,255,255))
        self.surface.blit(line2, (200, 350))

        pygame.display.flip()

        #Pause or stop the background music
        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def render_background(self):
        bg = pygame.image.load('resources/background.jpg').convert()
        self.surface.blit(bg, (0,0))

    
    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    #If the esc key is pressed, the program will stop running.
                    if event.key == K_ESCAPE:
                        running = False

                    if not pause:
                        #If the up key is pressed, the x-axis remains the same while the y-axis changes
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:                      
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            
            time.sleep(0.3) #Add delay
    

if __name__ == "__main__":
    game = Game()
    game.run()
