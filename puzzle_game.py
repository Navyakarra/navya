import pygame
import sys
import random
import json
import os
from PIL import Image, ImageTk
from puzzle import Puzzle
import numpy as np

# Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.font.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 150, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Sound effects
def create_sound(frequency, duration):
    """Create a simple sound effect using numpy"""
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    # Create stereo sound by duplicating the mono sound
    sound = np.sin(2 * np.pi * frequency * t)
    sound = np.column_stack((sound, sound))  # Convert to stereo
    sound = (sound * 32767).astype(np.int16)
    return pygame.sndarray.make_sound(sound)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=10)
        
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class InputBox:
    def __init__(self, x, y, width, height, text='', is_password=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GRAY
        self.text = text
        self.is_password = is_password
        self.font = pygame.font.Font(None, 36)
        self.txt_surface = self.font.render(text, True, BLACK)
        self.active = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            self.color = LIGHT_BLUE if self.active else GRAY
            
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                display_text = '*' * len(self.text) if self.is_password else self.text
                self.txt_surface = self.font.render(display_text, True, BLACK)
        return False
                
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, self.color, self.rect, 2)
        display_text = '*' * len(self.text) if self.is_password else self.text
        self.txt_surface = self.font.render(display_text, True, BLACK)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.dragging = False
        
    def draw(self, screen):
        # Draw text
        text_surface = self.font.render(self.text, True, BLACK)
        screen.blit(text_surface, (self.rect.x, self.rect.y - 30))
        
        # Draw slider background
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # Draw slider handle
        handle_x = self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width
        handle_rect = pygame.Rect(handle_x - 5, self.rect.y - 5, 10, self.rect.height + 10)
        pygame.draw.rect(screen, BLUE, handle_rect)
        pygame.draw.rect(screen, BLACK, handle_rect, 2)
        
        # Draw value
        value_text = f"{int(self.value)}%"
        value_surface = self.font.render(value_text, True, BLACK)
        screen.blit(value_surface, (self.rect.x + self.rect.width + 10, self.rect.y))
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.update_value(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.update_value(event.pos[0])
            
    def update_value(self, mouse_x):
        relative_x = max(0, min(mouse_x - self.rect.x, self.rect.width))
        self.value = self.min_val + (relative_x / self.rect.width) * (self.max_val - self.min_val)
        return self.value

class PuzzleGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Puzzle Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_screen = "login"  # login, signup, game, settings
        self.user_data = {}
        self.load_user_data()
        self.message = ""
        self.message_timer = 0
        self.message_color = BLACK
        
        # Create login UI elements
        self.username_box = InputBox(300, 200, 200, 40)
        self.password_box = InputBox(300, 270, 200, 40, is_password=True)
        self.login_button = Button(300, 340, 200, 40, "Login", BLUE, LIGHT_BLUE)
        self.signup_button = Button(300, 400, 200, 40, "Sign Up", GREEN, (100, 255, 100))
        
        # Create signup UI elements
        self.signup_username_box = InputBox(300, 200, 200, 40)
        self.signup_password_box = InputBox(300, 270, 200, 40, is_password=True)
        self.confirm_password_box = InputBox(300, 340, 200, 40, is_password=True)
        self.register_button = Button(300, 410, 200, 40, "Register", GREEN, (100, 255, 100))
        self.back_button = Button(300, 470, 200, 40, "Back", GRAY, (180, 180, 180))
        
        # Game settings
        self.volume = 0.5
        self.brightness = 1.0
        self.coins = 0
        self.hints_available = 3
        self.time_limit = 300  # 5 minutes in seconds
        self.time_remaining = self.time_limit
        
        # Create puzzle background pattern
        self.create_background_pattern()
        
        # Add puzzle-related attributes
        self.puzzle = None
        self.tile_size = 100
        self.puzzle_x = (SCREEN_WIDTH - 300) // 2
        self.puzzle_y = (SCREEN_HEIGHT - 300) // 2
        self.selected_tile = None
        
        # Initialize coins for new users
        self.starting_coins = 10  # Changed to 10 coins
        self.coins = self.starting_coins
        
        # Add game UI buttons
        self.new_puzzle_button = Button(20, 20, 150, 40, "New Puzzle", BLUE, LIGHT_BLUE)
        self.hint_button = Button(20, 70, 150, 40, f"Hint ({self.hints_available})", GREEN, (100, 255, 100))
        self.settings_button = Button(20, 120, 150, 40, "Settings", GRAY, (180, 180, 180))
        
        # Initialize puzzle immediately
        self.puzzle = Puzzle(3)
        self.time_remaining = self.time_limit
        
        # Add settings UI elements
        self.volume_slider = Slider(300, 200, 200, 20, 0, 100, 50, "Volume")
        self.brightness_slider = Slider(300, 300, 200, 20, 0, 100, 100, "Brightness")
        self.back_button = Button(300, 400, 200, 40, "Back to Game", BLUE, LIGHT_BLUE)
        
        # Initialize sounds
        self.sounds = {
            'click': create_sound(440, 0.1),  # A4 note
            'success': create_sound(880, 0.2),  # A5 note
            'error': create_sound(220, 0.2),  # A3 note
            'move': create_sound(660, 0.1),  # E5 note
            'hint': create_sound(550, 0.15),  # C#5 note
        }
        
        # Set initial volume
        self.update_volume(self.volume)
        
    def create_background_pattern(self):
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill(WHITE)
        for i in range(0, SCREEN_WIDTH, 100):
            for j in range(0, SCREEN_HEIGHT, 100):
                color = (230, 230, 255) if (i + j) // 100 % 2 == 0 else (220, 220, 245)
                pygame.draw.rect(self.background, color, (i, j, 100, 100))
                pygame.draw.rect(self.background, (200, 200, 235), (i, j, 100, 100), 1)

    def show_message(self, text, color=BLACK):
        self.message = text
        self.message_timer = 2 * FPS  # Show message for 2 seconds
        self.message_color = color

    def draw_login_screen(self):
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw title
        font = pygame.font.Font(None, 64)
        title = font.render("Puzzle Game", True, BLUE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # Draw input labels
        font = pygame.font.Font(None, 36)
        username_label = font.render("Username:", True, BLACK)
        password_label = font.render("Password:", True, BLACK)
        self.screen.blit(username_label, (300, 170))
        self.screen.blit(password_label, (300, 240))
        
        # Draw input boxes and buttons
        self.username_box.draw(self.screen)
        self.password_box.draw(self.screen)
        self.login_button.draw(self.screen)
        self.signup_button.draw(self.screen)
        
        # Draw message if any
        if self.message and self.message_timer > 0:
            msg_surface = font.render(self.message, True, self.message_color)
            msg_rect = msg_surface.get_rect(center=(SCREEN_WIDTH//2, 500))
            self.screen.blit(msg_surface, msg_rect)
            self.message_timer -= 1

    def draw_signup_screen(self):
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw title
        font = pygame.font.Font(None, 64)
        title = font.render("Sign Up", True, GREEN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # Draw input labels
        font = pygame.font.Font(None, 36)
        username_label = font.render("Username:", True, BLACK)
        password_label = font.render("Password:", True, BLACK)
        confirm_label = font.render("Confirm Password:", True, BLACK)
        self.screen.blit(username_label, (300, 170))
        self.screen.blit(password_label, (300, 240))
        self.screen.blit(confirm_label, (300, 310))
        
        # Draw input boxes and buttons
        self.signup_username_box.draw(self.screen)
        self.signup_password_box.draw(self.screen)
        self.confirm_password_box.draw(self.screen)
        self.register_button.draw(self.screen)
        self.back_button.draw(self.screen)
        
        # Draw message if any
        if self.message and self.message_timer > 0:
            msg_surface = font.render(self.message, True, self.message_color)
            msg_rect = msg_surface.get_rect(center=(SCREEN_WIDTH//2, 500))
            self.screen.blit(msg_surface, msg_rect)
            self.message_timer -= 1

    def handle_login_events(self, event):
        self.username_box.handle_event(event)
        self.password_box.handle_event(event)
        
        if self.login_button.handle_event(event):
            if self.login(self.username_box.text, self.password_box.text):
                self.play_sound('success')
                self.current_screen = "game"
                self.show_message("Login successful!", GREEN)
            else:
                self.play_sound('error')
                self.show_message("Invalid credentials!", RED)
                
        if self.signup_button.handle_event(event):
            self.play_sound('click')
            self.current_screen = "signup"
            self.signup_username_box.text = ""
            self.signup_password_box.text = ""
            self.confirm_password_box.text = ""

    def handle_signup_events(self, event):
        self.signup_username_box.handle_event(event)
        self.signup_password_box.handle_event(event)
        self.confirm_password_box.handle_event(event)
        
        if self.register_button.handle_event(event):
            if self.signup_password_box.text != self.confirm_password_box.text:
                self.play_sound('error')
                self.show_message("Passwords do not match!", RED)
            elif len(self.signup_username_box.text) < 3:
                self.play_sound('error')
                self.show_message("Username too short!", RED)
            elif len(self.signup_password_box.text) < 4:
                self.play_sound('error')
                self.show_message("Password too short!", RED)
            else:
                if self.signup(self.signup_username_box.text, self.signup_password_box.text):
                    self.play_sound('success')
                    self.show_message("Registration successful!", GREEN)
                    self.current_screen = "login"
                else:
                    self.play_sound('error')
                    self.show_message("Username already exists!", RED)
        
        if self.back_button.handle_event(event):
            self.play_sound('click')
            self.current_screen = "login"

    def load_user_data(self):
        try:
            with open("user_data.json", "r") as f:
                self.user_data = json.load(f)
        except FileNotFoundError:
            self.user_data = {}

    def save_user_data(self):
        with open("user_data.json", "w") as f:
            json.dump(self.user_data, f)

    def login(self, username, password):
        if username in self.user_data and self.user_data[username]["password"] == password:
            self.current_user = username
            self.coins = self.user_data[username].get("coins", self.starting_coins)
            return True
        return False

    def signup(self, username, password):
        if username in self.user_data:
            return False
        self.user_data[username] = {"password": password, "coins": self.starting_coins}
        self.save_user_data()
        return True

    def start_new_puzzle(self):
        self.puzzle = Puzzle(3)  # 3x3 puzzle
        self.time_remaining = self.time_limit
        self.hints_available = 3
        self.hint_button.text = f"Hint ({self.hints_available})"
        self.user_data[self.current_user]["coins"] = self.coins
        self.save_user_data()
        return True

    def draw_game_screen(self):
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw game info
        font = pygame.font.Font(None, 36)
        
        # Draw time remaining
        minutes = int(self.time_remaining // 60)
        seconds = int(self.time_remaining % 60)
        time_text = f"Time: {minutes:02d}:{seconds:02d}"
        time_surface = font.render(time_text, True, BLACK)
        self.screen.blit(time_surface, (SCREEN_WIDTH - 170, 20))
        
        # Draw coins
        coins_text = f"Coins: {self.coins}"
        coins_surface = font.render(coins_text, True, BLACK)
        self.screen.blit(coins_surface, (SCREEN_WIDTH - 170, 60))
        
        # Draw moves
        if self.puzzle:
            moves_text = f"Moves: {self.puzzle.moves}"
            moves_surface = font.render(moves_text, True, BLACK)
            self.screen.blit(moves_surface, (SCREEN_WIDTH - 170, 100))
        
        # Draw buttons
        self.new_puzzle_button.draw(self.screen)
        self.hint_button.draw(self.screen)
        self.settings_button.draw(self.screen)
        
        # Draw puzzle
        if self.puzzle:
            self.puzzle.draw(self.screen, self.puzzle_x, self.puzzle_y, self.tile_size)
        
        # Draw message if any
        if self.message and self.message_timer > 0:
            msg_surface = font.render(self.message, True, self.message_color)
            msg_rect = msg_surface.get_rect(center=(SCREEN_WIDTH//2, 500))
            self.screen.blit(msg_surface, msg_rect)
            self.message_timer -= 1
    
    def draw_settings_screen(self):
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw title
        font = pygame.font.Font(None, 64)
        title = font.render("Settings", True, BLUE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # Draw sliders
        self.volume_slider.draw(self.screen)
        self.brightness_slider.draw(self.screen)
        
        # Draw back button
        self.back_button.draw(self.screen)
        
        # Draw message if any
        if self.message and self.message_timer > 0:
            msg_surface = font.render(self.message, True, self.message_color)
            msg_rect = msg_surface.get_rect(center=(SCREEN_WIDTH//2, 500))
            self.screen.blit(msg_surface, msg_rect)
            self.message_timer -= 1
    
    def handle_settings_events(self, event):
        self.volume_slider.handle_event(event)
        self.brightness_slider.handle_event(event)
        
        if self.back_button.handle_event(event):
            self.play_sound('click')
            self.current_screen = "game"
            self.update_volume(self.volume_slider.value / 100)
            self.brightness = self.brightness_slider.value / 100
            self.show_message("Settings saved!", GREEN)
    
    def handle_game_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check button clicks
            if self.new_puzzle_button.handle_event(event):
                self.start_new_puzzle()
                self.play_sound('click')
                self.show_message("New puzzle started!", BLUE)
                return
                
            if self.hint_button.handle_event(event):
                if self.hints_available > 0:
                    hint = self.puzzle.get_hint()
                    if hint:
                        self.hints_available -= 1
                        self.hint_button.text = f"Hint ({self.hints_available})"
                        current_pos, target_pos = hint
                        self.play_sound('hint')
                        self.show_message(f"Move tile at {current_pos} to {target_pos}", BLUE)
                    else:
                        self.play_sound('error')
                        self.show_message("No hint available!", RED)
                else:
                    self.play_sound('error')
                    self.show_message("No hints left!", RED)
                return
                
            if self.settings_button.handle_event(event):
                self.play_sound('click')
                self.current_screen = "settings"
                return
            
            # Check puzzle tile clicks
            if self.puzzle:
                # Convert mouse position to puzzle grid position
                grid_x = (mouse_pos[0] - self.puzzle_x) // self.tile_size
                grid_y = (mouse_pos[1] - self.puzzle_y) // self.tile_size
                
                if 0 <= grid_x < self.puzzle.size and 0 <= grid_y < self.puzzle.size:
                    if self.puzzle.move_tile((grid_x, grid_y)):
                        self.play_sound('move')
                        if self.puzzle.is_solved():
                            reward = 20
                            self.coins += reward
                            self.user_data[self.current_user]["coins"] = self.coins
                            self.save_user_data()
                            self.play_sound('success')
                            self.show_message(f"Puzzle Solved! +{reward} coins", GREEN)
    
    def update_game(self):
        if self.puzzle and not self.puzzle.is_solved():
            self.time_remaining -= 1/FPS
            if self.time_remaining <= 0:
                self.show_message("Time's up! Try again!", RED)
                self.start_new_puzzle()
            
            self.puzzle.update()

    def update_volume(self, volume):
        self.volume = max(0, min(1, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.volume)
    
    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.current_screen == "game":
                            self.current_screen = "settings"
                        elif self.current_screen == "settings":
                            self.current_screen = "game"
                
                if self.current_screen == "login":
                    self.handle_login_events(event)
                elif self.current_screen == "signup":
                    self.handle_signup_events(event)
                elif self.current_screen == "game":
                    self.handle_game_events(event)
                elif self.current_screen == "settings":
                    self.handle_settings_events(event)

            if self.current_screen == "login":
                self.draw_login_screen()
            elif self.current_screen == "signup":
                self.draw_signup_screen()
            elif self.current_screen == "game":
                self.draw_game_screen()
                self.update_game()
            elif self.current_screen == "settings":
                self.draw_settings_screen()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = PuzzleGame()
    game.run() 