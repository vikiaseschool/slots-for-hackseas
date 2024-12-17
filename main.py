import pygame
import sys
import random
import functions

pygame.init()
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h

window_width = screen_width
window_height = screen_height - 50
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Freaky Slots')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

font = pygame.font.SysFont(None, 70)
small_font = pygame.font.SysFont(None, 40)

pygame.mixer.music.load('intro.mp3')
pygame.mixer.music.play(-1, 0.0)  # -1 pro nekonečné opakování
is_playing = True


credit = 500
credit_min = 0
credit_max = 1000
credit_slider_pos = int(credit * (screen_width - 200) / credit_max)

bet = 2.0
screen_filled = False
user_input = ''
slot_symbols = []

grid_rows, grid_cols = 3, 3
cell_width, cell_height = 150, 80

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


running = True
game_over = False
message = ''
message_timer = 0
win_sound_played = False
win_sound_time = 0

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if screen_filled and not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if spin_button.collidepoint(mouse_pos):
                    if credit >= bet:
                        credit -= bet
                        slot_symbols = functions.get_slot()


                        winnings = functions.check_winnings(slot_symbols)
                        if winnings != []:
                            winnings_value = functions.get_winnings_value(winnings)
                            message = f"You won: {winnings_value * bet:.2f} $"
                            message_timer = 30
                            credit += winnings_value * bet
                            if not win_sound_played:
                                pygame.mixer.Sound(functions.get_win_song(winnings)).play()
                                win_sound_time = pygame.time.get_ticks()
                                win_sound_played = True
                    else:
                        game_over = True

                if minus_button.collidepoint(mouse_pos) and bet > 0.25:
                    bet -= 0.25
                elif plus_button.collidepoint(mouse_pos) and bet < 5.0:
                    bet += 0.25


        else:  # Menu obrazovka
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.unicode.isdigit():
                    user_input += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_button.collidepoint(mouse_pos):
                    try:
                        credit = int(user_input)
                    except ValueError:
                        credit = 0
                    user_input = ''
                    screen_filled = True
                    pygame.mixer.music.stop()
                elif play_pause_button.collidepoint(mouse_pos):
                    if is_playing:
                        pygame.mixer.music.pause()
                        is_playing = False
                    else:
                        pygame.mixer.music.unpause()
                        is_playing = True

    if screen_filled:
        game_panel_rect = pygame.Rect(screen.get_width() // 2 - 300, screen.get_height() // 2 - 200, 600, 400)
        pygame.draw.rect(screen, GREY, game_panel_rect)
        draw_text("Let's Get Freaky!", font, WHITE, screen, game_panel_rect.centerx, game_panel_rect.top - 50)

        # Výherní mřížka
        for row in range(grid_rows):
            for col in range(grid_cols):
                cell_x = game_panel_rect.left + 50 + col * (cell_width + 10)
                cell_y = game_panel_rect.top + 50 + row * (cell_height + 10)
                cell_rect = pygame.Rect(cell_x, cell_y, cell_width, cell_height)
                pygame.draw.rect(screen, WHITE, cell_rect, 1)

                if slot_symbols:
                    symbol_name = slot_symbols[row][col]
                    try:
                        img = pygame.image.load(f'{symbol_name}.jpg')
                        img = pygame.transform.scale(img, (cell_width, cell_height))
                        screen.blit(img, (cell_x, cell_y))
                    except pygame.error:
                        draw_text('?', small_font, WHITE, screen, cell_rect.centerx, cell_rect.centery)


        spin_button = pygame.Rect(game_panel_rect.centerx - 75, game_panel_rect.bottom - 60, 150, 50)
        pygame.draw.rect(screen, GREEN, spin_button)
        draw_text('SPIN', small_font, WHITE, screen, spin_button.centerx, spin_button.centery)


        minus_button = pygame.Rect(game_panel_rect.centerx - 150, game_panel_rect.bottom + 80, 70, 50)
        pygame.draw.rect(screen, RED, minus_button)
        draw_text('-', small_font, WHITE, screen, minus_button.centerx, minus_button.centery)

        draw_text(f"Bet: {bet:.2f} $", small_font, WHITE, screen, game_panel_rect.centerx, game_panel_rect.bottom + 100)


        plus_button = pygame.Rect(game_panel_rect.centerx + 80, game_panel_rect.bottom + 80, 70, 50)
        pygame.draw.rect(screen, GREEN, plus_button)
        draw_text('+', small_font, WHITE, screen, plus_button.centerx, plus_button.centery)


        draw_text(f"Credits: {credit}", small_font, WHITE, screen, game_panel_rect.centerx, game_panel_rect.bottom + 40)

        if game_over:
            draw_text("GAME OVER", font, RED, screen, screen.get_width() // 2, screen.get_height() // 2)

        if win_sound_played and pygame.time.get_ticks() - win_sound_time >= 2000:
            win_sound_played = False

        if message_timer > 0:
            draw_text(message, small_font, GREEN, screen, game_panel_rect.centerx, game_panel_rect.bottom + 150)
            message_timer -= 1

    else:
        draw_text('Freaky Slots', font, WHITE, screen, screen.get_width() // 2, screen.get_height() // 4 - 50)
        draw_text('Credit:', small_font, WHITE, screen, screen.get_width() // 2, screen.get_height() // 2)

        input_box = pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 + 40, 200, 40)
        pygame.draw.rect(screen, GREY, input_box, 2)
        draw_text(user_input, small_font, WHITE, screen, input_box.centerx, input_box.centery)

        start_button = pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 + 100, 200, 50)
        pygame.draw.rect(screen, GREY, start_button)
        draw_text('START', small_font, WHITE, screen, start_button.centerx, start_button.centery)

        play_pause_button = pygame.Rect(screen.get_width() // 2 - 50, screen.get_height() // 2 + 160, 100, 40)
        pygame.draw.rect(screen, GREY, play_pause_button)
        button_text = "PAUSE" if is_playing else "PLAY"
        draw_text(button_text, small_font, WHITE, screen, play_pause_button.centerx, play_pause_button.centery)

    pygame.display.update()

pygame.quit()
sys.exit()
