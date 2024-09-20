from random import randint

import pygame
from config import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()

        #groups this class to Game class' groups
        self.game = game
        self.group = self.game.all_sprite
        self.solo_group = self.game.all_player

        # setups the player's paddle size
        self.player_width = tile_size
        self.player_height = tile_size * 3

        #setups the paddle's image and color
        self.image = pygame.Surface((self.player_width, self.player_height))
        self.image.fill(white)

        #setups the paddle's rect
        self.default_pos = (x, y)
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self): # Player class update function
        if not self.game.is_paused:
            self.movement()

    def movement(self): #Player's Control Function
        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            self.rect.y -= entity_speed
        if key[pygame.K_s]:
            self.rect.y += entity_speed

        self.rect.y = max(0, min(screen_height - self.player_height, self.rect.y))


class Ball(pygame.sprite.Sprite):
    def __init__(self, game, ball_type: str = 'main'):
        super().__init__()

        #groups this class to Game class too
        self.game = game
        self.ball_type = ball_type
        self.group = self.game.all_sprite
        self.solo_group = self.game.all_ball

        #the ball's size
        self.ball_width = tile_size
        self.ball_height = tile_size

        # the ball's image and color
        self.image = pygame.Surface((self.ball_width, self.ball_height))
        self.image.fill(white)
        self.rect = self.image.get_rect(topleft=(320, 176 + tile_size))

        # ball's starting direction when first start
        random = randint(1, 2)
        if random == 1:
            self.ball_direction = 'right'
        else:
            self.ball_direction = 'left'

        self.ball_vertical = ''
        self.ball_speedup = 0

        # ball's boolean attributes
        self.is_out = False
        self.is_ball_resets = False
        self.is_scored = False
        self.frame_count = 0
        self.countdown = 3
        self.winner = ''

        # more colors
        self.r = 1
        self.g = 1
        self.b = 1
        self.color = None

    def update(self): # Ball class update function
        if self.ball_type == 'intro':
            self.color_change()
            self.intro_movement()
        else:
            if not self.game.is_paused:
                self.movement()
                self.ball_reset()

    def color_change(self): # ball color switching effect function
        if 254 >= self.r >= 1 and self.g == 1 and self.b == 1: # r
            self.r += 1
            self.color = (self.r, self.g, self.b)
        elif self.r <= 255 and 254 >= self.g >= 1 and self.b == 1: # g
            self.r -= 1
            self.g += 1
            self.color = (self.r, self.g, self.b)
        elif self.g <= 255 and self.r == 1 and 254 >= self.b >= 1: # b
            self.g -= 1
            self.b += 1
            self.color = (self.r, self.g, self.b)
        elif self.b == 255 and self.g == 1 and 1 <= self.r <= 254: # r + b
            self.r += 1
            self.color = (self.r, self.g, self.b)
        elif self.b <= 255 and self.r == 255 and 1 <= self.g <= 254: #r + g
            self.g += 1
            self.b -= 1
            self.color = (self.r, self.g, self.b)
        elif self.g == 255 and self.r <= 255 and 1 <= self.b <= 254:  # g + b
            self.r -= 1
            self.b += 1
            self.color = (self.r, self.g, self.b)
        elif self.g == 255 and self.b == 255 and 1 <= self.r <= 254:
            self.r +=1
            self.color = (self.r, self.g, self.b)
        elif self.g <= 255 and self.b <= 255 and self.r <= 255:
            self.r -= 1
            self.g -= 1
            self.b -= 1
            self.color = (self.r, self.g, self.b)

        self.image.fill(self.color)

    def movement(self): #balls movement directions
        if not self.is_out:
            if self.ball_direction == 'left':
                self.rect.x -= ball_speed + self.ball_speedup
            elif self.ball_direction == 'right':
                self.rect.x += ball_speed + self.ball_speedup

            if self.ball_vertical == 'up':
                self.rect.y -= ball_speed + self.ball_speedup
            elif self.ball_vertical == 'down':
                self.rect.y += ball_speed + self.ball_speedup

        self.rect.x = max(0, min(screen_width - self.ball_width, self.rect.x))
        self.rect.y = max(0, min(screen_height - self.ball_height, self.rect.y))

        if self.rect.x == 0 or self.rect.x == screen_width - tile_size:
            self.is_scored = True

    def intro_movement(self): # this the function for the ball in the intro screen
        if self.ball_direction == 'left':
            self.rect.x -= 8
        elif self.ball_direction == 'right':
            self.rect.x += 8

        if self.ball_vertical == 'up':
            self.rect.y -= 8
        elif self.ball_vertical == 'down':
            self.rect.y += 8

        self.rect.x = max(0, min(screen_width - self.ball_width, self.rect.x))
        self.rect.y = max(0, min(screen_height - self.ball_height, self.rect.y))

        if self.rect.x == 0:
            self.ball_direction = 'right'
            self.ball_vertical = 'up' if randint(1, 2) == 1 else 'down'
            self.ball_vertical = self.ball_vertical if randint(1, 2) == 1 else ''

        if self.rect.x == screen_width - tile_size:
            self.ball_direction = 'left'
            self.ball_vertical = 'up' if randint(1, 2) == 1 else 'down'
            self.ball_vertical = self.ball_vertical if randint(1, 2) == 1 else ''

        if self.rect.y == 0:
            self.ball_vertical = 'down'
            self.ball_direction = 'left' if randint(1, 2) == 1 else 'right'
            self.ball_direction = self.ball_direction if randint(1, 2) == 1 else ''

        if self.rect.y == screen_height - tile_size:
            self.ball_vertical = 'up'
            self.ball_direction = 'left' if randint(1, 2) == 1 else 'right'
            self.ball_direction = self.ball_direction if randint(1, 2) == 1 else ''

    def ball_reset(self): # resets the ball when someone scores
            if self.is_ball_resets:
                self.ball_vertical = ''
                self.rect.x = 320
                self.rect.y = 176 + tile_size * 1
                self.ball_speedup = 0
                self.is_ball_resets = False

                if self.is_scored:
                    if self.ball_direction == 'right':
                        self.game.player_score += 1
                    if self.ball_direction == 'left':
                        self.game.enemy_score += 1

                    if self.game.player_score == self.game.max_score or self.game.enemy_score == self.game.max_score:
                        self.game.is_game_over = True

                    self.is_scored = False

            if self.rect.x == 0:
                self.is_out = True
                self.winner = 'Player 2'


            if self.rect.x == screen_width - tile_size:
                self.is_out = True
                self.winner = 'Player 1'



            if self.rect.y == 0:
                self.ball_vertical = 'down'

            if self.rect.y == screen_height - tile_size:
                self.ball_vertical = 'up'

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()

        #groups in game class
        self.game = game
        self.group = self.game.all_sprite
        self.solo_group = self.game.all_enemy

        #its size
        self.enemy_width = tile_size
        self.enemy_height = tile_size * 3

        #its image and color
        self.image = pygame.Surface((self.enemy_width, self.enemy_height))
        self.image.fill(white)

        #its rect/position
        self.default_pos = (x, y)
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self): # update function of enemy class
        if not self.game.is_paused:
            self.movement()

    def movement(self): # its controls
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.rect.y -= entity_speed
        if key[pygame.K_DOWN]:
            self.rect.y += entity_speed

        self.rect.y = max(0, min(screen_height - self.enemy_height, self.rect.y))
