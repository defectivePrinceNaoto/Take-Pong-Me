# pong

## Because, why not.

## Game ends when AI gets 10 points. Player 1's score has no cap. Goal
## is to beat your high score.  Counter turns orange-gold once you beat
## your current high score (which is oddly motivation.. maybe there
## should be a gradual shift in color as goal is approached?)
## Short play field is to encourage quick games. Currently, where the
## ball collides the paddle does not alter the ball's path. May change
## this when I add sound effects, though..


import pygame as pyg
from pygame.locals import *
import random, os, sys

# Constants
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

BLUE = (45, 15, 110)
BLACK = (190, 190, 240)
TRANS = (255, 255, 255)
ORANGE = (255, 179, 80)
RED = (229, 113, 108)
GREEN = (67, 135, 129)
DARKGREEN = (0, 113, 49)
GOLD = (176, 113, 0)

TRUE_BLACK = (0, 0, 0)

WINDOWHEIGHT = 100
WINDOWWIDTH = 100

global score1
score1 = 0
global score2
score2 = 0

class Bar(pyg.sprite.Sprite):
    def __init__(self, x, pc, w=5, h=20, ):
        
        self.pc = pc
        self.X_RAIL = x
        
        self.image = pyg.Surface((w, h))
        
        self.image.fill(BLUE)
        
        self.rect = self.image.get_rect()
        
        self.rect.topleft = (self.X_RAIL, 0)
        
        pyg.sprite.Sprite.__init__(self)
        self.move_speed = 3
        
        
    def move(self, direction):
        if direction is UP:
            if self.rect.y - self.move_speed <= 0:
                self.rect.topleft = (self.X_RAIL, 0)
                
            else:
                self.rect = self.rect.move((0, -self.move_speed))
                
        elif direction is DOWN:
            if self.rect.y+self.rect.height + self.move_speed >= WINDOWHEIGHT:
                self.rect.bottomleft = (self.X_RAIL, WINDOWHEIGHT)
                
            else:
                self.rect = self.rect.move((0, self.move_speed))
                
    def ai(self, ballpos):
        # think about where to move based on the position of the passed ball
        if self.rect.bottomleft[1] > ballpos[1] > self.rect.topleft[1]:
            pass
        elif self.rect.center[1] > ballpos[1]:
            self.move(UP)
        elif self.rect.center[1] < ballpos[1]:
            self.move(DOWN)
                
    def update(self, balls):
        if self.pc != '1': # Isn't 1st Player-aru
            # Focus on a random ball.. stupid, but can expand later.
            ballpos = balls[random.randint(0, len(balls)-1)].rect.center
            if ballpos[0] > WINDOWWIDTH/2:
                self.ai(ballpos)
            
        
    
class Ball(pyg.sprite.Sprite):
    def __init__(self):
        self.image = pyg.Surface((5, 5))
        self.image.fill(TRANS)
        self.image.set_colorkey(TRANS)
        
        pyg.draw.ellipse(self.image, RED, self.image.get_rect())
        
        self.rect = self.image.get_rect()
        
        pyg.sprite.Sprite.__init__(self)
        self.move_speed = 1
        self.rect.center = ((WINDOWWIDTH/2, WINDOWHEIGHT/2))
        
        self.move = False
        
        self.x, self.y = self.rect.center
        
        self.xspeed = 2
        self.yspeed = 2
        
    def bounce(self, coord):
        if coord == 'x':
            self.xspeed = -self.xspeed
        elif coord == 'y':
            self.yspeed = -self.yspeed
        
    def update(self):
        if self.move:
            # left/right walls
            
            if (self.x + self.xspeed <= 0):
                self.bounce('x')
                # point goes to p2
                global score2
                score2 += 1
                
            if (self.x + self.xspeed >= WINDOWWIDTH):
                self.bounce('x')
                # point goes to p1
                global score1
                score1 += 1
                
            # top/bottom walls
            if (self.y + self.yspeed <= 0) or (self.y + self.yspeed >= WINDOWHEIGHT):
                self.bounce('y')
                
            # move
            self.rect = self.rect.move(self.xspeed, self.yspeed)
            self.x, self.y = self.rect.center
            
            
                
            
class Score(object):
    def __init__(self, hiscore):
        
        self.hiscore = hiscore
        
        # make the screen to be drawn upon
        self.image1 = pyg.Surface((WINDOWWIDTH, 15))
        self.image1.fill(TRANS)
        self.image1.set_colorkey(TRANS)
        
        self.image2 = pyg.Surface((WINDOWWIDTH, 15))
        self.image2.fill(TRANS)
        self.image2.set_colorkey(TRANS)
        
        # Font init
        self.font = pyg.font.Font("Bubble Butts.ttf", 15)
        
        #self.image.blit(self.font, (0, 0))
        self.image1.blit(self.font.render("{score1}".format(score1=score1), False, DARKGREEN), (0, 0))
        self.image2.blit(self.font.render("{score2}".format(score2=score2), False, DARKGREEN), (0, 0))
        self.oldscores = (score1, score2)
        
    def update(self):
        if self.oldscores[0] != score1:
            self.image1.fill(TRANS)
            if self.hiscore >= score1:
                self.image1.blit(self.font.render("{score1}".format(score1=score1), False, DARKGREEN), (0, 0))
            else:
                self.image1.blit(self.font.render("{score1}".format(score1=score1), False, GOLD), (0, 0))
        if self.oldscores[1] != score2:
            self.image2.fill(TRANS)
            self.image2.blit(self.font.render("{score2}".format(score2=score2), False, DARKGREEN), (0, 0))
        
        self.oldscores = (score1, score2)
        
    def draw(self, screen):
        screen.blit(self.image1, (0, 0))
        screen.blit(self.image2, (WINDOWWIDTH-10, 0))


class Program(object):
    def __init__(self):
        # Set up groups, load defaults, state
        pyg.init()
        

        self.init_mixer()
        self.font = pyg.font.Font("Bubble Butts.ttf", 5)
        
    def init_mixer(self):pass
        
    
    def handle_input(self):
    # Handle input
        
        for event in pyg.event.get():
            if event.type == QUIT:
                self.save_score()
                pyg.quit()
                sys.exit()
            
            if event.type == KEYDOWN:
                key = event.key
                if key == K_UP:
                    self.held_keys[UP] = True
                elif key == K_DOWN:
                    self.held_keys[DOWN] = True
                elif key == K_LEFT:
                    self.held_keys[LEFT] = True
                elif key == K_RIGHT:
                    self.held_keys[RIGHT] = True
                elif key == K_ESCAPE:
                    self.save_score()
                    pyg.event.post(pyg.event.Event(QUIT))
                    
                elif key == K_SPACE:
                    # Toggle ball movement
                    if not self.started:
                        self.startMessage.fill(BLACK)
                        self.screen.blit(self.startMessage, (WINDOWWIDTH/2, WINDOWHEIGHT/2))
                        self.started = True
                        
                    if self.ball.move:
                        self.ball.move = False
                    else:
                        self.ball.move = True
                        
                elif key == ord('z'):
                    self.restart()
                    
                    
            elif event.type == KEYUP:
                key = event.key
                if key == K_UP:
                    self.held_keys[UP] = False
                elif key == K_DOWN:
                    self.held_keys[DOWN] = False
                elif key == K_LEFT:
                    self.held_keys[LEFT] = False
                elif key == K_RIGHT:
                    self.held_keys[RIGHT] = False
        
        if self.held_keys[UP]:
            self.bar1.move(UP)
        elif self.held_keys[DOWN]:
            self.bar1.move(DOWN)
        elif self.held_keys[LEFT]:
            self.bar1.move(LEFT)
        elif self.held_keys[RIGHT]:
            self.bar1.move(RIGHT)

    def handle_collision(self):
        for ball, bar in pyg.sprite.groupcollide(self.balls, self.paddles, False, False).iteritems():
            #     ball, bar; assumes single bar/ball (or at least will only mind the first one)
            bar = bar[0]
            if bar.pc is '1' and ball.xspeed < 0:
                ball.bounce('x')
            elif bar.pc is '2' and ball.xspeed > 0:
                ball.bounce('x')

    
    def save_score(self):
        if self.hiscore >= score1:
            return
        self.hiscore = score1
        with file('hs', 'w') as fp:
            fp.write("{hiscore}".format(hiscore=self.hiscore))
        
    
    def restart(self):
        self.save_score()
        self.init_state()
        self.blank_screen()
        self.init_score()
        self.init_keys()
        self.init_bars()
        self.init_balls()
        
    def init_state(self):
        self.started = False
        
    def load_score(self):
        with file('hs', 'r') as fp:
            self.hiscore = int(fp.read().strip('\n'))
        print self.hiscore
        
    def init_score(self):
        
        if 'hs' in os.listdir('.') and os.path.isfile('hs'):
            self.load_score()
        else:
            print 'hs of 0'
            self.hiscore = 0
        
        global score1
        score1 = 0
        global score2
        score2 = 0
        
        self.score = Score(self.hiscore)
        
    def init_bars(self):
        self.bar1 = Bar(10, '1')
        self.bar2 = Bar(WINDOWWIDTH-20, '2')
        self.paddles = pyg.sprite.Group(self.bar1, self.bar2)
        
    def init_balls(self):
        self.ball = Ball()
        self.balls = pyg.sprite.Group(self.ball)
        
    def init_keys(self):
        self.held_keys = {UP:False,
            DOWN:False,
            LEFT:False,
            RIGHT:False}
            
    def blank_screen(self):
        self.screen.fill(BLACK)
        pyg.display.update()
    
    def main(self):
    # Main loop;
    # input, update, draw, tick
        fpsClock = pyg.time.Clock()

        self.windowSurfaceObj = pyg.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pyg.display.set_caption('Tiny Pong')
        self.screen = pyg.display.get_surface()
        
        self.started = False
        
        self.init_bars()
        
        self.init_balls()
        
        self.init_score()
        
        self.init_keys()

        while True:
            if not self.started:
                self.screen.fill(BLACK)
                self.handle_input()
                self.startMessage = pyg.Surface((WINDOWWIDTH, 5))
                self.startMessage.blit(self.font.render("PRESS SPACE TO BEGIN", False, DARKGREEN), (0, 0))
                self.screen.blit(self.startMessage, (0, WINDOWHEIGHT/2))
                pyg.display.update()
                fpsClock.tick(30)
                
            else:
                if score2 > 9:
                    self.restart()
                
                self.screen.fill(BLACK)
                
                self.handle_input()
                
                self.handle_collision()
                
                self.score.update()
                self.paddles.update(self.balls.sprites())
                self.balls.update()
                
                self.score.draw(self.screen)
                self.paddles.draw(self.screen)
                self.balls.draw(self.screen)
                
                pyg.display.update()
                fpsClock.tick(30)
                
            
if __name__ == "__main__":
    prog = Program()
    prog.main()
