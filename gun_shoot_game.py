import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Shoot the Object Game")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Load images
gun_img = pygame.image.load('gun1.png')
gun_img = pygame.transform.scale(gun_img, (50, 50))
bullet_img = pygame.image.load('bullet.png')
bullet_img = pygame.transform.scale(bullet_img, (10, 30))
fire_button_img = pygame.image.load('fire_button.png')
fire_button_img = pygame.transform.scale(fire_button_img, (50, 50))
left_arrow_img = pygame.image.load('left_arrow.png')
left_arrow_img = pygame.transform.scale(left_arrow_img, (50, 50))
right_arrow_img = pygame.image.load('right_arrow.png')
right_arrow_img = pygame.transform.scale(right_arrow_img, (50, 50))
background_img = pygame.image.load('background.png')

# Load target images
target_images = [
    pygame.image.load('target1.png'),
    pygame.image.load('target2.png'),
    pygame.image.load('target3.png'),
    pygame.image.load('target4.png'),
    pygame.image.load('target5.png'),
    pygame.image.load('target6.png')
]

for i in range(len(target_images)):
    target_images[i] = pygame.transform.scale(target_images[i], (50, 50))

# Load sounds
gunshot_sound = pygame.mixer.Sound('gunshot.wav')
hit_sound = pygame.mixer.Sound('hit.wav')

# Load background music
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)  # Play music in a loop

# Gun settings
gun_x = width // 2
gun_y = height - 60
gun_speed = 10

# Target settings
targets = []
for _ in range(3):  # Initially, 3 targets
    img = random.choice(target_images)
    targets.append([img, random.randint(0, width - 50), random.randint(0, height // 2 - 50)])

# Bullet settings
bullet_speed = 20
bullets = []

# Game variables
run = True
score = 0
font = pygame.font.SysFont(None, 55)
can_shoot = True

def draw_window():
    win.blit(background_img, (0, 0))  # Draw the background image
    win.blit(gun_img, (gun_x, gun_y))
    
    for target_img, target_x, target_y in targets:
        win.blit(target_img, (target_x, target_y))
    
    for bullet in bullets:
        win.blit(bullet_img, (bullet[0], bullet[1]))
    
    score_text = font.render(f"Score: {score}", True, red)
    win.blit(score_text, [10, 10])
    
    # Draw buttons
    win.blit(left_arrow_img, (50, height - 70))
    win.blit(right_arrow_img, (150, height - 70))
    win.blit(fire_button_img, (width - 100, height - 70))
    
    pygame.display.update()

def handle_bullets():
    global score
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)
        for target in targets[:]:
            target_img, target_x, target_y = target
            if target_x < bullet[0] < target_x + 50 and target_y < bullet[1] < target_y + 50:
                score += 1
                hit_sound.play()
                bullets.remove(bullet)
                targets.remove(target)
                img = random.choice(target_images)
                targets.append([img, random.randint(0, width - 50), random.randint(0, height // 2 - 50)])
                break

def is_over(pos, x, y, w, h):
    return x < pos[0] < x + w and y < pos[1] < y + h

# Main loop
while run:
    pygame.time.delay(50)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if is_over(mouse_pos, 50, height - 70, 50, 50):
                gun_x -= gun_speed
            if is_over(mouse_pos, 150, height - 70, 50, 50):
                gun_x += gun_speed
            if is_over(mouse_pos, width - 100, height - 70, 50, 50) and can_shoot:
                gunshot_sound.play()
                bullets.append([gun_x + 20, gun_y])
                can_shoot = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and gun_x - gun_speed > 0:
        gun_x -= gun_speed
    if keys[pygame.K_RIGHT] and gun_x + gun_speed < width - 50:
        gun_x += gun_speed
    if keys[pygame.K_SPACE] and can_shoot:
        gunshot_sound.play()
        bullets.append([gun_x + 20, gun_y])
        can_shoot = False  # Prevent multiple bullets being fired at once

    if not keys[pygame.K_SPACE]:
        can_shoot = True  # Allow shooting again once SPACE is released
        
    handle_bullets()
    
    draw_window()

pygame.quit()
