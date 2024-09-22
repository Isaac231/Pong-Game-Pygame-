import pygame
import os

pygame.mixer.init()

sounds_dir = os.path.join(os.path.dirname(__file__), 'sounds')

ball_hit_sfx = pygame.mixer.Sound(os.path.join(sounds_dir, "retro_blip.wav"))
ball_out_sfx = pygame.mixer.Sound(os.path.join(sounds_dir, "game_over_sfx.wav"))
wall_hit_sfx = pygame.mixer.Sound(os.path.join(sounds_dir, "wall_hit_sfx.wav"))
score_sfx = pygame.mixer.Sound(os.path.join(sounds_dir, "retro-coin.wav"))
counting_sfx = pygame.mixer.Sound(os.path.join(sounds_dir, "countdown_sound.wav"))
start_sfx = pygame.mixer.Sound(os.path.join(sounds_dir, "start_btn_sfx.wav"))
pause_sfx = pygame.mixer.Sound(os.path.join(sounds_dir, "pause_sfx.wav"))
final_score_sfx = pygame.mixer.Sound(os.path.join(sounds_dir, "end_sfx.wav"))
game_over = pygame.mixer.Sound(os.path.join(sounds_dir, "game_over_sfx2.wav"))
intro_bgm = pygame.mixer.Sound(os.path.join(sounds_dir, "intro_bgm.wav"))
ingame_bgm = os.path.join(os.path.dirname(__file__), 'sounds', 'ingame_bgm.wav')
pygame.mixer.music.load(ingame_bgm)
pygame.mixer.music.set_volume(0.3)


# main bgm setup
def play_main_bgm(loop=-1):
    pygame.mixer.music.play(loop)


def pause_main_bgm():
    pygame.mixer.music.pause()


def resume_main_bgm():
    pygame.mixer.music.unpause()


def restart_main_bgm():
    pygame.mixer.music.stop()
    pygame.mixer.music.play()


# sfx of ball hitting the paddles
def play_ball_impact():
    ball_hit_sfx.play()


# sfx of ball out of bounce
def play_ball_out():
    ball_out_sfx.set_volume(1.0)
    ball_out_sfx.play()


# sfx of ball hitting the edges of the screen
def play_hits_wall():
    wall_hit_sfx.play()


def play_score_sfx():
    score_sfx.play()


def play_count_sfx():
    counting_sfx.play()


def play_start_sfx():
    start_sfx.play()


def play_pause_sfx():
    pause_sfx.play()


def play_end_sfx():
    final_score_sfx.play()


def play_game_over_sfx():
    game_over.play()


# intro bgm setup
def play_intro_bgm(status=1):
    loop = -1 if status == 1 else 0
    intro_bgm.set_volume(0.3)
    if status == 1:
        intro_bgm.play(loop)
    elif status == 2:
        intro_bgm.stop()
