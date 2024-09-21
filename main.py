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
        self.font5 = pygame.font.Font(self.font_face2, 25)

        self.running = False
        self.is_paused = False
        self.is_intro = True
        self.is_start_pressed = False
        self.is_game_over = False
        self.ball_collided = False
        self.winner_txt = None
        self.counter1 = 0
        self.counter2 = 0
        self.counter3 = 0
        self.y_hover = 0
        self.x_hover = 0
        self.font_size = 15
        self.player_score = 0
        self.enemy_score = 0
        self.max_score = 10

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

            if event.type == pygame.KEYDOWN and not self.is_game_over:  # pauses the game
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
            countdown_txt = self.font1.render(f"{self.ball.countdown}", True, white)

            self.screen.blit(self.winner_txt, (320 - (tile_size * 8), 176 - (tile_size * 2)))
            self.screen.blit(countdown_txt, (320 - (tile_size * 2), 176 - tile_size))

        self.game_paused()
        self.score_board()

        pygame.display.update()

    def if_collided(self):  # collision detection function

        def check_diagonally(ball, paddle):  # checks if the ball hits the top/bottom corner for diagonal movement
            # create a three section for the paddle (top, center, and bottom)
            paddle_top = pygame.Rect(paddle.rect.x, paddle.rect.y, tile_size, tile_size)
            paddle_center = pygame.Rect(paddle.rect.x, paddle.rect.y + tile_size, tile_size, tile_size)
            paddle_bottom = pygame.Rect(paddle.rect.x, paddle.rect.y + tile_size * 2, tile_size, tile_size)

            # get the clipped rect
            top = paddle_top.clip(ball.rect)
            center = paddle_center.clip(ball.rect)
            bottom = paddle_bottom.clip(ball.rect)

            # calculate the area of the clipped rect
            top_area = top.width * top.height
            center_area = center.width * center.height
            bottom_area = bottom.width * bottom.height

            if top_area > center_area and top_area > bottom_area:
                return 'up'
            elif bottom_area > center_area and bottom_area > top_area:
                return 'down'
            else:
                return ''

        if pygame.sprite.spritecollide(self.ball, self.all_player, False):  # checks if collided for player
            if not self.ball_collided:
                self.ball.ball_vertical = check_diagonally(self.ball, self.player)

                self.ball.ball_direction = 'right'
                if 0 <= self.ball.ball_speedup <= 32:
                    self.ball.ball_speedup += 0.5

                self.ball_collided = True
        else:
            self.ball_collided = False

        if pygame.sprite.spritecollide(self.ball, self.all_enemy, False):  # checks if collided for enemy
            if not self.ball_collided:
                self.ball.ball_vertical = check_diagonally(self.ball, self.enemy)

                self.ball.ball_direction = 'left'
                if 0 <= self.ball.ball_speedup <= 32:
                    self.ball.ball_speedup += 0.5
                self.ball_collided = True
        else:
            self.ball_collided = False

    def score_board(self):  # game's scoring system
        player_scoreboard = self.font2.render(f"{self.player_score}", True, white)
        self.screen.blit(player_scoreboard, (tile_size + (tile_size * 4), tile_size))

        enemy_scoreboard = self.font2.render(f"{self.enemy_score}", True, white)
        self.screen.blit(enemy_scoreboard, (screen_width - (tile_size * 6), tile_size))

    def intro_update(self):  # intro screen update function
        self.all_intro_ball.update()

    def intro_draw(self):  # intro screen draw function
        self.screen.fill(black)

        self.font4 = pygame.font.Font(self.font_face2, int(self.font_size))
        title_txt = self.font1.render(f"Pong", True, self.get_frame_counts(1))
        start_txt = self.font4.render(f"click anywhere to start", True, self.get_frame_counts(2))

        self.screen.blit(title_txt, ((screen_width // 2 - title_txt.get_width() // 2), 176 - (tile_size * 5)))
        self.screen.blit(start_txt, ((screen_width // 2 - start_txt.get_width() // 2) - self.x_hover,
                                     176 + (tile_size * 3) - self.y_hover))

        self.frame_counters(1)

        self.all_intro_ball.draw(self.screen)
        pygame.display.update()

    def get_frame_counts(self, section):
        color = white
        if section == 1:
            if 0 <= self.counter1 <= 120:  # title's blinking effect
                color = white
            elif 121 <= self.counter1 <= 150:
                color = black
        elif section == 2:
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
                if 0 <= self.counter2 <= 5:  # start button blink effect
                    color = white
                elif 6 <= self.counter2 <= 10:
                    color = black

                if self.counter3 >= 90:
                    self.is_intro = False
                    self.running = True
        elif section == 3:
            if self.counter2 <= 30:  # paused blink effect
                if 0 <= self.counter3 <= 5:
                    color = white
                elif 6 <= self.counter3 <= 10:
                    color = black

        return color

    def frame_counters(self, section):
        if section == 1:  # intro_draw function
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
        elif section == 2:  # game_paused function
            if self.counter3 <= 10:
                self.counter3 += 1
            else:
                self.counter3 = 0

            if self.counter2 <= 30:
                self.counter2 += 1

    def intro_screen(self):  # intro screen runner
        while self.is_intro:
            self.event()
            self.intro_update()
            self.intro_draw()
            self.frame_rate.tick(FPS)

    def game_paused(self):  # adds a paused indicator on top when paused
        if self.is_paused:
            paused_txt = self.font4.render("PAUSED", True, self.get_frame_counts(3))
            self.screen.blit(paused_txt, (320 - tile_size, 176 - tile_size * 5))

            self.frame_counters(2)

        else:
            self.counter2 = 0
            self.counter3 = 0

    def yes_button(self, text, x, y, width, height):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        button_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(button_surface, transparent, button_surface.get_rect())

        if button_rect.collidepoint(mouse_pos):
            self.font_size = 30
            if click[0] == 1:
                return True

        else:
            self.font_size = 25

        font = pygame.font.Font(self.font_face2, self.font_size)

        yes_txt = font.render(text, True, white)
        self.screen.blit(yes_txt,
                         (x + (width // 2 - yes_txt.get_width() // 2), y + (height // 2 - yes_txt.get_height() // 2)))

        return False

    def no_button(self, text, x, y, width, height):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        button_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(button_surface, transparent, button_surface.get_rect())

        if button_rect.collidepoint(mouse_pos):
            self.font_size = 30
            if click[0] == 1:
                return True

        else:
            self.font_size = 25

        font = pygame.font.Font(self.font_face2, self.font_size)

        yes_txt = font.render(text, True, white)
        self.screen.blit(yes_txt,
                         (x + (width // 2 - yes_txt.get_width() // 2), y + (height // 2 - yes_txt.get_height() // 2)))

        return False

    def game_over(self):
        self.screen.fill(black)

        self.ball.winner = "Player 1" if self.player_score == self.max_score else "Player 2"
        game_over_txt = self.font3.render("Game Over", True, self.get_frame_counts(1))
        self.winner_txt = self.font5.render(f"{self.ball.winner} won the game!", True, white)
        final_score_txt = self.font5.render(f"{self.player_score} - {self.enemy_score}", True, white)
        replay_txt = self.font5.render("Play again?", True, white)

        self.screen.blit(game_over_txt, (320 - tile_size * 9 - 10, 176 - tile_size * 5))
        self.screen.blit(self.winner_txt, (320 - tile_size * 7, 176 - tile_size * 2))
        self.screen.blit(final_score_txt, (320 - tile_size * 2, 176 - tile_size))
        self.screen.blit(replay_txt, (320 - tile_size * 3.5, 176 + tile_size * 2))

        if self.yes_button("Yes", 320 - tile_size * 1.5, 176 + tile_size * 3, 80, 45):
            self.player_score, self.enemy_score = 0, 0
            self.ball.ball_speedup = 0
            self.player.rect.topleft = self.player.default_pos
            self.enemy.rect.topleft = self.enemy.default_pos
            self.is_game_over = False

        if self.no_button("No", 320 - tile_size * 1.2, 176 + tile_size * 5, 60, 45):
            self.running = False

        self.frame_counters(1)
        pygame.display.update()

    def main(self):  # game loop runner
        self.event()
        if not self.is_game_over:
            self.update()
            self.draw()
        self.frame_rate.tick(FPS)


if __name__ == '__main__':
    run = Game()
    run.intro_screen()
    while run.running:
        run.main()
        if run.is_game_over:
            run.game_over()

pygame.quit()
sys.exit()
