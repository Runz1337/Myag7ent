#!/usr/bin/env python3
import curses
import random
import time
import os

# Constants
GRID_SIZE = 20
PLAYER_CHAR = '@'
ORE_CHAR = 'O'
ASTEROID_CHAR = '#'
EMPTY_CHAR = '.'
MAX_ORE = 5
MAX_ASTEROIDS = 8
MINING_DELAY = 0.3  # seconds between mining actions

# Game state
class GameState:
    def __init__(self):
        self.grid = [[EMPTY_CHAR for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.player_x = GRID_SIZE // 2
        self.player_y = GRID_SIZE // 2
        self.ore_count = 0
        self.asteroids = []
        self.ore_spots = []
        self.game_over = False
        self.last_mine_time = 0

        # Place ore and asteroids
        self.generate_resources()

    def generate_resources(self):
        # Place ore
        for _ in range(MAX_ORE):
            while True:
                x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
                if (x, y) != (self.player_x, self.player_y) and self.grid[y][x] == EMPTY_CHAR:
                    self.grid[y][x] = ORE_CHAR
                    self.ore_spots.append((x, y))
                    break

        # Place asteroids
        for _ in range(MAX_ASTEROIDS):
            while True:
                x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
                if (x, y) != (self.player_x, self.player_y) and self.grid[y][x] == EMPTY_CHAR:
                    self.grid[y][x] = ASTEROID_CHAR
                    self.asteroids.append((x, y))
                    break

    def move_player(self, dx, dy):
        new_x = self.player_x + dx
        new_y = self.player_y + dy

        # Boundary check
        if not (0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE):
            return

        # Collision with asteroid
        if (new_x, new_y) in self.asteroids:
            self.game_over = True
            return

        # Move player
        self.player_x = new_x
        self.player_y = new_y

        # Check for ore
        if (new_x, new_y) in self.ore_spots:
            self.ore_spots.remove((new_x, new_y))
            self.grid[new_y][new_x] = EMPTY_CHAR
            self.ore_count += 1
            # Spawn new ore elsewhere
            while True:
                x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
                if (x, y) != (self.player_x, self.player_y) and self.grid[y][x] == EMPTY_CHAR and (x, y) not in self.asteroids:
                    self.grid[y][x] = ORE_CHAR
                    self.ore_spots.append((x, y))
                    break

    def mine(self):
        current_time = time.time()
        if current_time - self.last_mine_time < MINING_DELAY:
            return
        self.last_mine_time = current_time

        # Check if player is on ore
        if (self.player_x, self.player_y) in self.ore_spots:
            self.ore_spots.remove((self.player_x, self.player_y))
            self.grid[self.player_y][self.player_x] = EMPTY_CHAR
            self.ore_count += 1
            # Spawn new ore
            while True:
                x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
                if (x, y) != (self.player_x, self.player_y) and self.grid[y][x] == EMPTY_CHAR and (x, y) not in self.asteroids:
                    self.grid[y][x] = ORE_CHAR
                    self.ore_spots.append((x, y))
                    break
            # Play sound effect
            print('\a', end='', flush=True)

    def render(self, stdscr):
        stdscr.clear()
        # Draw grid
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                char = self.grid[y][x]
                if x == self.player_x and y == self.player_y:
                    char = PLAYER_CHAR
                stdscr.addch(y, x, char)

        # Draw HUD
        stdscr.addstr(GRID_SIZE + 1, 0, f"Ore collected: {self.ore_count}")
        stdscr.addstr(GRID_SIZE + 2, 0, "Use arrow keys to move. Press 'm' to mine. Press 'q' to quit.")
        
        if self.game_over:
            stdscr.addstr(GRID_SIZE // 2, GRID_SIZE // 2 - 5, "GAME OVER - ASTEROID COLLISION!", curses.A_BOLD | curses.A_REVERSE)
            stdscr.addstr(GRID_SIZE // 2 + 1, GRID_SIZE // 2 - 7, "Press 'r' to restart or 'q' to quit")

        stdscr.refresh()

def main(stdscr):
    # Initialize curses
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    game = GameState()

    while True:
        game.render(stdscr)

        # Handle input
        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == ord('r') and game.game_over:
            game = GameState()  # Restart
        elif key == ord('m'):
            game.mine()
        elif key == curses.KEY_UP:
            game.move_player(0, -1)
        elif key == curses.KEY_DOWN:
            game.move_player(0, 1)
        elif key == curses.KEY_LEFT:
            game.move_player(-1, 0)
        elif key == curses.KEY_RIGHT:
            game.move_player(1, 0)

        # Auto-check game over
        if game.game_over:
            while True:
                key = stdscr.getch()
                if key == ord('q'):
                    return
                elif key == ord('r'):
                    game = GameState()
                    break

if __name__ == "__main__":
    curses.wrapper(main)
