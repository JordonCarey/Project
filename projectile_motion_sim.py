import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Projectile Motion Simulator")

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Initialize variables
gravity = 9.8  # Acceleration due to gravity (m/s^2)
initial_velocity = 50  # Default initial velocity
angle = 45  # Default launch angle
time = 0  # Time elapsed (s)
paused = False
time_scale = 1.0
velocity_x, velocity_y = 0, 0

# Function to calculate the initial components of velocity
def calculate_velocity_components(velocity, angle):
    velocity_x = velocity * math.cos(math.radians(angle))
    velocity_y = velocity * math.sin(math.radians(angle))
    return velocity_x, velocity_y

def draw_text(text, position, color=WHITE, size=36):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

# Set up the projectile's initial position
x = 0
y = height

# Set up the clock
clock = pygame.time.Clock()

# Function to reset the simulation
def reset_simulation():
    global time, velocity_x, velocity_y, x, y, paused
    time = 0
    paused = False
    velocity_x, velocity_y = calculate_velocity_components(initial_velocity, angle)
    x = 0
    y = height

# Function to draw the projectile
def draw_projectile(x, y):
    pygame.draw.circle(screen, WHITE, (int(x), int(y)), 5)

# Function to draw buttons
def draw_button(text, x, y, w, h, color):
    pygame.draw.rect(screen, color, (x, y, w, h))
    draw_text(text, (x + 10, y + 10), BLACK, 24)

# Function to check if a button is clicked
def is_button_clicked(x, y, w, h, mouse_pos):
    return x <= mouse_pos[0] <= x + w and y <= mouse_pos[1] <= y + h

# Function to handle input for initial velocity and angle
def handle_input():
    global initial_velocity, angle
    input_active = True
    user_text = ''
    field = 'velocity'  # Start by asking for velocity
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if field == 'velocity':
                        initial_velocity = float(user_text)
                        user_text = ''
                        field = 'angle'
                    elif field == 'angle':
                        angle = float(user_text)
                        input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

        # Render input screen
        screen.fill(BLACK)
        if field == 'velocity':
            prompt = 'Enter Initial Velocity (m/s): ' + user_text
        else:
            prompt = 'Enter Launch Angle (degrees): ' + user_text
        
        draw_text(prompt, (100, height // 2))
        pygame.display.flip()
        clock.tick(30)

    return True

# Main loop
if handle_input():  # Only run if input is handled successfully
    reset_simulation()
    running = True
    while running:
        # Handle events
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if is_button_clicked(50, 50, 100, 40, mouse_pos):  # Reset button
                    reset_simulation()
                elif is_button_clicked(50, 100, 100, 40, mouse_pos):  # Pause/Resume button
                    paused = not paused
                elif is_button_clicked(50, 150, 100, 40, mouse_pos):  # Increase speed button
                    time_scale *= 1.5
                elif is_button_clicked(50, 200, 100, 40, mouse_pos):  # Decrease speed button
                    time_scale /= 1.5

        if not paused:
            # Update the projectile's position
            x += velocity_x * time_scale
            y -= velocity_y * time_scale
            velocity_y -= gravity * time_scale

            # Bounce off the ground
            if y >= height:
                y = height
                velocity_y = -velocity_y * 0.9  # Dampen the vertical bounce

            # Bounce off the walls
            if x <= 0 or x >= width:
                velocity_x = -velocity_x  # Reverse horizontal direction

            # Clear the screen
            screen.fill(BLACK)

            # Draw the projectile
            draw_projectile(x, y)

            # Draw the buttons
            draw_button("Reset", 50, 50, 100, 40, GRAY)
            draw_button("Pause/Resume", 50, 100, 100, 40, GRAY)
            draw_button("Speed +", 50, 150, 100, 40, GRAY)
            draw_button("Speed -", 50, 200, 100, 40, GRAY)

            # Update the display
            pygame.display.flip()

        # Limit the frame rate
        clock.tick(60)

# Quit Pygame
pygame.quit()
