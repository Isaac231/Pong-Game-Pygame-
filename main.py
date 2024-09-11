import pygame
from config import *
import sys

from sprites import Player, Ball, Enemy

pygame.init()


class Game:
    def __init__(self):

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Pong Game")
        self.frame_rate = pygame.time.Clock()

        self.font_face1 = 'font/Blox2.ttf'
        self.font_face2 = 'font/joystix monospace.otf'

        self.font1 = pygame.font.Font(self.font_face2, 150)
        self.font2 = pygame.font.Font(self.font_face2, 40)
        self.font3 = pygame.font.Font(self.font_face2, 80)
        self.font4 = pygame.font.Font(self.font_face2, 15)

        self.running = False
        self.is_paused = False
        self.is_intro = True
        self.is_start_pressed = False
        self.color = white
        self.color2 = white
        self.title_txt = None
        self.start_txt = None
        self.winner_txt = None
        self.countdown_txt = None
        self.paused_txt = None
        self.player_scoreboard = None
        self.enemy_scoreboard = None
        self.counter1 = 0
        self.counter2 = 0
        self.counter3 = 0
        self.y_hover = 0
        self.x_hover = 0
        self.font_size = 15
        self.player_score = 0
        self.enemy_score = 0

        self.all_sprite = pygame.sprite.Group()
        self.all_player = pygame.sprite.GroupSingle()
        self.all_enemy = pygame.sprite.GroupSingle()
        self.all_ball = pygame.sprite.GroupSingle()
        self.all_intro_ball = pygame.sprite.GroupSingle()

        self.player = Player(self, 64, 176, )

        self.ball = Ball(self)
        self.intro_ball = Ball(self, 'intro')

        self.enemy = Enemy(self, 544, 176)

        self.all_sprite.add(self.player, self.ball, self.enemy)
        self.all_player.add(self.player)
        self.all_ball.add(self.ball)
        self.all_intro_ball.add(self.intro_ball)
        self.all_enemy.add(self.enemy)

    def event(self):  # game loop event function
        for event in pygame.event.get():  # checks if quit button is pressed
            if event.type == pygame.QUIT:
                self.running = False
                self.is_intro = False

            if self.is_intro:  # starts the intro button blinking effect
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.is_start_pressed = True
                        self.counter2 = 0

            if event.type == pygame.KEYDOWN:  # pauses the game
                if event.key == pygame.K_SPACE:
                    self.is_paused = not self.is_paused

    def update(self):  # game loop draw function
        self.all_sprite.update()

        if self.ball.is_out and not self.is_paused:  # ball timer when out of bounce
            self.ball.frame_count += 1
            if self.ball.frame_count >= 60:
                self.ball.countdown -= 1
                self.ball.frame_count = 0
                if self.ball.countdown == 0:
                    self.ball.countdown = 3
                    self.ball.is_ball_resets = True
                    self.ball.is_out = False

        if not self.is_paused:
            self.if_collided()

    def draw(self):  # game loop draw function
        self.screen.fill(black)
        self.all_sprite.draw(self.screen)

        if self.ball.is_out:
            self.winner_txt = self.font2.render(f"{self.ball.winner} scores!", True, white)
            self.countdown_txt = self.font1.render(f"{self.ball.countdown}", True, white)

            self.screen.blit(self.winner_txt, (320 - (tile_size * 8), 176 - (tile_size * 2)))
            self.screen.blit(self.countdown_txt, (320 - (tile_size * 2), 176 - tile_size))

        self.game_paused()
        self.score_board()

        pygame.display.update()

    def if_collided(self):  # collision detection function

        def check_diagonally(ball, rect):  # checks if the ball hits the top/bottom corner for diagonal movement
            if ball.rect.colliderect(rect.rect) and (rect.rect.y + tile_size) <= ball.rect.y <= (
                    rect.rect.y + tile_size * 2):
                return ''
            elif ball.rect.colliderect(rect.rect) and rect.rect.y - tile_size <= ball.rect.y <= (
                    rect.rect.y):
                return 'up'
            elif ball.rect.colliderect(rect.rect) and (rect.rect.y + tile_size * 2) <= ball.rect.y <= (
                    rect.rect.y + tile_size * 3):
                return 'down'

        if pygame.sprite.spritecollide(self.ball, self.all_player, False):  # checks if collided for player
            self.ball.ball_vertical = check_diagonally(self.ball, self.player)

            self.ball.ball_direction = 'right'
            if 0 <= self.ball.ball_speedup <= 32:
                self.ball.ball_speedup += 0.5

        if pygame.sprite.spritecollide(self.ball, self.all_enemy, False):  # checks if collided for enemy
            self.ball.ball_vertical = check_diagonally(self.ball, self.enemy)

            self.ball.ball_direction = 'left'
            if 0 <= self.ball.ball_speedup <= 32:
                self.ball.ball_speedup += 0.5

    def score_board(self):  # game's scoring system
        self.player_scoreboard = self.font2.render(f"{self.player_score}", True, white)
        self.screen.blit(self.player_scoreboard, (tile_size + (tile_size * 4), tile_size))

        self.enemy_scoreboard = self.font2.render(f"{self.enemy_score}", True, white)
        self.screen.blit(self.enemy_scoreboard, (screen_width - (tile_size * 6), tile_size))

    def intro_update(self):  # intro screen update function
        self.all_intro_ball.update()

    def intro_draw(self):  # intro screen draw function
        self.screen.fill(black)

        if 0 <= self.counter1 <= 120:  # title's blinking effect
            self.color = white
        elif 121 <= self.counter1 <= 150:
            self.color = black

        if not self.is_start_pressed:  # start button hovering and blinking effect
            if 1 <= self.counter2 <= 60:
                self.y_hover += 0.05
                self.font_size += 0.015
                self.x_hover += 0.02
            elif 61 <= self.counter2 <= 120:
                self.y_hover -= 0.05
                self.font_size -= 0.015
                self.x_hover -= 0.02
        else:
            if 0 <= self.counter2 <= 5:
                self.color2 = white
            elif 6 <= self.counter2 <= 10:
                self.color2 = black

            if self.counter3 >= 90:
                self.is_intro = False
                self.running = True

        self.font4 = pygame.font.Font(self.font_face2, int(self.font_size))
        self.title_txt = self.font1.render(f"Pong", True, self.color)
        self.start_txt = self.font4.render(f"click anywhere to start", True, self.color2)

        self.screen.blit(self.title_txt, (320 - (tile_size * 8), 176 - (tile_size * 5)))
        self.screen.blit(self.start_txt, (320 - (tile_size * 4 + 15) - self.x_hover,
                                          176 + (tile_size * 3) - self.y_hover))

        if not self.is_start_pressed:  # counter loops
            if self.counter2 <= 120:
                self.counter2 += 1
            else:
                self.counter2 = 0
        else:
            if self.counter2 <= 10:
                self.counter2 += 1
            else:
                self.counter2 = 0
            if self.counter3 <= 90:
                self.counter3 += 1
            else:
                self.counter3 = 0

        if self.counter1 <= 150:
            self.counter1 += 1
        else:
            self.counter1 = 0

        self.all_intro_ball.draw(self.screen)
        pygame.display.update()

    def intro_screen(self):  # intro screen runner
        while self.is_intro:
            self.event()
            self.intro_update()
            self.intro_draw()
            self.frame_rate.tick(FPS)

    def game_paused(self):  # adds a paused indicator on top when paused
        if self.is_paused:
            if self.counter2 <= 30:
                if 0 <= self.counter3 <= 5:
                    self.color = white
                elif 6 <= self.counter3 <= 10:
                    self.color = black

            self.paused_txt = self.font4.render("PAUSED", True, self.color)
            self.screen.blit(self.paused_txt, (320 - tile_size, 176 - tile_size * 5))

            if self.counter3 <= 10:
                self.counter3 += 1
            else:
                self.counter3 = 0

            if self.counter2 <= 30:
                self.counter2 += 1
            else:
                self.color = white
        else:
            self.counter2 = 0
            self.counter3 = 0

    def main(self):  # game loop runner
        self.event()
        self.update()
        self.draw()
        self.frame_rate.tick(FPS)


if __name__ == '__main__':
    run = Game()
    run.intro_screen()
    while run.running:
        run.main()

pygame.quit()
sys.exit()
