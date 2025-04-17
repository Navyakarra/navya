import pygame
import random
import time

class Puzzle:
    def __init__(self, size=3):
        self.size = size
        self.tiles = []
        self.empty_pos = (size-1, size-1)
        self.moves = 0
        self.start_time = 0
        self.solved = False
        self.hints_used = 0
        self.hint_cooldown = 0
        self.initialize_puzzle()

    def initialize_puzzle(self):
        # Create solved puzzle
        self.tiles = [[i + j * self.size + 1 for i in range(self.size)] for j in range(self.size)]
        self.tiles[self.size-1][self.size-1] = 0  # Empty tile
        
        # Shuffle the puzzle
        for _ in range(1000):
            moves = self.get_valid_moves()
            if moves:
                self.move_tile(random.choice(moves))
        
        self.start_time = time.time()
        self.moves = 0
        self.solved = False

    def get_valid_moves(self):
        moves = []
        x, y = self.empty_pos
        
        if x > 0:
            moves.append((x-1, y))
        if x < self.size-1:
            moves.append((x+1, y))
        if y > 0:
            moves.append((x, y-1))
        if y < self.size-1:
            moves.append((x, y+1))
            
        return moves

    def move_tile(self, pos):
        if pos in self.get_valid_moves():
            x, y = pos
            empty_x, empty_y = self.empty_pos
            self.tiles[empty_y][empty_x] = self.tiles[y][x]
            self.tiles[y][x] = 0
            self.empty_pos = pos
            self.moves += 1
            return True
        return False

    def is_solved(self):
        for y in range(self.size):
            for x in range(self.size):
                if self.tiles[y][x] != (x + y * self.size + 1) % (self.size * self.size):
                    return False
        return True

    def get_hint(self):
        if self.hints_used >= 3 or self.hint_cooldown > 0:
            return None
            
        # Find the first misplaced tile
        for y in range(self.size):
            for x in range(self.size):
                correct_value = (x + y * self.size + 1) % (self.size * self.size)
                if self.tiles[y][x] != correct_value:
                    # Find where this tile should go
                    target_y = (self.tiles[y][x] - 1) // self.size
                    target_x = (self.tiles[y][x] - 1) % self.size
                    self.hints_used += 1
                    self.hint_cooldown = 5  # 5 seconds cooldown
                    return (x, y), (target_x, target_y)
        return None

    def update(self):
        if self.hint_cooldown > 0:
            self.hint_cooldown -= 1/60  # Assuming 60 FPS

    def draw(self, screen, x, y, tile_size):
        for i in range(self.size):
            for j in range(self.size):
                value = self.tiles[i][j]
                if value != 0:
                    rect = pygame.Rect(x + j * tile_size, y + i * tile_size, tile_size, tile_size)
                    pygame.draw.rect(screen, (200, 200, 200), rect)
                    pygame.draw.rect(screen, (0, 0, 0), rect, 2)
                    
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(value), True, (0, 0, 0))
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)

    def get_time_remaining(self):
        elapsed = time.time() - self.start_time
        return max(0, 300 - elapsed)  # 5 minutes = 300 seconds 