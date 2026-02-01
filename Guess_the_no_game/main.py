import os
import pygame
import random
import sys
import time

# ---------------- PATH SETUP ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------- PYGAME INIT ----------------
pygame.init()
pygame.mixer.init()

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 750, 520
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Guess The Number - Multiplayer")

# ---------------- COLORS ----------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 120, 220)
GREEN = (0, 180, 0)
RED = (200, 0, 0)
GRAY = (240, 240, 240)

# ---------------- FONTS ----------------
font = pygame.font.SysFont("arial", 26)
big_font = pygame.font.SysFont("arial", 42)

# ---------------- SOUND LOADER ----------------
def load_sound(name):
    path = os.path.join(BASE_DIR, name)
    return pygame.mixer.Sound(path) if os.path.exists(path) else None

correct_sound = load_sound("correct.wav")
wrong_sound   = load_sound("wrong.wav")
click_sound   = load_sound("click.wav")

# ---------------- CLOCK ----------------
clock = pygame.time.Clock()

# ---------------- GAME VARIABLES ----------------
mode = None          # "CPU" or "PVP"
turn = 1
secret_number = 0
attempts = 0
max_attempts = 7
user_input = ""
message = ""
start_time = 0
winner = None

# ---------------- FUNCTIONS ----------------
def draw_button(text, x, y, w, h):
    pygame.draw.rect(screen, BLUE, (x, y, w, h), border_radius=12)
    txt = font.render(text, True, WHITE)
    screen.blit(txt, (x + w//2 - txt.get_width()//2, y + 12))
    return pygame.Rect(x, y, w, h)

def reset_game():
    global secret_number, attempts, user_input, message, start_time, winner
    secret_number = random.randint(1, 100)
    attempts = 0
    user_input = ""
    message = "Guess a number (1–100)"
    start_time = time.time()
    winner = None

# ---------------- MAIN LOOP ----------------
running = True
while running:
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ---------- KEYBOARD INPUT ----------
        if event.type == pygame.KEYDOWN and mode:
            if event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]

            elif event.key == pygame.K_RETURN and user_input and not winner:
                guess = int(user_input)
                attempts += 1

                if guess == secret_number:
                    if correct_sound:
                        correct_sound.play()
                    winner = f"Player {turn}" if mode == "PVP" else "You"
                    message = f"🎉 {winner} Wins!"

                elif guess < secret_number:
                    if wrong_sound:
                        wrong_sound.play()
                    message = "🔽 Too Low!"

                else:
                    if wrong_sound:
                        wrong_sound.play()
                    message = "🔼 Too High!"

                if attempts >= max_attempts and not winner:
                    if mode == "CPU":
                        message = f"❌ You Lost! Number was {secret_number}"
                    else:
                        turn = 2 if turn == 1 else 1
                        reset_game()
                        message = f"Player {turn}'s Turn"

                user_input = ""

            elif event.unicode.isdigit() and not winner:
                user_input += event.unicode

        # ---------- MOUSE INPUT ----------
        if event.type == pygame.MOUSEBUTTONDOWN:
            if click_sound:
                click_sound.play()

            if not mode:
                if cpu_btn.collidepoint(event.pos):
                    mode = "CPU"
                    reset_game()

                if pvp_btn.collidepoint(event.pos):
                    mode = "PVP"
                    turn = 1
                    reset_game()

            else:
                if restart_btn.collidepoint(event.pos):
                    mode = None
                    user_input = ""
                    message = ""

    # ---------------- UI ----------------
    title = big_font.render("Guess The Number", True, BLACK)
    screen.blit(title, (200, 30))

    if not mode:
        cpu_btn = draw_button("Player vs Computer", 250, 200, 260, 60)
        pvp_btn = draw_button("2 Players (PVP)", 250, 280, 260, 60)

    else:
        timer = int(time.time() - start_time)
        info = font.render(
            f"Attempts: {attempts}/{max_attempts}   Time: {timer}s",
            True, BLACK
        )
        screen.blit(info, (220, 120))

        if mode == "PVP":
            turn_text = font.render(f"Player {turn}'s Turn", True, BLUE)
            screen.blit(turn_text, (300, 160))

        input_text = font.render(f"Your Guess: {user_input}", True, BLACK)
        screen.blit(input_text, (260, 200))

        msg_color = GREEN if winner else RED
        msg = font.render(message, True, msg_color)
        screen.blit(msg, (200, 240))

        restart_btn = draw_button("Restart", 315, 320, 120, 50)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
