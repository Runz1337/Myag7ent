import random
import time

class Game:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.grid = [['.' for _ in range(width)] for _ in range(height)]
        self.player = {'x': width//2, 'y': height//2, 'ore': 0, 'health': 100}
        self.asteroids = []
        self.ore_spots = []
        self.generate_map()

    def generate_map(self):
        # Spawn 8 asteroids
        for _ in range(8):
            while True:
                x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
                if (x, y) != (self.player['x'], self.player['y']):
                    self.asteroids.append((x, y))
                    self.grid[y][x] = 'A'
                    break

        # Spawn 6 ore spots
        for _ in range(6):
            while True:
                x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
                if (x, y) not in self.asteroids and (x, y) != (self.player['x'], self.player['y']):
                    self.ore_spots.append((x, y))
                    self.grid[y][x] = 'O'
                    break

    def move_player(self, dx, dy):
        x, y = self.player['x'] + dx, self.player['y'] + dy
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False

        # Collision with asteroid
        if (x, y) in self.asteroids:
            self.player['health'] -= 20
            if self.player['health'] <= 0:
                return 'dead'
            return False

        # Collect ore
        if (x, y) in self.ore_spots:
            self.player['ore'] += 1
            self.ore_spots.remove((x, y))
            self.grid[y][x] = '.'

        # Move player
        self.player['x'], self.player['y'] = x, y
        return True

    def render(self):
        # Copy grid
        display = [row[:] for row in self.grid]
        display[self.player['y']][self.player['x']] = '@'

        # Render
        output = []
        output.append(" STAR MINER — Press WASD to move, Q to quit")
        output.append(" " + "-" * self.width)
        for row in display:
            output.append("|" + ''.join(row) + "|")
        output.append(" " + "-" * self.width)
        output.append(f"Ore: {self.player['ore']} | Health: {self.player['health']}")
        return "\n".join(output)

    def is_won(self):
        return self.player['ore'] >= 6
