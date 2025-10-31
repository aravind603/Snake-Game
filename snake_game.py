import pygame
import random
import sys

# -------------------------
# INITIAL SETUP
# -------------------------
pygame.init()
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
BLOCK_SIZE = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
DARK_GREEN = (0, 150, 0)
YELLOW = (255, 200, 0)

# Create window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")

# Fonts
small_font = pygame.font.SysFont(None, 24)
big_font = pygame.font.SysFont(None, 40)
title_font = pygame.font.SysFont(None, 60)

clock = pygame.time.Clock()


# -------------------------
# UTILITY FUNCTIONS
# -------------------------
def draw_text_center(surface, text, font, color, y):
    text_surf = font.render(text, True, color)
    rect = text_surf.get_rect(center=(WINDOW_WIDTH // 2, y))
    surface.blit(text_surf, rect)


def random_food_position():
    x = random.randrange(0, WINDOW_WIDTH - BLOCK_SIZE, BLOCK_SIZE)
    y = random.randrange(0, WINDOW_HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
    return x, y


# -------------------------
# PAUSE SCREEN
# -------------------------
def pause_screen():
    paused = True
    while paused:
        screen.fill(BLACK)
        draw_text_center(screen, "PAUSED", title_font, YELLOW, WINDOW_HEIGHT // 3)
        draw_text_center(screen, "Press SPACE to Resume", small_font, WHITE, WINDOW_HEIGHT // 2)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    paused = False


# -------------------------
# MENU: SHAPE SELECTION
# -------------------------
def menu_screen_shape():
    while True:
        screen.fill(BLACK)
        draw_text_center(screen, "SNAKE GAME", title_font, YELLOW, WINDOW_HEIGHT // 4)
        draw_text_center(screen, "Choose Snake Shape", big_font, WHITE, WINDOW_HEIGHT // 2 - 40)
        draw_text_center(screen, "1 - Rectangle", small_font, WHITE, WINDOW_HEIGHT // 2 + 10)
        draw_text_center(screen, "2 - Circle", small_font, WHITE, WINDOW_HEIGHT // 2 + 40)
        draw_text_center(screen, "Press 1 or 2", small_font, YELLOW, WINDOW_HEIGHT - 50)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key in (pygame.K_1, pygame.K_KP1):
                    return "rectangle"
                if event.key in (pygame.K_2, pygame.K_KP2):
                    return "circle"


# -------------------------
# MENU: SPEED SELECTION
# -------------------------
def menu_screen_speed():
    while True:
        screen.fill(BLACK)
        draw_text_center(screen, "Choose Speed Level", big_font, WHITE, WINDOW_HEIGHT // 2 - 60)
        draw_text_center(screen, "1 - Slow", small_font, WHITE, WINDOW_HEIGHT // 2 - 10)
        draw_text_center(screen, "2 - Medium", small_font, WHITE, WINDOW_HEIGHT // 2 + 20)
        draw_text_center(screen, "3 - Fast", small_font, WHITE, WINDOW_HEIGHT // 2 + 50)
        draw_text_center(screen, "4 - Very Fast", small_font, WHITE, WINDOW_HEIGHT // 2 + 80)
        draw_text_center(screen, "Press 1, 2, 3 or 4", small_font, YELLOW, WINDOW_HEIGHT - 50)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key in (pygame.K_1, pygame.K_KP1):
                    return 8   # Slow
                if event.key in (pygame.K_2, pygame.K_KP2):
                    return 13  # Medium
                if event.key in (pygame.K_3, pygame.K_KP3):
                    return 18  # Fast
                if event.key in (pygame.K_4, pygame.K_KP4):
                    return 25  # Very Fast


# -------------------------
# MAIN GAME LOOP
# -------------------------
def game_loop(chosen_shape, fps_speed):

    x = (WINDOW_WIDTH // 2) // BLOCK_SIZE * BLOCK_SIZE
    y = (WINDOW_HEIGHT // 2) // BLOCK_SIZE * BLOCK_SIZE

    x_change = BLOCK_SIZE
    y_change = 0

    snake_list = [[x, y]]
    snake_length = 1

    food_x, food_y = random_food_position()
    score = 0
    game_over = False

    while True:

        # INPUT HANDLING
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # ESC = quit game
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # SPACE = pause
                if event.key == pygame.K_SPACE:
                    pause_screen()
                    continue

                # Movement
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = BLOCK_SIZE
                    x_change = 0

        # MOVE SNAKE
        x += x_change
        y += y_change

        # Boundary collision
        if x < 0 or x >= WINDOW_WIDTH or y < 0 or y >= WINDOW_HEIGHT:
            game_over = True

        screen.fill(BLACK)

        # Draw food
        pygame.draw.rect(screen, RED, (food_x, food_y, BLOCK_SIZE, BLOCK_SIZE))

        # Update snake body
        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Self collision
        if snake_head in snake_list[:-1]:
            game_over = True

        # Draw snake
        for i, segment in enumerate(snake_list):
            sx, sy = segment

            if chosen_shape == "rectangle":
                color = DARK_GREEN if i == len(snake_list) - 1 else GREEN
                pygame.draw.rect(screen, color, (sx, sy, BLOCK_SIZE, BLOCK_SIZE))
            else:
                center = (sx + BLOCK_SIZE // 2, sy + BLOCK_SIZE // 2)
                color = DARK_GREEN if i == len(snake_list) - 1 else GREEN
                pygame.draw.circle(screen, color, center, BLOCK_SIZE // 2)

        # Display score
        score_text = small_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.update()

        # Eating food
        if x == food_x and y == food_y:
            food_x, food_y = random_food_position()
            snake_length += 1
            score += 10

        clock.tick(fps_speed)

        # GAME OVER SCREEN
        if game_over:
            while True:
                screen.fill(BLACK)
                draw_text_center(screen, "GAME OVER", title_font, RED, WINDOW_HEIGHT // 3)
                draw_text_center(screen, f"Score: {score}", big_font, WHITE, WINDOW_HEIGHT // 2 - 20)
                draw_text_center(screen, "Press C to Play Again", small_font, YELLOW, WINDOW_HEIGHT // 2 + 40)
                draw_text_center(screen, "Press Q to Quit", small_font, YELLOW, WINDOW_HEIGHT // 2 + 70)
                pygame.display.update()

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()

                        if event.key == pygame.K_c:
                            return  # restart entire game


# -------------------------
# START PROGRAM
# -------------------------
if __name__ == "__main__":
    while True:
        shape = menu_screen_shape()
        speed = menu_screen_speed()
        game_loop(shape, speed)