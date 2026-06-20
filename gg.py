#!/usr/bin/env python3
import os
import random
import time

# Constants
GRID_SIZE = 20
MAX_TURNS = 50
ASTEROID_COUNT = 4
COLLAPSE_WEIGHTS = [1, 1, 1, 1, 1, 1, 1, 2, 2, 3]  # 70% low, 20% medium, 10% high

# ANSI Escape Codes
CLEAR = "\033[2J\033[H"
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
GRAY = "\033[90m"
BOLD = "\033[1m"
REVERSE = "\033[7m"

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_at(y, x, text, color=""):
    print(f"\033[{y+1};{x+1}H{color}{text}{RESET}", end="")

def main():
    player_y, player_x = GRID_SIZE // 2, GRID_SIZE // 2
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    asteroids = []
    score = 0
    turns = 0

    # Initialize quantum tiles (superposition)
    for _ in range(15):
        y, x = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if grid[y][x] == 0:
            grid[y][x] = -1  # Superposition state

    # Spawn asteroids
    for _ in range(ASTEROID_COUNT):
        y, x = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if grid[y][x] == 0 and (y, x) != (player_y, player_x):
            asteroids.append((y, x))

    # Game loop
    while turns < MAX_TURNS:
        clear_screen()

        # Render grid
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if (y, x) == (player_y, player_x):
                    print_at(y, x, "█", BOLD + REVERSE)
                elif (y, x) in asteroids:
                    print_at(y, x, "@", RED + BOLD)
                elif grid[y][x] > 0:
                    print_at(y, x, "*", GREEN + BOLD)
                elif grid[y][x] == -1:
                    print_at(y, x, "~", GRAY)
                else:
                    print_at(y, x, " ")

        # Render HUD
        print_at(0, GRID_SIZE + 2, f"Score: {score}")
        print_at(1, GRID_SIZE + 2, f"Turns: {turns}/{MAX_TURNS}")
        print_at(2, GRID_SIZE + 2, "WASD: Move | Q: Quit")

        # Check for collisions
        if (player_y, player_x) in asteroids:
            print_at(GRID_SIZE // 2, GRID_SIZE // 2 - 4, "YOU HIT AN ASTEROID!", RED + BOLD)
            time.sleep(2)
            break

        # Handle input
        try:
            key = input("\033[25;0H")[:1].lower()
        except:
            key = ''

        if key == 'q':
            break
        elif key == 'w' and player_y > 0:
            player_y -= 1
        elif key == 's' and player_y < GRID_SIZE - 1:
            player_y += 1
        elif key == 'a' and player_x > 0:
            player_x -= 1
        elif key == 'd' and player_x < GRID_SIZE - 1:
            player_x += 1

        # Check for adjacent superposition collapse
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy == 0 and dx == 0:
                    continue
                ny, nx = player_y + dy, player_x + dx
                if 0 <= ny < GRID_SIZE and 0 <= nx < GRID_SIZE and grid[ny][nx] == -1:
                    value = random.choice(COLLAPSE_WEIGHTS)
                    grid[ny][nx] = value
                    score += value
                    os.system('echo -e "\a"')  # Terminal bell

        # Move asteroids randomly every 3 turns
        if turns % 3 == 0:
            new_asteroids = []
            for ay, ax in asteroids:
                moves = [(0,1), (1,0), (0,-1), (-1,0)]
                random.shuffle(moves)
                for dy, dx in moves:
                    ny, nx = ay + dy, ax + dx
                    if 0 <= ny < GRID_SIZE and 0 <= nx < GRID_SIZE and grid[ny][nx] == 0 and (ny, nx) != (player_y, player_x):
                        new_asteroids.append((ny, nx))
                        break
                else:
                    new_asteroids.append((ay, ax))
            asteroids = new_asteroids

        turns += 1
        time.sleep(0.1)

    # End game
    clear_screen()
    print(f"\033[{GRID_SIZE//2 - 1};{GRID_SIZE//2 - 5}H{BOLD}GAME OVER{RESET}")
    print(f"\033[{GRID_SIZE//2};{GRID_SIZE//2 - 4}HFinal Score: {score}{RESET}")
    print(f"\033[{GRID_SIZE//2 + 1};{GRID_SIZE//2 - 6}HPress Enter to exit...{RESET}")
    input()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
