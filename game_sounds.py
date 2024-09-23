import pygame
import os

pygame.mixer.init()

# -----------SOUND SETUP----------
sounds_dir = os.path.join(os.path.dirname(__file__), 'sounds')

ball_hit_sfx = pygame.mixer.Sound(os.path.join(sounds_dir, "retro_blip.wav"))
ball_out_sfx = pygame.mixer.Sound(os.path.join(sounds_dir, "game_over_sfx.wav"))
wall_hit_sfx = pygame.mixer.Sound(os.path.join(sounds_dir, "wall_hit_sfx.wav"))
score_sfx = pygame.mixer.Sound(os.path.join(sounds_dir, "retro-coin.wav"))
pause_sfx = pygame.mixer.Sound(os.path.join(sounds_dir, "pause_sfx.wav"))
start_sfx = pygame.mixer.Sound(os.path.join(sounds_dir, "start_btn_sfx.wav"))
final_score_sfx = pygame.mixer.Sound(os.path.join(sounds_dir, "end_sfx.wav"))
game_over = pygame.mixer.Sound(os.path.join(sounds_dir, "game_over_sfx2.wav"))
intro_bgm = pygame.mixer.Sound(os.path.join(sounds_dir, "intro_bgm.wav"))
ingame_bgm = os.path.join(os.path.dirname(__file__), 'sounds', 'ingame_bgm.wav')
counting_sfx = pygame.mixer.Sound(os.path.join(sounds_dir, 'countdown_sound.wav'))

pygame.mixer.music.load(ingame_bgm)

countdown_chn = pygame.mixer.Channel(1)
end_chn = pygame.mixer.Channel(2)
out_chn = pygame.mixer.Channel(3)

pygame.mixer.music.set_volume(0.3)


# ---------MAIN BGM SETUP--------------
def play_main_bgm(loop=-1):
    pygame.mixer.music.play(loop)


def pause_main_bgm():
    pygame.mixer.music.pause()


def resume_main_bgm():
    pygame.mixer.music.unpause()


def restart_main_bgm():
    pygame.mixer.music.stop()
    pygame.mixer.music.play()


# ---------COUNTDOWN SETUP--------------
def play_count_sfx():
    countdown_chn.play(counting_sfx)


def pause_count_sfx():
    countdown_chn.pause()


def resume_count_sfx():
    countdown_chn.unpause()


# ---------MAX SCORE SFX SETUP--------------
def play_end_sfx():
    end_chn.play(final_score_sfx)


def pause_end_sfx():
    end_chn.pause()


def resume_end_sfx():
    end_chn.unpause()


# ---------BALL OUT SFX SETUP--------------
def play_ball_out():
    out_chn.play(ball_out_sfx)


def pause_ball_out():
    out_chn.pause()


def resume_ball_out():
    out_chn.unpause()


# ---------START BUTTON SFX SETUP--------------
def play_start_sfx():
    start_sfx.play()


# sfx of ball hitting the paddles
def play_ball_impact():
    ball_hit_sfx.play()


# SFX WHEN HITTING THE EDGES OF THE WINDOW
def play_hits_wall():
    wall_hit_sfx.play()


# SFX WHEN SCORING
def play_score_sfx():
    score_sfx.play()


# PAUSE SFX
def play_pause_sfx():
    pause_sfx.play()


# ---------GAME OVER SFX SETUP--------------
def play_game_over_sfx(status=1):
    if status == 1:
        game_over.play()
    else:
        game_over.stop()


# ---------INTRO BGM SETUP--------------
def play_intro_bgm(status=1):
    loop = -1 if status == 1 else 0
    intro_bgm.set_volume(0.3)
    if status == 1:
        intro_bgm.play(loop)
    else:
        intro_bgm.stop()
