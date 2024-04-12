import os
import pygame
import random


# Determine the base path to use for asset loading
base_path = os.path.dirname(__file__)  # Gets the directory where the script is located
asset_path = os.path.join(base_path, 'assets')

# Initialize Pygame
pygame.init()

# Screen setup
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))


# Background image
background_image = pygame.image.load(os.path.join(asset_path, "stars-bg.png")).convert()
background_image = pygame.transform.scale(
    background_image, (screen_width, screen_height)
)  # Scale it to your screen size

# Colors
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLUE = (0, 128, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

# FPS
clock = pygame.time.Clock()
fps = 60

# Score initialization
score = 0
font = pygame.font.SysFont(None, 36)  # Choose an appropriate font and size

# Health initialization
health = 3

# Spaceship spritesheet
spaceship_spritesheet_image = pygame.image.load(
    os.path.join(asset_path, "spaceship.png")
).convert_alpha()  # Use the correct path to your spritesheet file
# Assuming there are 3 frames in the spritesheet
spaceship_frame_width = spaceship_spritesheet_image.get_width() // 5
spaceship_frame_height = spaceship_spritesheet_image.get_height()
spaceship_frames = [
    spaceship_spritesheet_image.subsurface(
        pygame.Rect(
            i * spaceship_frame_width, 0, spaceship_frame_width, spaceship_frame_height
        )
    )
    for i in range(5)
]
# Scale the frames to your desired size
spaceship_frames = [
    pygame.transform.scale(
        frame, (spaceship_frame_width / 2, spaceship_frame_height / 2)
    )
    for frame in spaceship_frames
]

# Load the bullet spritesheet
bullet_spritesheet_image = pygame.image.load(
    os.path.join(asset_path, "bullet.png")
).convert_alpha()  # Make sure to provide the correct path to the image file
# Assume there are 4 frames in the spritesheet
bullet_frame_width = bullet_spritesheet_image.get_width() // 3
bullet_frame_height = bullet_spritesheet_image.get_height()
bullet_frames = [
    bullet_spritesheet_image.subsurface(
        pygame.Rect(i * bullet_frame_width, 0, bullet_frame_width, bullet_frame_height)
    )
    for i in range(3)
]
# Scale the frames to your desired size
bullet_frames = [
    pygame.transform.scale(frame, (bullet_frame_width / 8, bullet_frame_height / 8))
    for frame in bullet_frames
]

# Load enemy spritesheets
enemy_flyer_spritesheet = pygame.image.load(os.path.join(asset_path, "enemy-flyer.png")).convert_alpha()
enemy_seeker_spritesheet = pygame.image.load(os.path.join(asset_path, "enemy-seeker.png")).convert_alpha()
# Assuming there are multiple frames for each enemy type in the spritesheet
# Calculate the frame width for each spritesheet based on your known number of frames
flyer_frame_width = (
    enemy_flyer_spritesheet.get_width() // 4
)  # Replace number_of_frames_flyer with the correct number of frames
seeker_frame_width = (
    enemy_seeker_spritesheet.get_width() // 4
)  # Replace number_of_frames_seeker with the correct number of frames
# Slice into frames
enemy_flyer_frames = [
    enemy_flyer_spritesheet.subsurface(
        pygame.Rect(
            i * flyer_frame_width,
            0,
            flyer_frame_width,
            enemy_flyer_spritesheet.get_height(),
        )
    )
    for i in range(4)
]
enemy_seeker_frames = [
    enemy_seeker_spritesheet.subsurface(
        pygame.Rect(
            i * seeker_frame_width,
            0,
            seeker_frame_width,
            enemy_seeker_spritesheet.get_height(),
        )
    )
    for i in range(4)
]
# rotate the seeker frames
enemy_seeker_frames = [
    pygame.transform.rotate(frame, -90) for frame in enemy_seeker_frames
]

# Load the explosion spritesheet
explosion_spritesheet = pygame.image.load(os.path.join(asset_path, "explosion.png")).convert_alpha()
# Assuming the spritesheet is a grid of equal-sized frames
explosion_frames = []
explosion_frame_width = explosion_spritesheet.get_width() // 6
explosion_frame_height = explosion_spritesheet.get_height() // 6
for row in range(6):
    for col in range(6):
        frame = explosion_spritesheet.subsurface(
            (
                col * explosion_frame_width,
                row * explosion_frame_height,
                explosion_frame_width,
                explosion_frame_height,
            )
        )
        explosion_frames.append(frame)

# Load game over and win message images
game_over_image = pygame.image.load(os.path.join(asset_path, "message-lose.png")).convert_alpha()
game_over_image_rect = game_over_image.get_rect(
    center=(screen_width // 2, screen_height // 2)
)
win_image = pygame.image.load(os.path.join(asset_path, "message-win.png")).convert_alpha()
win_image_rect = win_image.get_rect(center=(screen_width // 2, screen_height // 2))

# Load the final round message image
final_round_image = pygame.image.load(
    os.path.join(asset_path, "final-round.png")
).convert_alpha()  # Adjust path as needed
final_round_image_rect = final_round_image.get_rect(
    center=(screen_width // 2, screen_height // 2)
)

# Define game states
GAME_ACTIVE = 0
GAME_OVER = 1
GAME_WIN = 2
GAME_FINAL_ROUND = 3

# Start with the game in the active state
game_state = GAME_ACTIVE

# Load sounds
explosion_sound = pygame.mixer.Sound(
    os.path.join(asset_path, "explosion_sound.mp3")
)  # Replace with the path to your explosion sound
game_win_sound = pygame.mixer.Sound(
    os.path.join(asset_path, "game_win_sound.mp3")
)  # Replace with the path to your win sound
game_lose_sound = pygame.mixer.Sound(
    os.path.join(asset_path, "game_lose_sound.mp3")
)  # Replace with the path to your lose sound
# Load and play background music
pygame.mixer.music.load(
    os.path.join(asset_path, "background_music.mp3")
)  # Replace with the path to your background music
pygame.mixer.music.play(loops=-1)  # Play music continuously


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.frames = spaceship_frames  # Frames sliced from the spritesheet
        self.current_frame = 1  # Start with the middle frame
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=(screen_width / 2, screen_height - 50))
        self.speed = 5
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100  # Milliseconds between frames

    def update(self, keys_pressed):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

        if keys_pressed[pygame.K_LEFT] and self.rect.left > 0:
            self.current_frame = 1  # Tilt left frame
            self.rect.x -= self.speed
        elif keys_pressed[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.current_frame = 3  # Tilt right frame
            self.rect.x += self.speed
        else:
            self.current_frame = 2  # Middle frame

        self.image = self.frames[self.current_frame]  # Update the image

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullets.add(bullet)


# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Bullet, self).__init__()
        self.frames = bullet_frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=(x, y))
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  # Adjust frame rate as needed

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

        self.rect.y -= 10
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super(Explosion, self).__init__()
        self.frames = explosion_frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=center)
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  # Time between frames in milliseconds

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame == len(self.frames):
                self.kill()
            else:
                self.image = self.frames[self.current_frame]


# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, advanced_movement=False):
        super(Enemy, self).__init__()
        self.type = enemy_type
        self.advanced_movement = advanced_movement
        if self.type == "flyer":
            self.frames = enemy_flyer_frames
            self.speed = 2
            self.score_value = 1
        elif self.type == "seeker":
            self.frames = enemy_seeker_frames
            self.speed = 5
            self.score_value = 5

        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(
            center=(random.randint(20, screen_width - 20), -50)
        )
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100  # Adjust frame rate as needed for animation

        # New attributes for advanced movement
        self.x_speed = random.choice([-1, 1]) * self.speed
        self.y_speed = self.speed

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

        # Check if advanced movement is enabled
        if self.advanced_movement:
            self.rect.x += self.x_speed
            self.rect.y += self.y_speed

            # Bounce off the walls
            if self.rect.left <= 0 or self.rect.right >= screen_width:
                self.x_speed *= -1
        else:
            self.rect.y += self.speed

        # Check if the enemy has left the screen
        if self.rect.top > screen_height:
            self.kill()


# Sprite groups
player = Player()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
explosions = pygame.sprite.Group()

# Enemy spawn event
ENEMY_SPAWN = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMY_SPAWN, 2000)
advanced_movement = False

# Game loop
running = True
final_round_displayed = (
    False  # Flag to indicate if the final round message was displayed
)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state in [GAME_OVER, GAME_WIN, GAME_FINAL_ROUND]:
                    # Restart the game if it's over or won
                    health = 3
                    score = 0
                    enemies.empty()
                    bullets.empty()
                    explosions.empty()
                    advanced_movement = False  # Reset advanced movement
                    final_round_displayed = False  # Reset the final round message flag
                    game_state = GAME_ACTIVE
                    pygame.mixer.music.play(loops=-1)  # Play music continuously
                elif game_state == GAME_ACTIVE:
                    player.shoot()
        elif event.type == ENEMY_SPAWN and game_state == GAME_ACTIVE:
            enemy_type = random.choice(["flyer", "seeker"])
            enemy = Enemy(enemy_type, advanced_movement)
            enemies.add(enemy)
            all_sprites.add(enemy)

    if game_state == GAME_ACTIVE:
        # Update
        keys_pressed = pygame.key.get_pressed()
        player.update(keys_pressed)
        bullets.update()
        enemies.update()
        explosions.update()

        # Collision detection
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            explosion_sound.play()  # Play explosion sound
            explosion = Explosion(hit.rect.center)
            explosions.add(explosion)
            score += (
                hit.score_value
            )  # Add the enemy's score value to the player's score
        # Displaying the score
        score_text = font.render(f"Score: {score}", True, GREY)

        # Inside your game loop, check for player-enemy collisions
        player_hits = pygame.sprite.spritecollide(
            player, enemies, True
        )  # The True argument makes the enemies disappear on collision
        for hit in player_hits:
            explosion_sound.play()  # Play explosion sound
            explosion = Explosion(hit.rect.center)
            explosions.add(explosion)
            health -= 1  # Decrease health by 1
        # Displaying health
        health_text = font.render(f"Health: {health}", True, GREY)

        # Draw / render
        screen.blit(background_image, (0, 0))
        bullets.draw(screen)
        enemies.draw(screen)
        explosions.draw(screen)
        all_sprites.draw(screen)
        screen.blit(score_text, (10, 10))  # Position it at top left
        screen.blit(
            health_text, (screen_width - health_text.get_width() - 10, 10)
        )  # Position it at top right

        if score >= 20 and not final_round_displayed:
            game_state = GAME_FINAL_ROUND

        if health <= 0:
            game_state = GAME_OVER
            pygame.mixer.music.stop()
            game_lose_sound.play()
        elif score >= 50:
            game_state = GAME_WIN
            pygame.mixer.music.stop()
            game_win_sound.play()

    elif game_state == GAME_FINAL_ROUND:
        if not final_round_displayed:
            # Show the final round message and pause before starting the final round
            screen.blit(final_round_image, final_round_image_rect)
            pygame.display.flip()
            pygame.time.wait(3000)  # Wait for 3 seconds
            final_round_displayed = True
            advanced_movement = True  # Enable advanced movement for enemies
            game_state = GAME_ACTIVE  # Proceed to final round
            for enemy in enemies:  # Increase the speed of all enemies
                enemy.speed += 2  # Adjust this value as needed for your game
                enemy.advanced_movement = advanced_movement

    elif game_state == GAME_OVER:
        # Draw game over message
        screen.blit(game_over_image, game_over_image_rect)

    elif game_state == GAME_WIN:
        # Draw win message
        screen.blit(win_image, win_image_rect)

    # Update the display
    pygame.display.flip()
    # Cap FPS
    clock.tick(fps)

pygame.quit()
