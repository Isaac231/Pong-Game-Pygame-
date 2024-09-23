#YES I KNOW MY CODE IS MESSY, SPECIALLY THE HARDCODED X, Y ARGUMENTS AND SUCH. TOO LAZY TO FIX THEM NOW HIHI

import pygame
from config import *
import sys
from game_sounds import play_ball_impact, play_ball_out, play_intro_bgm, play_main_bgm, pause_main_bgm, resume_main_bgm, \
    restart_main_bgm, play_score_sfx, play_count_sfx, play_pause_sfx, play_start_sfx, play_end_sfx, play_game_over_sfx, \
    resume_count_sfx, pause_count_sfx, pause_ball_out, pause_end_sfx, resume_end_sfx, resume_ball_out

from sprites import Player, Ball, Enemy

pygame.init()


class Game:
    def __init__(self):
        # ----------SCREEN/FPS SETUP----------
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Pong Game")
        self.frame_rate = pygame.time.Clock()

        # ----------FONT SETUP----------
        self.font_face1 = 'font/Blox2.ttf'
        self.font_face2 = 'font/joystix monospace.otf'

        self.font1 = pygame.font.Font(self.font_face2, 150)
        self.font2 = pygame.font.Font(self.font_face2, 40)
        self.font3 = pygame.font.Font(self.font_face2, 80)
        self.font4 = pygame.font.Font(self.font_face2, 15)
        self.font5 = pygame.font.Font(self.font_face2, 25)

        # ----------BOOLEANS----------
        self.running = False
        self.sound_played = False
        self.count_played = False
        self.bgm_playing = False
        self.game_over_played = False
        self.scored = False
        self.is_paused = False
        self.is_intro = True
        self.is_start_pressed = False
        self.is_game_over = False
        self.ball_collided = False
        self.winner_txt = None

        # ----------COUNTERS----------
        self.collision_counter = 0
        self.counter1 = 0
        self.counter2 = 0
        self.counter3 = 0
        self.y_hover = 0
        self.x_hover = 0
        self.font_size = 15
        self.player_score = 0
        self.enemy_score = 0
        self.max_score = 10

        # ----------SPRITES SETUP----------
        self.all_sprite = pygame.sprite.Group()
        self.all_player = pygame.sprite.GroupSingle()
        self.all_enemy = pygame.sprite.GroupSingle()
        self.all_ball = pygame.sprite.GroupSingle()
        self.all_intro_ball = pygame.sprite.GroupSingle()

        # CREATE INSTANCES
        self.player = Player(self, 64, 176, )
        self.ball = Ball(self)
        self.intro_ball = Ball(self, 'intro')
        self.enemy = Enemy(self, 544, 176)

        # ADD TO SPRITES GROUP
        self.all_sprite.add(self.player, self.ball, self.enemy)
        self.all_player.add(self.player)
        self.all_ball.add(self.ball)
        self.all_intro_ball.add(self.intro_ball)
        self.all_enemy.add(self.enemy)

    # -----------EVENTS SETUP----------
    def event(self):
        # CHECKS IF THE PLAYER PRESSED THE EXIT ON THE WINDOW
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.is_intro = False

            # TRIGGERS BLINK EFFECT OF THE START BUTTON IN THE INTRO SCREEN
            if self.is_intro:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.is_start_pressed = True
                        self.counter2 = 0

            # PAUSES THE GAME AND SOME OTHER SOUNDS
            if event.type == pygame.KEYDOWN and not self.is_game_over:
                if event.key == pygame.K_SPACE:
                    self.is_paused = not self.is_paused
                    if self.is_paused:
                        play_pause_sfx()
                        pause_main_bgm()

                        if self.ball.is_out:
                            pause_count_sfx()

                            if self.player_score != self.max_score and self.enemy_score != self.max_score:
                                pause_ball_out()
                            else:
                                pause_end_sfx()

                    elif not self.is_paused:
                        if not self.ball.is_out:
                            resume_main_bgm()
                        else:
                            resume_count_sfx()

                            if self.player_score != self.max_score and self.enemy_score != self.max_score:
                                resume_ball_out()
                            else:
                                resume_end_sfx()

    # -----------UPDATE SPRITES AND OTHERS----------
    def update(self):
        # UPDATE ALL SPRITES
        self.all_sprite.update()

        # COUNTER OF COUNTDOWN SEQUENCE
        if self.ball.is_out and not self.is_paused:  # ball timer when out of bounce
            if not self.count_played:
                pause_main_bgm()
                if self.player_score != self.max_score - 1 and self.enemy_score != self.max_score - 1:
                    play_count_sfx()
                self.count_played = True

            self.ball.frame_count += 1
            if self.ball.frame_count >= 60:
                self.ball.countdown -= 1
                self.ball.frame_count = 0
                if self.ball.countdown == 0:
                    self.ball.countdown = 3
                    self.ball.is_ball_resets = True
                    self.ball.is_out = False
                    self.sound_played = False

        # CHECKS FOR COLLISIONS IF NOT PAUSED
        if not self.is_paused:
            self.if_collided()

    # -----------DRAW SPRITES, TEXT AND OTHERS----------
    def draw(self):  # game loop draw function
        # DRAW SCREEN
        self.screen.fill(black)

        # DRAW A LINE IN THE MIDDLE OF THE WINDOW
        divider_line = pygame.Surface((5, 480))
        divider_line.fill(white)
        divider_rect = divider_line.get_rect(midtop=(320, 0))
        self.screen.blit(divider_line, divider_rect)

        # INCREMENTS SCORE AND DISPLAYS WINNER AND COUNTDOWN TEXT
        if self.ball.is_out:
            if self.player_score != self.max_score and self.enemy_score != self.max_score:
                if self.ball.ball_direction == 'right' and not self.scored:
                    self.player_score += 1
                    play_score_sfx()
                    self.scored = True
                if self.ball.ball_direction == 'left' and not self.scored:
                    self.enemy_score += 1
                    play_score_sfx()
                    self.scored = True

            if not self.sound_played:
                if self.player_score != self.max_score and self.enemy_score != self.max_score:
                    play_ball_out()
                else:
                    play_end_sfx()

                self.sound_played = True

            if self.player_score != self.max_score and self.enemy_score != self.max_score:
                self.winner_txt = self.font2.render(f"{self.ball.winner} scores!", True, white, pygame.SRCALPHA)
                countdown_txt = self.font3.render(f"{self.ball.countdown}", True, white, pygame.SRCALPHA)

                self.screen.blit(self.winner_txt, (320 - (tile_size * 8) + 5, 176 - (tile_size + 10)))
                self.screen.blit(countdown_txt, (320 - tile_size, 176 + tile_size))

        # DRAW ALL SPRITES
        self.all_sprite.draw(self.screen)

        # DRAW PAUSE TEXT WHEN PAUSED
        self.game_paused()

        # DRAW SCORE BOARD TEXT
        self.score_board()

        # REDRAW THE WHOLE SCREEN
        pygame.display.update()

    # -----------COLLISION SETUP----------
    def if_collided(self):

        # CHECKS IF THE BALL HITS THE TOP/BOTTOM PART OF THE PADDLE IF TRUE BALL MOVES DIAGONALLY
        def check_diagonally(ball, paddle):
            # CREATE THREE SECTION FOR THE PADDLE (TOP, CENTER, BOTTOM)
            paddle_top = pygame.Rect(paddle.rect.x, paddle.rect.y, tile_size, tile_size)
            paddle_center = pygame.Rect(paddle.rect.x, paddle.rect.y + tile_size, tile_size, tile_size)
            paddle_bottom = pygame.Rect(paddle.rect.x, paddle.rect.y + tile_size * 2, tile_size, tile_size)

            # USE CLIP METHOD TO CHECKS OVERLAYS
            top = paddle_top.clip(ball.rect)
            center = paddle_center.clip(ball.rect)
            bottom = paddle_bottom.clip(ball.rect)

            # CALCULATE THE AREA OF THE CLIPPED RECT
            top_area = top.width * top.height
            center_area = center.width * center.height
            bottom_area = bottom.width * bottom.height

            # COMPARE BOTH CLIPPED RECT TO SEE WHICH IS BIGGER
            # THIS IS SO THAT IF THE BALL HITS TWO SECTION OF THE PADDLE
            # IT WILL CHECK WHICH SECTION HAS THE LARGER OVERLAY AND PICKS IT
            if top_area > center_area and top_area > bottom_area:
                return 'up'
            elif bottom_area > center_area and bottom_area > top_area:
                return 'down'
            else:
                return ''

        #CHECKS IF BALL COLLIDES WITH PLAYER PADDLE
        if pygame.sprite.spritecollide(self.ball, self.all_player, False):
            # ADDS COLLISION COUNTER TO PREVENT MULTIPLE EXECUTION
            if self.collision_counter == 0:
                self.ball_collided = True
                play_ball_impact() #PLAY SFX

                self.ball.ball_vertical = check_diagonally(self.ball, self.player)  # CHECK IF DIAGONAL

                self.ball.ball_direction = 'right'
                if 0 <= self.ball.ball_speedup <= 25:
                    self.ball.ball_speedup += 0.5  # GRADUALLY INCREASE THE BALL SPEED

                self.collision_counter = 1
        else:
            if self.ball_collided:
                self.ball_collided = False

            if self.collision_counter > 0:
                self.collision_counter += 1

            if self.collision_counter > 0 and self.collision_counter >= 30:
                self.collision_counter = 0

        #SAME SETUP FOR ENEMY PADDLE
        if pygame.sprite.spritecollide(self.ball, self.all_enemy, False):  # checks if collided for enemy
            if self.collision_counter == 0:
                self.ball_collided = True
                play_ball_impact()  # play ball collide sfx

                self.ball.ball_vertical = check_diagonally(self.ball, self.enemy)

                self.ball.ball_direction = 'left'
                if 0 <= self.ball.ball_speedup <= 25:
                    self.ball.ball_speedup += 0.5

                self.collision_counter = 1

        else:
            if self.ball_collided:
                self.ball_collided = False

            if self.collision_counter > 0:
                self.collision_counter += 1

            if self.collision_counter > 0 and self.collision_counter >= 30:
                self.collision_counter = 0

    # -----------SCORE BOARD SETUP----------
    def score_board(self):
        player_scoreboard = self.font2.render(f"{self.player_score}", True, white)
        self.screen.blit(player_scoreboard, (tile_size + (tile_size * 4), tile_size))

        enemy_scoreboard = self.font2.render(f"{self.enemy_score}", True, white)
        self.screen.blit(enemy_scoreboard, (screen_width - (tile_size * 6), tile_size))


    # -----------INTRO SCREEN SETUP----------
    def intro_update(self):
        self.all_intro_ball.update()

    def intro_draw(self):
        self.screen.fill(black)

        if self.is_intro:
            if not self.bgm_playing:
                play_intro_bgm()
                self.bgm_playing = True

        self.font4 = pygame.font.Font(self.font_face2, int(self.font_size))
        title_txt = self.font1.render(f"Pong", True, self.get_frame_counts(1))
        start_txt = self.font4.render(f"click anywhere to start", True, self.get_frame_counts(2))

        self.screen.blit(title_txt, ((screen_width // 2 - title_txt.get_width() // 2), 176 - (tile_size * 5)))
        self.screen.blit(start_txt, ((screen_width // 2 - start_txt.get_width() // 2) - self.x_hover,
                                     176 + (tile_size * 3) - self.y_hover))

        self.frame_counters(1)

        self.all_intro_ball.draw(self.screen)
        pygame.display.update()

    #ALL COUNTER GETTER
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
                if not self.sound_played:
                    play_start_sfx()
                    self.sound_played = True

                if 0 <= self.counter2 <= 5:  # start button blink effect
                    color = white
                elif 6 <= self.counter2 <= 10:
                    color = black

                if self.counter3 >= 90:
                    self.is_intro = False
                    self.bgm_playing = False
                    self.sound_played = False
                    play_intro_bgm(2)
                    self.running = True
        elif section == 3:
            if self.counter2 <= 30:  # paused blink effect
                if 0 <= self.counter3 <= 5:
                    color = white
                elif 6 <= self.counter3 <= 10:
                    color = transparent

        return color

    #ALL COUNTER CHECKER
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

    def game_paused(self):
        if self.is_paused:
            paused_txt = self.font4.render("PAUSED", True, self.get_frame_counts(3), pygame.SRCALPHA)
            self.screen.blit(paused_txt, (320 - tile_size, 176 - tile_size * 5))

            self.frame_counters(2)

        else:
            self.counter2 = 0
            self.counter3 = 0

    # -----------BUTTON SETUP----------
    def yes_button(self, text, x, y, width, height):
        mouse_pos = pygame.mouse.get_pos() #GET CURRENT MOUSE POSITION
        click = pygame.mouse.get_pressed() #CHECK IF MOUSE CLICKS

        #DRAW INVISIBLE RECT
        button_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(button_surface, transparent, button_surface.get_rect())

        #CHECKS IF MOUSE LEFT CLICK AND HOVER EFFECT
        if button_rect.collidepoint(mouse_pos):
            self.font_size = 30
            if click[0] == 1:
                return True

        else:
            self.font_size = 25

        font = pygame.font.Font(self.font_face2, self.font_size)

        yes_txt = font.render(text, True, white)

        #DRAWS THE TEXT IN THE CENTER OF THE INVISIBLE RECT
        self.screen.blit(yes_txt,
                         (x + (width // 2 - yes_txt.get_width() // 2), y + (height // 2 - yes_txt.get_height() // 2)))

        #RETURN FALSE IF NO LEFT CLICKS
        return False

    #SAME SETUP
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

    # -----------GAME OVER SETUP----------
    def game_over(self):
        self.screen.fill(black)

        if not self.game_over_played:
            play_game_over_sfx()
            self.game_over_played = True

        # -----------TEXT SETUP----------
        self.ball.winner = "Player 1" if self.player_score == self.max_score else "Player 2"
        game_over_txt = self.font3.render("Game Over", True, self.get_frame_counts(1))
        self.winner_txt = self.font5.render(f"{self.ball.winner} won the game!", True, white)
        final_score_txt = self.font5.render(f"{self.player_score} - {self.enemy_score}", True, white)
        replay_txt = self.font5.render("Play again?", True, white)

        self.screen.blit(game_over_txt, (320 - tile_size * 9 - 10, 176 - tile_size * 5))
        self.screen.blit(self.winner_txt, (320 - tile_size * 7, 176 - tile_size * 2))
        self.screen.blit(final_score_txt, (320 - tile_size * 2, 176 - tile_size))
        self.screen.blit(replay_txt, (320 - tile_size * 3.5, 176 + tile_size * 2))

        # -----------CHECK FOR BUTTONS SETUP----------
        if self.yes_button("Yes", 320 - tile_size * 1.5, 176 + tile_size * 3, 80, 45):
            self.player_score, self.enemy_score = 0, 0
            self.ball.ball_speedup = 0
            self.player.rect.topleft = self.player.default_pos
            self.enemy.rect.topleft = self.enemy.default_pos
            self.is_game_over = False
            self.game_over_played = False
            play_game_over_sfx(2)
            play_score_sfx()
            restart_main_bgm()

        if self.no_button("No", 320 - tile_size * 1.2, 176 + tile_size * 5, 60, 45):
            play_ball_out()
            self.running = False
            pygame.time.delay(1000)

        self.frame_counters(1)
        pygame.display.update()

    #MAIN LOOP RUNNER
    def main(self):
        if self.running and not self.is_paused and not self.is_game_over:
            if not self.bgm_playing:
                play_main_bgm()
                self.bgm_playing = True
        self.event()
        if not self.is_game_over:
            self.update()
            self.draw()
        self.frame_rate.tick(FPS)

#RUNNER
if __name__ == '__main__':
    run = Game()
    run.intro_screen()
    while run.running:
        run.main()
        if run.is_game_over:
            run.game_over()

pygame.quit()
sys.exit()
