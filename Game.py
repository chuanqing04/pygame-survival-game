from random import randint
from PIL import Image

import pygame
import sys
import random
import math
import time

pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
MAP_WIDTH, MAP_HEIGHT = 2100, 2100  # The total size of the map
ZOOM_FACTOR = 0.8  # Smaller value = more zoomed out
BASE_SCREEN_WIDTH, BASE_SCREEN_HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT
current_viewport_width = SCREEN_WIDTH
current_viewport_height = SCREEN_HEIGHT

ATTACK_COOLDOWN = 500  # 0.5 seconds in milliseconds
PLAYER_INVULNERABLE = 1000  # 1 second invulnerability after hit
HEALTH = 5
SPEED = 5
ENEMY_LIMIT = 0
KNOCKBACK = 10
RECOVERYAMOUNT = 1
WATER = 0
ZOMBIEHEALTH = 20
HEALTHPERWAVE = 0

SAMURAI2_SCALE = 1.2
sskill_scale = 1.4
double_scale = 2.0
charging_scale = 2.5
transform_scale = 3.0
skill_scale = 1.2
star_scale = 5.0
normal_scale = 1.0


# ---------------------------------------------------------------------------------------------------------------------------------
# Load Assets
# Load scaled Images
def load_scaled_images(path_list, scale_factor):
    scaled_images = []
    for path in path_list:
        img = pygame.image.load(path)  # Load the image once
        width = int(img.get_width() * scale_factor)
        height = int(img.get_height() * scale_factor)
        scaled_images.append(pygame.transform.scale(img, (width, height)))
    return scaled_images


# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Survive the Onslaught")

# Load assets
background1 = pygame.image.load("Assets\\Map\\forest.jpg")  # relative file path
background1 = pygame.transform.scale(background1, (2100, 2100))
background2 = pygame.image.load("Assets\\Map\\withered forest.png")
background2 = pygame.transform.scale(background2, (2100, 2100))

# Help Tips
helptips = pygame.image.load("Assets\\Help Tips.png")
helptips = pygame.transform.scale(helptips, (SCREEN_WIDTH, SCREEN_HEIGHT))
menu = pygame.image.load("Assets\\Menu.png")
menu = pygame.transform.scale(menu, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Player animations
main1idle = [pygame.image.load(f"Assets\\Samurai\\Idle\\{i}.png") for i in range(0, 1)]
main1walk = [pygame.image.load(f"Assets\\Samurai\\run\\{i}.png") for i in range(0, 7)]
main1attack1 = [pygame.image.load(f"Assets\\Samurai\\Attack 1\\{i}.png") for i in range(0, 5)]
main1attack2 = [pygame.image.load(f"Assets\\Samurai\\Attack 2\\{i}.png") for i in range(0, 3)]
main1attack3 = [pygame.image.load(f"Assets\\Samurai\\Attack 3\\{i}.png") for i in range(0, 2)]
main1hurt = [pygame.image.load(f"Assets\\Samurai\\Hurt\\{i}.png") for i in range(0, 1)]
main1dead = [pygame.image.load(f"Assets\\Samurai\\Dead\\{i}.png") for i in range(0, 3)]

# Zombie Type 1 animations
zombie1idle = [pygame.image.load(f"Assets\\Zombie1\\Idle\\{i}.png") for i in range(0, 7)]
zombie1walk = [pygame.image.load(f"Assets\\Zombie1\\Walk\\{i}.png") for i in range(0, 7)]
zombie1attack = [pygame.image.load(f"Assets\\Zombie1\\Attack\\{i}.png") for i in range(0, 5)]
zombie1hurt = [pygame.image.load(f"Assets\\Zombie1\\Hurt\\{i}.png") for i in range(0, 5)]
zombie1dead = [pygame.image.load(f"Assets\\Zombie1\\Dead\\{i}.png") for i in range(0, 6)]

# Zombie Type 2 animations
zombie2idle = [pygame.image.load(f"Assets\\Zombie2\\Idle\\{i}.png") for i in range(0, 7)]
zombie2walk = [pygame.image.load(f"Assets\\Zombie2\\Walk\\{i}.png") for i in range(0, 7)]
zombie2attack = [pygame.image.load(f"Assets\\Zombie2\\Attack\\{i}.png") for i in range(0, 6)]
zombie2hurt = [pygame.image.load(f"Assets\\Zombie2\\Hurt\\{i}.png") for i in range(0, 5)]
zombie2dead = [pygame.image.load(f"Assets\\Zombie2\\Dead\\{i}.png") for i in range(0, 7)]

# Samurai2 Animations (scaled)
samuraiidle = load_scaled_images([f"Assets\\Samurai2\\Idle\\Idle.png"], SAMURAI2_SCALE)
samuraiattack1 = load_scaled_images([f"Assets\\Samurai2\\Attack1\\SAttack{i}.png" for i in range(1, 5)], SAMURAI2_SCALE)
samuraiattack2 = load_scaled_images([f"Assets\\Samurai2\\Attack2\\S2Attack{i}.png" for i in range(1, 7)],
                                    SAMURAI2_SCALE)
samuraiulti = load_scaled_images([f"Assets\\Samurai2\\Ulti\\Ulti{i}.png" for i in range(1, 4)], SAMURAI2_SCALE)
samuraidead = load_scaled_images([f"Assets\\Samurai2\\Dead\\SDead{i}.png" for i in range(1, 6)], SAMURAI2_SCALE)
samuraihurt = load_scaled_images([f"Assets\\Samurai2\\Hurt\\SHurt{i}.png" for i in range(1, 3)], SAMURAI2_SCALE)
samurairun = load_scaled_images([f"Assets\\Samurai2\\Run\\SRun{i}.png" for i in range(1, 6)], SAMURAI2_SCALE)
samuraiskill = load_scaled_images([f"Assets\\Samurai2\\Skill\\SSkill{i}.png" for i in range(1, 16)], sskill_scale)

bossidle = load_scaled_images([f"Assets\\Boss\\Idle\\Idle.png"], SAMURAI2_SCALE)
bossdead = load_scaled_images([f"Assets\\Boss\\Dead\\VDeath{i}.png" for i in range(1, 8)], SAMURAI2_SCALE)
bossskill = load_scaled_images([f"Assets\\Boss\\Skill\\Skill{i}.png" for i in range(1, 6)], SAMURAI2_SCALE)
bosswalk = load_scaled_images([f"Assets\\Boss\\Walk\\VWalk{i}.png" for i in range(1, 8)], SAMURAI2_SCALE)
bosshurt = load_scaled_images([f"Assets\\Boss\\Hurt\\VHurt{i}.png" for i in range(1, 3)], SAMURAI2_SCALE)
bossattack = load_scaled_images([f"Assets\\Boss\\Attack\\VAttack{i}.png" for i in range(1, 7)], SAMURAI2_SCALE)

fire = load_scaled_images([f"Assets\\Effect\\Fire\\Fire{i}.png" for i in range(1, 10)], charging_scale)
transform = load_scaled_images([f"Assets\\Effect\\Transform\\Transform{i}.png" for i in range(1, 16)], transform_scale)
lightning = load_scaled_images([f"Assets\\Effect\\Lightning\\Lightning{i}.png" for i in range(1, 26)], transform_scale)
chargingskill = load_scaled_images([f"Assets\\Effect\\Lightning\\Lightning{i}.png" for i in range(1, 26)],
                                   charging_scale)
main1skill1 = load_scaled_images([f"Assets\\Samurai\\Skill1\\Skill{i}.png" for i in range(1, 4)], SAMURAI2_SCALE)
main1skill2 = load_scaled_images([f"Assets\\Samurai\\Skill2\\2Skill{i}.png" for i in range(1, 7)], skill_scale)
explodingskill = load_scaled_images([f"Assets\\Effect\\Explode\\Explode{i}.png" for i in range(1, 6)], SAMURAI2_SCALE)
waterexplodingskill = load_scaled_images([f"Assets\\Effect\\WaterExplode\\Water{i}.png" for i in range(1, 5)],
                                         SAMURAI2_SCALE)
waterskill = load_scaled_images([f"Assets\\Effect\\Water\\Water{i}.png" for i in range(1, 4)], SAMURAI2_SCALE)
waterfallskill = load_scaled_images([f"Assets\\Effect\\Waterfall\\Waterfall{i}.png" for i in range(1, 4)],
                                    SAMURAI2_SCALE)
slashskill = load_scaled_images([f"Assets\\Effect\\Slice\\Slice{i}.png" for i in range(1, 3)], charging_scale)
fireskill1 = load_scaled_images([f"Assets\\Effect\\Fire2\\Fire{i}.png" for i in range(1, 4)], SAMURAI2_SCALE)
fireskill2 = load_scaled_images([f"Assets\\Effect\\Fire3\\Fire{i}.png" for i in range(1, 6)], SAMURAI2_SCALE)
starskill = load_scaled_images([f"Assets\\Effect\\Stars\\Stars{i}.png" for i in range(1, 5)], charging_scale)

# Musics and sounds
mainmenumusic = pygame.mixer.Sound(f"Assets\\MusicSoundEffect\\MainMenuMusic.mp3")
gamemusic = pygame.mixer.Sound(f"Assets\\MusicSoundEffect\\InGameMusic.mp3")
slashsound = pygame.mixer.Sound(f"Assets\\MusicSoundEffect\\SlashSound.mp3")
survivedsound = pygame.mixer.Sound(f"Assets\\MusicSoundEffect\\SurvivedSound.mp3")
zombieattacksound = pygame.mixer.Sound(f"Assets\\MusicSoundEffect\\ZombieAttack.mp3")
zombiedead1sound = pygame.mixer.Sound(f"Assets\\MusicSoundEffect\\ZombieDead1.mp3")
zombiedead2sound = pygame.mixer.Sound(f"Assets\\MusicSoundEffect\\ZombieDead2.mp3")
potionsound = pygame.mixer.Sound(f"Assets\\MusicSoundEffect\\PotionSound.mp3")
lasersound = pygame.mixer.Sound(f"Assets/MusicSoundEffect/LaserSound.mp3")
transformsound = pygame.mixer.Sound(f"Assets\\MusicSoundEffect\\TransformSound.mp3")
dashattacksound = pygame.mixer.Sound(f"Assets\\MusicSoundEffect\\DashAttackSound.mp3")
comboattacksound = pygame.mixer.Sound(f"Assets\\MusicSoundEffect\\ComboAttackSound.mp3")
fireballsound = pygame.mixer.Sound(f"Assets\\MusicSoundEffect\\FireballSound.mp3")
gameovermusic = pygame.mixer.Sound(f"Assets\\MusicSoundEffect\\GameOverMusic.mp3")
victorymusic = pygame.mixer.Sound(f"Assets\\MusicSoundEffect\\VictoryMusic.mp3")
bossmusic = pygame.mixer.Sound(f"Assets\\MusicSoundEffect\\BossMusic.mp3")
playerdeadsound = pygame.mixer.Sound(f"Assets\\MusicSoundEffect\\PlayerDeadSound.mp3")
selectionsound = pygame.mixer.Sound(f"Assets\\MusicSoundEffect\\SelectionSound.mp3")
bossattacksound1 = pygame.mixer.Sound(f"Assets\\MusicSoundEffect\\BossAttackSound1.mp3")
bossattacksound2 = pygame.mixer.Sound(f"Assets\\MusicSoundEffect\\BossAttackSound2.mp3")
bossskillsound = pygame.mixer.Sound(f"Assets\\MusicSoundEffect\\BossSkillSound.mp3")
bossdeadsound = pygame.mixer.Sound(f"Assets\\MusicSoundEffect\\BossDeadSound.mp3")
dialogmusic1 = pygame.mixer.Sound(f"Assets\\MusicSoundEffect\\Dialogue music.mp3")
playerhitsound = pygame.mixer.Sound(f"Assets\\MusicSoundEffect\\PlayerHitSound.mp3")
revertsound = pygame.mixer.Sound(f"Assets\\MusicSoundEffect\\RevertSound.mp3")

# Camera variables (for scrolling)
camera_x, camera_y = 0, 0


# -----------------------------------------------------------------------------------------------------------------------------------
# Special Effects
def create_heart_surface(width, height):
    # Create a transparent surface for the heart
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    border_thickness = 2

    # Calculate radii and centers for the two top circles
    radius = width // 4
    center1 = (radius, radius)
    center2 = (width - radius, radius)

    # Draw the black border for the circles
    pygame.draw.circle(surface, (0, 0, 0), center1, radius)
    pygame.draw.circle(surface, (0, 0, 0), center2, radius)
    # Draw the inner red circles (shrunken by the border thickness)
    pygame.draw.circle(surface, (255, 0, 0), center1, radius - border_thickness)
    pygame.draw.circle(surface, (255, 0, 0), center2, radius - border_thickness)

    # Define the bottom (triangle) points for the heart border
    points = [(0, radius), (width, radius), (width // 2, height)]
    pygame.draw.polygon(surface, (0, 0, 0), points)
    # Define inner points for the red part (inset by border_thickness)
    inner_points = [(border_thickness, radius),
                    (width - border_thickness, radius),
                    (width // 2, height - border_thickness)]
    pygame.draw.polygon(surface, (255, 0, 0), inner_points)
    return surface


class HeartEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, duration=1000):
        super().__init__()
        self.duration = duration  # Total duration in milliseconds
        self.start_time = pygame.time.get_ticks()
        # Create the heart surface with a black border
        self.image = create_heart_surface(30, 30)
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity_y = -1  # Floats upward

    def update(self):
        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed >= self.duration:
            self.kill()
            return
        # Fade out linearly over the duration
        alpha = int(255 * (1 - elapsed / self.duration))
        self.image = self.original_image.copy()
        self.image.set_alpha(alpha)
        # Move the heart upward
        self.rect.y += self.velocity_y


# Skill Potions
class Potion(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.original_image = pygame.image.load(image_path)
        self.original_image = pygame.transform.scale(self.original_image, (75, 75))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(x, y))

        # Floating animation variables
        self.float_offset = 0  # Up/down offset
        self.float_speed = 0.001  # Speed of floating effect
        self.float_range = 10  # Max vertical movement range
        self.start_y = y

        # Particle effect
        self.particles = []  # Store particles

    def update(self):
        # **1. Floating Animation**
        self.float_offset = math.sin(pygame.time.get_ticks() * self.float_speed) * self.float_range
        self.rect.y = self.start_y + self.float_offset

        # **2. Add Particle Effect**
        self.add_particles()
        self.update_particles()

    def draw(self, screen, camera_x, camera_y):
        # **Correct Shadow Placement**
        shadow_x = self.rect.centerx - camera_x
        shadow_y = self.rect.bottom - camera_y + 10  # Move shadow slightly below the potion

        # Create semi-transparent shadow
        shadow_surface = pygame.Surface((50, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 100), (0, 0, 50, 20))

        # **Blit shadow slightly below the potion**
        screen.blit(shadow_surface, (shadow_x - 25, shadow_y))

        # **Draw Potion**
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

        # **Draw Particles**
        for particle in self.particles:
            pygame.draw.circle(screen, (255, 255, 150, particle["alpha"]),
                               (particle["x"] - camera_x, particle["y"] - camera_y), particle["radius"])

    def add_particles(self):
        if random.randint(0, 10) == 0:  # Control particle spawn rate
            self.particles.append({
                "x": self.rect.centerx + random.randint(-10, 10),
                "y": self.rect.y + random.randint(-5, 5),
                "radius": random.randint(2, 4),
                "alpha": 255,  # Full opacity initially
                "speed": random.uniform(0.3, 0.8)
            })

    def update_particles(self):
        for particle in self.particles:
            particle["y"] -= particle["speed"]  # Move upward
            particle["alpha"] -= 5  # Fade out
        self.particles = [p for p in self.particles if p["alpha"] > 0]  # Remove faded particles


class BloodSplashEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, duration=500):
        super().__init__()
        self.duration = duration  # Effect duration in milliseconds
        self.start_time = pygame.time.get_ticks()
        # Create a small surface for the blood splash effect
        size = 100  # Adjust size as needed
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        # Draw several red circles to simulate blood splatter
        for i in range(5):
            pos = (random.randint(0, size), random.randint(0, size))
            radius = random.randint(2, 6)
            # Use a darker red for blood
            pygame.draw.circle(self.image, (139, 0, 0, 255), pos, radius)
        # Save the original image for fading calculations
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed >= self.duration:
            self.kill()
            return
        # Fade out over time
        alpha = int(255 * (1 - elapsed / self.duration))
        self.image = self.original_image.copy()
        self.image.set_alpha(alpha)


class TransformationEffect(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = transform
        self.current_image_index = 0
        self.image = self.images[self.current_image_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 8  # Adjust animation speed as needed
        self.counter = 0
        self.done = False
        self.damage = 0

    def update(self):
        self.counter += 1
        if self.counter % self.animation_speed == 0:
            self.current_image_index += 1
            if self.current_image_index >= len(self.images):
                self.done = True
                self.kill()
            else:
                self.image = self.images[self.current_image_index]


active_transition_effect = None


class ChargingEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, duration):
        super().__init__()
        self.images = chargingskill
        self.current_image_index = 0
        self.image = self.images[self.current_image_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 5
        self.counter = 0
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            self.kill()
            return
        self.counter += 1
        if self.counter % self.animation_speed == 0:
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
            self.image = self.images[self.current_image_index]


class SwordFireEffect(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = fire  # Use existing fire animation frames
        self.current_image_index = 0
        self.image = self.images[self.current_image_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 5
        self.counter = 0
        self.damage = 10
        self.last_damage_time = 0
        self.damage_interval = 200  # Damage every 200ms
        self.damaged_bosses = set()  # Add this line

    def update(self):
        self.counter += 1
        if self.counter % self.animation_speed == 0:
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
            self.image = self.images[self.current_image_index]

        # Damage zombies in contact with the fire effect
        current_time = pygame.time.get_ticks()
        if current_time - self.last_damage_time >= self.damage_interval:
            for zombie in zombies:
                if pygame.sprite.collide_rect(self, zombie):
                    zombie.take_damage(self.damage)
            self.last_damage_time = current_time


class WaterExplosionEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, facing_right):
        super().__init__()
        self.images = [pygame.transform.flip(img, True, False) for img in
                       waterexplodingskill] if not facing_right else waterexplodingskill
        self.current_image_index = 0
        self.image = self.images[self.current_image_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 10
        self.counter = 0
        self.damage = 10
        self.damaged_zombies = set()
        self.damaged_bosses = set()  # Add this line

    def update(self):
        self.counter += 1
        if self.counter % self.animation_speed == 0:
            self.current_image_index += 1
            if self.current_image_index >= len(self.images):
                self.kill()  # Remove effect when animation completes
            else:
                self.image = self.images[self.current_image_index]

        if self.current_image_index == 2:
            for zombie in zombies:
                if pygame.sprite.collide_rect(self, zombie) and zombie not in self.damaged_zombies:
                    zombie.take_damage(self.damage)
                    self.damaged_zombies.add(zombie)
            for boss in bosses:
                if pygame.sprite.collide_rect(self, boss) and boss not in self.damaged_bosses:
                    boss.take_damage(self.damage / 2)
                    self.damaged_bosses.add(boss)


class ExplosionEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, facing_right):
        super().__init__()
        self.images = [pygame.transform.flip(img, True, False) for img in
                       explodingskill] if not facing_right else explodingskill
        self.current_image_index = 0
        self.image = self.images[self.current_image_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 10
        self.counter = 0
        self.damage = 5
        self.damaged_zombies = set()
        self.damaged_bosses = set()  # Add this line
        self.last_damage_time = 0
        self.damage_interval = 200  # Damage every 200ms

    def update(self):
        self.counter += 1
        if self.counter % self.animation_speed == 0:
            self.current_image_index += 1
            if self.current_image_index >= len(self.images):
                self.kill()  # Remove effect when animation completes
            else:
                self.image = self.images[self.current_image_index]

        if self.current_image_index == 2:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_damage_time >= self.damage_interval:
                for zombie in zombies:
                    if pygame.sprite.collide_rect(self, zombie):
                        zombie.take_damage(self.damage)
                self.last_damage_time = current_time


class WaterEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, facing_right):
        super().__init__()
        self.images = [pygame.transform.flip(img, True, False) for img in
                       waterskill] if not facing_right else waterskill
        self.current_image_index = 0
        self.image = self.images[self.current_image_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 10
        self.counter = 0
        self.damage = 5
        self.damaged_zombies = set()
        self.damaged_bosses = set()  # Add this line

    def update(self):
        self.counter += 1
        if self.counter % self.animation_speed == 0:
            self.current_image_index += 1
            if self.current_image_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.current_image_index]
                # Update rect to keep centered
                self.rect = self.image.get_rect(center=self.rect.center)

        # Damage zombies in contact
        for zombie in zombies:
            if pygame.sprite.collide_rect(self, zombie) and zombie not in self.damaged_zombies:
                zombie.take_damage(self.damage)
                self.damaged_zombies.add(zombie)


class WaterfallEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, facing_right):
        super().__init__()
        self.images = [pygame.transform.flip(img, True, False) for img in
                       waterfallskill] if not facing_right else waterfallskill
        self.current_image_index = 0
        self.image = self.images[self.current_image_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 10
        self.counter = 0
        self.damage = 5
        self.damaged_zombies = set()
        self.damaged_bosses = set()  # Add this line

    def update(self):
        self.counter += 1
        if self.counter % self.animation_speed == 0:
            self.current_image_index += 1
            if self.current_image_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.current_image_index]
                # Update rect to keep centered
                self.rect = self.image.get_rect(center=self.rect.center)

        # Damage zombies in contact
        for zombie in zombies:
            if pygame.sprite.collide_rect(self, zombie) and zombie not in self.damaged_zombies:
                zombie.take_damage(self.damage)
                self.damaged_zombies.add(zombie)


class SliceEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, facing_right):
        super().__init__()
        self.images = slashskill
        if not facing_right:
            self.images = [pygame.transform.flip(img, True, False) for img in slashskill]
        self.current_image_index = 0
        self.image = self.images[self.current_image_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 10
        self.counter = 0
        self.damage = 3
        self.damaged_zombies = set()
        self.damaged_bosses = set()  # Add this line
        self.last_damage_time = 0
        self.damage_interval = 200  # Damage every 200ms
        self.pushed_entities = set()  # Track pushed enemies
        self.facing_right = facing_right  # Store facing direction

    def update(self):
        self.counter += 1
        if self.counter % self.animation_speed == 0:
            self.current_image_index += 1
            if self.current_image_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.current_image_index]
        current_time = pygame.time.get_ticks()
        if current_time - self.last_damage_time >= self.damage_interval:
            for zombie in zombies:
                if pygame.sprite.collide_rect(self, zombie) and zombie not in self.pushed_entities:
                    # Push zombie
                    if self.facing_right:
                        zombie.rect.x += 250
                    else:
                        zombie.rect.x -= 250
                    self.pushed_entities.add(zombie)
            self.last_damage_time = current_time
            for boss in bosses:
                if pygame.sprite.collide_rect(self, boss) and boss not in self.pushed_entities:
                    # Push boss
                    if self.facing_right:
                        boss.rect.x += 125
                    else:
                        boss.rect.x -= 125
                    self.pushed_entities.add(boss)


class Fire2Effect(pygame.sprite.Sprite):
    def __init__(self, x, y, facing_right):
        super().__init__()
        self.images = fireskill1
        if not facing_right:
            self.images = [pygame.transform.flip(img, True, False) for img in fireskill1]
        self.current_image_index = 0
        self.image = self.images[self.current_image_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 10
        self.counter = 0
        self.damage = 8
        self.damaged_zombies = set()
        self.damaged_bosses = set()  # Add this line
        self.last_damage_time = 0
        self.damage_interval = 200  # Damage every 200ms

    def update(self):
        self.counter += 1
        if self.counter % self.animation_speed == 0:
            self.current_image_index += 1
            if self.current_image_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.current_image_index]
        current_time = pygame.time.get_ticks()
        if current_time - self.last_damage_time >= self.damage_interval:
            for zombie in zombies:
                if pygame.sprite.collide_rect(self, zombie):
                    zombie.take_damage(self.damage)
            self.last_damage_time = current_time


class Fire3Effect(pygame.sprite.Sprite):
    def __init__(self, x, y, facing_right):
        super().__init__()
        self.images = fireskill2
        if not facing_right:
            self.images = [pygame.transform.flip(img, True, False) for img in fireskill2]
        self.current_image_index = 0
        self.image = self.images[self.current_image_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 10
        self.counter = 0
        self.damage = 8
        self.damaged_zombies = set()
        self.damaged_bosses = set()  # Add this line
        self.last_damage_time = 0
        self.damage_interval = 200  # Damage every 200ms

    def update(self):
        self.counter += 1
        if self.counter % self.animation_speed == 0:
            self.current_image_index += 1
            if self.current_image_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.current_image_index]
        current_time = pygame.time.get_ticks()
        if current_time - self.last_damage_time >= self.damage_interval:
            for zombie in zombies:
                if pygame.sprite.collide_rect(self, zombie):
                    zombie.take_damage(self.damage)
            self.last_damage_time = current_time


class StarEffect(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = starskill
        self.current_image_index = 0
        self.image = self.images[self.current_image_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 5
        self.counter = 0
        self.damage = 1  # Damage per tick
        self.start_time = pygame.time.get_ticks()
        self.duration = 5000  # 5 seconds
        self.is_boss_skill = True  # Flag for boss skills
        self.last_damage_time = 0
        self.damage_interval = 500  # Damage every 500ms

        # Use a larger hitbox for collision
        self.hitbox = pygame.Rect(
            self.rect.x - 50,  # Expand left
            self.rect.y - 50,  # Expand upward
            self.rect.width + 100,  # Total width
            self.rect.height + 100  # Total height
        )

    def update(self):
        # Remove effect after duration expires
        if pygame.time.get_ticks() - self.start_time > self.duration:
            self.kill()
            return

        # Update hitbox position to follow animation
        self.hitbox.center = self.rect.center  # Match star's position

        # Animate
        self.counter += 1
        if self.counter % self.animation_speed == 0:
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
            self.image = self.images[self.current_image_index]

        # Continuous damage check with hitbox
        current_time = pygame.time.get_ticks()
        if current_time - self.last_damage_time >= self.damage_interval:
            # Use pygame.Rect.colliderect() for direct rect comparison
            if self.hitbox.colliderect(player.rect):
                player.take_damage(self.damage)
                self.last_damage_time = current_time


# -------------------------------------------------------------------------------------------------------------------------------
# Characters
class Player(pygame.sprite.Sprite):
    def __init__(self, bool1, bool2, bool3, bool4):
        super().__init__()
        self.idle_images = main1idle
        self.walk_images = main1walk
        self.attack_sets = [main1attack1, main1attack2, main1attack3]
        self.skill_sets = main1skill1
        self.skill_sets2 = main1skill2
        self.hurt_images = main1hurt
        self.dead_images = main1dead

        self.flipped_idle_images = [pygame.transform.flip(img, True, False) for img in self.idle_images]
        self.flipped_walk_images = [pygame.transform.flip(img, True, False) for img in self.walk_images]
        self.flipped_attack_sets = [[pygame.transform.flip(img, True, False) for img in attack] for attack in
                                    self.attack_sets]
        self.flipped_hurt_images = [pygame.transform.flip(img, True, False) for img in self.hurt_images]
        self.flipped_dead_images = [pygame.transform.flip(img, True, False) for img in self.dead_images]
        self.flipped_skill_set = [pygame.transform.flip(img, True, False) for img in self.skill_sets]
        self.flipped_skill_set2 = [pygame.transform.flip(img, True, False) for img in self.skill_sets2]

        self.currentImages = self.idle_images
        self.currentImageIndex = 0
        self.image = self.currentImages[self.currentImageIndex]
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH, SCREEN_HEIGHT)

        self.animationCounter = 0
        self.speed = SPEED
        self.facing_right = True  # Default direction
        self.is_attacking = False
        self.attack_set_index = 0
        self.last_attack_time = 0  # Timestamp for attack cooldown

        self.max_health = HEALTH  # Max HP
        self.health = self.max_health  # Current HP
        self.invulnerable_time = 0  # Timestamp for invulnerability after being hit
        self.has_hit_zombie = False
        self.is_transitioning = False
        self.ulti_zoom = False
        self.skill1_learned = bool1
        self.skill2_learned = bool2
        self.Transform_learned = bool3
        if self.Transform_learned:
            self.transform_cooldown = 30000  # e.g., 10 seconds cooldown
            self.last_transform_time = 0

        self.skill1_cooldown = 3000  # 3 seconds
        self.last_skill1_time = 0
        self.is_using_skill1 = False
        self.is_using_skill2 = False

        self.skill2_cooldown = 3000
        self.skill2_duration = 3000  # Total skill duration 3 seconds
        self.last_skill2_time = 0
        self.skill2_effect_delay = 500  # Water effects appear after 2 seconds
        self.skill2_start_time = 0

        # Add a flag for the Recover skill; set to True if selected
        self.recover_skill_selected = bool4
        self.recover_interval = 10000  # 10 seconds in milliseconds
        self.last_recover_time = pygame.time.get_ticks()  # initialize recovery timer

        # Load with PIL
        charimage = Image.open("Assets\\Samurai\\Idle\\0.png")

        # Define crop box (left, top, right, bottom)
        box = (20, 5, 80, 65)  # Adjust these values to match the head position

        # Crop and convert to Pygame
        charcropped = charimage.crop(box)
        self.icon = pygame.image.fromstring(charcropped.tobytes(), charcropped.size, charcropped.mode)

        # Resize if necessary
        self.icon = pygame.transform.scale(self.icon, (60, 60))

        self.is_dead = False
        self.death_animation_timer = 0  # Track how long the death animation plays
        self.death_animation_finished = False  # Flag to check if animation is done

    def use_skill(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_skill1_time >= self.skill1_cooldown and not self.is_attacking:
            self.is_using_skill1 = True
            skill_channel = pygame.mixer.Channel(3)
            skill_channel.set_volume(0.5)
            skill_channel.play(dashattacksound)
            self.currentImages = self.skill_sets if self.facing_right else self.flipped_skill_set
            self.currentImageIndex = 0
            self.last_skill1_time = current_time
            self.has_hit_zombie = False

            # Add multiple explosion effects in a line
            offset = 100 if self.facing_right else -100
            for i in range(1, 4):
                explosion_x = self.rect.centerx + (offset * i)
                explosion = WaterExplosionEffect(explosion_x, self.rect.centery, self.facing_right)
                all_sprites.add(explosion)

    def use_skill2(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.skill2_start_time >= self.skill2_duration and current_time - self.last_skill2_time >= self.skill2_cooldown and not self.is_attacking:
            self.is_using_skill2 = True
            skill_channel = pygame.mixer.Channel(3)
            skill_channel.set_volume(0.5)
            skill_channel.play(fireballsound)
            self.currentImages = self.skill_sets2 if self.facing_right else self.flipped_skill_set2
            self.currentImageIndex = 0
            self.skill2_start_time = current_time  # Track start time
            self.last_skill2_time = current_time

    def transition_to_samurai2(self):
        # Create a new Samurai2 instance at the player's position
        x, y = self.rect.center
        health = self.health
        facing_right = self.facing_right
        samurai2 = Samurai2(x, y, health, facing_right)

        # Copy cooldown attributes from Player to Samurai2
        samurai2.last_skill1_time = self.last_skill1_time
        samurai2.skill1_cooldown = self.skill1_cooldown
        samurai2.last_skill2_time = self.last_skill2_time
        samurai2.skill2_cooldown = self.skill2_cooldown

        # Copy transform cooldown attributes if the transform skill is learned
        if self.Transform_learned:
            samurai2.Transform_learned = self.Transform_learned
            samurai2.transform_cooldown = self.transform_cooldown
            samurai2.last_transform_time = self.last_transform_time

        # Copy the skill learned booleans so Samurai2 has them
        samurai2.skill1_learned = self.skill1_learned
        samurai2.skill2_learned = self.skill2_learned

        # *** Copy the recovery skill attributes ***
        samurai2.recover_skill_selected = self.recover_skill_selected
        samurai2.recover_interval = self.recover_interval
        samurai2.last_recover_time = self.last_recover_time

        # Replace the player with Samurai2
        all_sprites.remove(self)
        all_sprites.add(samurai2)
        return samurai2

    def recover_hp(self):
        if self.health < self.max_health:
            self.health += RECOVERYAMOUNT
            if self.health > self.max_health:
                self.health = self.max_health
            # Spawn the heart effect above the player's head (or adjust position as needed)
            heart_effect = HeartEffect(self.rect.centerx, self.rect.top - 10, duration=1000)
            all_sprites.add(heart_effect)

    def move(self, direction):
        global camera_x, camera_y
        if direction == "a":
            if self.rect.left > 430:
                self.rect.x -= self.speed
                camera_x -= self.speed
                if self.facing_right:
                    self.facing_right = False
        elif direction == "d":
            if self.rect.right < MAP_WIDTH - 430:
                self.rect.x += self.speed
                camera_x += self.speed
                if not self.facing_right:
                    self.facing_right = True
        elif direction == "w":
            if self.rect.top > 305:
                self.rect.y -= self.speed
                camera_y -= self.speed
        elif direction == "s":
            if self.rect.bottom < MAP_HEIGHT - 305:
                self.rect.y += self.speed
                camera_y += self.speed
        elif direction == "wa":
            if self.rect.top > 305 and self.rect.left > 430:
                self.rect.x -= self.speed
                self.rect.y -= self.speed
                camera_x -= self.speed
                camera_y -= self.speed
                if self.facing_right:
                    self.facing_right = False
        elif direction == "wd":
            if self.rect.top > 305 and self.rect.right < MAP_WIDTH - 430:
                self.rect.x += self.speed
                self.rect.y -= self.speed
                camera_x += self.speed
                camera_y -= self.speed
                if not self.facing_right:
                    self.facing_right = True
        elif direction == "sa":
            if self.rect.left > 430 and self.rect.bottom < MAP_HEIGHT - 305:
                self.rect.x -= self.speed
                self.rect.y += self.speed
                camera_x -= self.speed
                camera_y += self.speed
                if self.facing_right:
                    self.facing_right = False
        elif direction == "sd":
            if self.rect.right < MAP_WIDTH - 430 and self.rect.bottom < MAP_HEIGHT - 305:
                self.rect.x += self.speed
                self.rect.y += self.speed
                camera_x += self.speed
                camera_y += self.speed
                if not self.facing_right:
                    self.facing_right = True

    def attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= ATTACK_COOLDOWN:
            self.is_attacking = True
            slashsound.set_volume(0.3)
            slashsound.play()
            self.currentImageIndex = 0
            self.currentImages = self.attack_sets[self.attack_set_index] if self.facing_right else \
                self.flipped_attack_sets[self.attack_set_index]
            self.attack_set_index = (self.attack_set_index + 1) % 3
            self.last_attack_time = current_time

    def draw_health_bar(self, screen):
        bar_width = 200  # Width of the health bar
        bar_height = 50  # Height of the health bar
        health_ratio = self.health / self.max_health  # Scale HP to bar size

        bar_x = 80  # X position of the bar
        bar_y = 20  # Y position of the bar

        # **Draw Background Bar (Black)**
        pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height))

        # **Draw Health Bar (Red)**
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))

        # **Draw the Character Icon Next to the Health Bar**
        icon_size = 75  # Adjust as needed
        icon_x = bar_x - icon_size  # Move left of health bar
        icon_y = bar_y - (icon_size // 6)  # Align vertically
        pygame.draw.rect(screen, (0, 0, 88), (icon_x, icon_y, icon_size, icon_size))

        icon_x = bar_x - 75
        icon_y = bar_y - 10
        screen.blit(self.icon, (icon_x, icon_y))

        # **Draw Health Text**
        font = pygame.font.Font(None, 50)
        text = font.render(f"{self.health}/{self.max_health}", True, (255, 255, 255))
        screen.blit(text, (bar_x + 70, bar_y + 10))

        # **Red Pulsing Border When Low HP**
        if self.health <= 3:
            pulse_intensity = max(50, 255 - (self.health * 80))  # More intense at lower HP
            alpha = abs(math.sin(pygame.time.get_ticks() * 0.005)) * pulse_intensity  # Smooth pulsing

            border_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(border_surface, (255, 0, 0, int(alpha)), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 20)
            screen.blit(border_surface, (0, 0))

    def take_damage(self, amount):
        # Reduce player's health when hit and handle invulnerability.
        current_time = pygame.time.get_ticks()

        # Spawn blood splash effect at the entity's position
        blood_effect = BloodSplashEffect(self.rect.centerx, self.rect.centery)
        all_sprites.add(blood_effect)

        # Create a red flash effect
        red_flash = self.image.copy()
        red_overlay = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        red_overlay.fill((255, 0, 0, 150))  # Red tint with transparency
        red_flash.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        self.image = red_flash  # Apply red effect

        # Schedule reverting to normal image after a short time
        self.flash_time = pygame.time.get_ticks() + 50

        if current_time > self.invulnerable_time:
            self.health -= amount
            hit_channel = pygame.mixer.Channel(6)
            hit_channel.set_volume(0.5)
            hit_channel.play(playerhitsound)

            if self.health < 0:
                self.health = 0  # Prevent negative health
            self.invulnerable_time = current_time + PLAYER_INVULNERABLE  # 1 second of invulnerability
            self.currentImages = self.hurt_images if self.facing_right else self.flipped_hurt_images
            self.currentImageIndex = 0

    def dead(self):
        if not self.is_dead:  # Ensure this runs only once
            self.is_dead = True
            dead_channel = pygame.mixer.Channel(5)
            dead_channel.set_volume(3)
            dead_channel.play(playerdeadsound)
            self.currentImages = self.dead_images  # Set death animation frames
            self.currentImageIndex = 0  # Start from the first death frame
            self.animationCounter = 0  # Reset animation counter
            self.death_animation_timer = pygame.time.get_ticks()  # Start death animation timer

    def update(self, keys):
        global running
        current_time = pygame.time.get_ticks()

        if self.health <= 0:
            if not self.is_dead:
                self.dead()

            # **Play Death Animation for 1.5 Seconds Before Clearing Screen**
            elif pygame.time.get_ticks() - self.death_animation_timer < 1500:
                self.animationCounter += 1
                if self.animationCounter % 20 == 0:  # Slower animation speed
                    if self.currentImageIndex < len(self.currentImages) - 1:
                        self.currentImageIndex += 1
                    self.image = self.currentImages[self.currentImageIndex]
            else:
                self.death_animation_finished = True  # Mark animation as done
                all_sprites.empty()
                zombies.empty()

            return

        if self.recover_skill_selected:
            if current_time - self.last_recover_time >= self.recover_interval:
                self.recover_hp()
                self.last_recover_time = current_time

        moving = False
        if not self.is_attacking:
            if keys[pygame.K_a] and keys[pygame.K_w]:
                self.move("wa")
                moving = True
            elif keys[pygame.K_a] and keys[pygame.K_s]:
                self.move("sa")
                moving = True
            elif keys[pygame.K_d] and keys[pygame.K_w]:
                self.move("wd")
                moving = True
            elif keys[pygame.K_d] and keys[pygame.K_s]:
                self.move("sd")
                moving = True
            elif keys[pygame.K_a]:
                self.move("a")
                moving = True
            elif keys[pygame.K_d]:
                self.move("d")
                moving = True
            elif keys[pygame.K_w]:
                self.move("w")
                moving = True
            elif keys[pygame.K_s]:
                self.move("s")
                moving = True

        if keys[pygame.K_j]:
            self.attack()

        # Handle invulnerability flickering
        current_time = pygame.time.get_ticks()
        if current_time < self.invulnerable_time:
            if (current_time // 100) % 2 == 0:
                self.image.set_alpha(0)  # Make invisible
            else:
                self.image.set_alpha(255)  # Make visible
        else:
            self.image.set_alpha(255)  # Ensure visibility after invulnerability

        if self.skill1_learned:
            if keys[pygame.K_k] and not self.is_using_skill1:
                self.use_skill()

        # Handle skill animation
        if self.is_using_skill1:
            self.animationCounter += 1

            # Update frame and movement only every 8 ticks
            if self.animationCounter % 8 == 0:
                self.currentImageIndex += 1

                # Handle left-facing movement synchronized with specific frames
                if self.facing_right:
                    if self.currentImageIndex == 1:
                        self.rect.x += 100
                        # Add boundary check
                        if self.rect.left > MAP_WIDTH - 430:
                            self.rect.left = MAP_WIDTH - 430
                    elif self.currentImageIndex == 2:
                        self.rect.x += 125
                        if self.rect.left > MAP_WIDTH - 430:
                            self.rect.left = MAP_WIDTH - 430
                    elif self.currentImageIndex == 3:
                        self.rect.x += 150
                        if self.rect.left > MAP_WIDTH - 430:
                            self.rect.left = MAP_WIDTH - 430

                # Handle left-facing movement synchronized with specific frames
                if not self.facing_right:
                    if self.currentImageIndex == 1:
                        self.rect.x -= 100
                        # Add boundary check
                        if self.rect.left < 430:
                            self.rect.left = 430
                    elif self.currentImageIndex == 2:
                        self.rect.x -= 125
                        if self.rect.left < 430:
                            self.rect.left = 430
                    elif self.currentImageIndex == 3:
                        self.rect.x -= 150
                        if self.rect.left < 430:
                            self.rect.left = 430

                # Update image and check animation completion for all directions
                if self.currentImageIndex >= len(self.currentImages):
                    # Reset animation
                    self.is_using_skill1 = False
                    self.currentImages = self.idle_images if self.facing_right else self.flipped_idle_images
                    self.currentImageIndex = 0
                else:
                    # Update current frame image
                    self.image = self.currentImages[self.currentImageIndex]

            return  # Prevent other animations from overriding

        if self.skill2_learned:
            if keys[pygame.K_l] and not self.is_using_skill2:
                self.use_skill2()

        if self.skill2_start_time > 0:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.skill2_start_time

            # Add water effects after 2000ms
            if elapsed >= self.skill2_effect_delay:
                water_x = self.rect.centerx + 150 if self.facing_right else self.rect.centerx - 50
                offset = 100 if self.facing_right else -100
                for i in range(1, 4):
                    effect_x = water_x + (offset * i)
                    all_sprites.add(
                        WaterEffect(water_x, self.rect.centery, self.facing_right),
                        WaterfallEffect(effect_x, self.rect.centery, self.facing_right)
                    )
                self.skill2_start_time = 0  # Reset to prevent continuous spawning

        # Handle skill animation
        if self.is_using_skill2:
            self.animationCounter += 1
            if self.animationCounter % 8 == 0:
                self.currentImageIndex += 1
                if self.currentImageIndex >= len(self.currentImages):
                    self.is_using_skill2 = False
                    self.currentImages = self.idle_images if self.facing_right else self.flipped_idle_images
                    self.currentImageIndex = 0
                else:
                    self.image = self.currentImages[self.currentImageIndex]
            return  # Prevent other animations from overriding

        if self.Transform_learned:
            if keys[
                pygame.K_t] and not self.is_transitioning and pygame.time.get_ticks() - self.last_transform_time >= self.transform_cooldown:
                transformsound.play()
                self.is_transitioning = True
                self.last_transform_time = pygame.time.get_ticks()  # start the cooldown
                global active_transition_effect
                active_transition_effect = TransformationEffect(self.rect.centerx, self.rect.centery - 60)
                all_sprites.add(active_transition_effect)

        self.animationCounter += 1
        if self.animationCounter % 5 == 0:
            self.currentImageIndex = (self.currentImageIndex + 1) % len(self.currentImages)
            self.image = self.currentImages[self.currentImageIndex]

        # Handle invulnerability flickering
        current_time = pygame.time.get_ticks()
        if current_time < self.invulnerable_time and not (
                self.is_using_skill1 or self.is_using_skill2):  # Add condition
            if (current_time // 100) % 2 == 0:
                self.image.set_alpha(0)
            else:
                self.image.set_alpha(255)
        elif not (self.is_using_skill1 or self.is_using_skill2):  # Ensure normal visibility when not using skill
            self.image.set_alpha(255)

        # Handle animation transitions
        if self.is_attacking:
            if self.currentImageIndex == len(self.currentImages) - 1:
                self.is_attacking = False
                self.currentImages = self.walk_images if moving else self.idle_images
                if not self.facing_right:
                    self.currentImages = self.flipped_walk_images if moving else self.flipped_idle_images
                self.currentImageIndex = 0
        elif moving:
            self.currentImages = self.walk_images if self.facing_right else self.flipped_walk_images
        else:
            self.currentImages = self.idle_images if self.facing_right else self.flipped_idle_images


class Samurai2(pygame.sprite.Sprite):
    def __init__(self, x, y, health, facing_right):
        super().__init__()
        self.idle_images = samuraiidle
        self.walk_images = samurairun
        self.attack_sets = [samuraiattack1, samuraiattack2, samuraiulti]
        self.hurt_images = samuraihurt
        self.dead_images = samuraidead

        self.flipped_idle_images = [pygame.transform.flip(img, True, False) for img in self.idle_images]
        self.flipped_walk_images = [pygame.transform.flip(img, True, False) for img in self.walk_images]
        self.flipped_attack_sets = [[pygame.transform.flip(img, True, False) for img in attack] for attack in
                                    self.attack_sets]
        self.flipped_hurt_images = [pygame.transform.flip(img, True, False) for img in self.hurt_images]
        self.flipped_dead_images = [pygame.transform.flip(img, True, False) for img in self.dead_images]

        self.currentImages = self.idle_images if facing_right else self.flipped_idle_images
        self.currentImageIndex = 0
        self.image = self.currentImages[self.currentImageIndex]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.animationCounter = 0
        self.speed = SPEED + 1  # Adjust speed if needed
        self.facing_right = facing_right
        self.is_attacking = False
        self.attack_set_index = 0
        self.last_attack_time = 0
        self.max_health = HEALTH  # Max HP
        self.health = self.max_health  # Current HP
        self.health = health
        self.invulnerable_time = 0
        self.has_hit_zombie = False
        self.death_animation_finished = False

        # Add new ultimate variables
        self.ulti_active = False
        self.ulti_start_time = 0
        self.ulti_duration = 5000  # 5 seconds
        self.ulti_cooldown = 10000  # 10 seconds cooldown
        self.last_ulti_time = 0
        self.last_damage_time = 0
        self.ulti_zoom = False
        self.skill3_cooldown = 5000  # 5 seconds cooldown
        self.last_skill3_time = 0
        self.is_using_skill3 = False
        self.skill3_phase = 0  # 0: slice, 1: fire, 2: explosion

        # Load with PIL
        charimage = Image.open("Assets\\Samurai2\\Idle\\Idle.png")

        # Define crop box (left, top, right, bottom)
        box = (60, 35, 120, 95)  # Adjust these values to match the head position

        # Crop and convert to Pygame
        charcropped = charimage.crop(box)
        self.icon = pygame.image.fromstring(charcropped.tobytes(), charcropped.size, charcropped.mode)

        # Resize if necessary
        self.icon = pygame.transform.scale(self.icon, (60, 60))

        self.transform_start_time = pygame.time.get_ticks()  # record transformation start
        self.transform_duration = 15000  # 15 seconds duration

    def use_skill3(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_skill3_time >= self.skill3_cooldown:
            self.is_using_skill3 = True
            skill_channel = pygame.mixer.Channel(3)
            skill_channel.set_volume(0.7)
            skill_channel.play(comboattacksound)
            self.currentImages = samuraiskill if self.facing_right else [pygame.transform.flip(img, True, False) for img
                                                                         in samuraiskill]
            self.currentImageIndex = 0
            self.last_skill3_time = current_time
            self.skill3_start_time = current_time
            self.skill3_phase = 0
            self.skill3_effects_added = [False, False, False]

    def move(self, direction):
        global camera_x, camera_y
        if direction == "a":
            if self.rect.left > 430:
                self.rect.x -= self.speed
                camera_x -= self.speed
                if self.facing_right:
                    self.facing_right = False
        elif direction == "d":
            if self.rect.right < MAP_WIDTH - 430:
                self.rect.x += self.speed
                camera_x += self.speed
                if not self.facing_right:
                    self.facing_right = True
        elif direction == "w":
            if self.rect.top > 305:
                self.rect.y -= self.speed
                camera_y -= self.speed
        elif direction == "s":
            if self.rect.bottom < MAP_HEIGHT - 305:
                self.rect.y += self.speed
                camera_y += self.speed
        elif direction == "wa":
            if self.rect.top > 305 and self.rect.left > 430:
                self.rect.x -= self.speed
                self.rect.y -= self.speed
                camera_x -= self.speed
                camera_y -= self.speed
                if self.facing_right:
                    self.facing_right = False
        elif direction == "wd":
            if self.rect.top > 305 and self.rect.right < MAP_WIDTH - 430:
                self.rect.x += self.speed
                self.rect.y -= self.speed
                camera_x += self.speed
                camera_y -= self.speed
                if not self.facing_right:
                    self.facing_right = True
        elif direction == "sa":
            if self.rect.left > 430 and self.rect.bottom < MAP_HEIGHT - 305:
                self.rect.x -= self.speed
                self.rect.y += self.speed
                camera_x -= self.speed
                camera_y += self.speed
                if self.facing_right:
                    self.facing_right = False
        elif direction == "sd":
            if self.rect.right < MAP_WIDTH - 430 and self.rect.bottom < MAP_HEIGHT - 305:
                self.rect.x += self.speed
                self.rect.y += self.speed
                camera_x += self.speed
                camera_y += self.speed
                if not self.facing_right:
                    self.facing_right = True

    def attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= ATTACK_COOLDOWN:
            self.is_attacking = True
            slashsound.set_volume(0.3)
            slashsound.play()
            self.currentImageIndex = 0
            self.currentImages = self.attack_sets[self.attack_set_index] if self.facing_right else \
                self.flipped_attack_sets[self.attack_set_index]
            self.attack_set_index = (self.attack_set_index + 1) % 2  # Only 2 attack sets
            self.last_attack_time = current_time
            self.has_hit_zombie = False

    def draw_health_bar(self, screen):
        bar_width = 200  # Width of the health bar
        bar_height = 50  # Height of the health bar
        health_ratio = self.health / self.max_health  # Scale HP to bar size

        bar_x = 80  # X position of the bar
        bar_y = 20  # Y position of the bar

        # **Draw Background Bar (Black)**
        pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height))

        # **Draw Health Bar (Red)**
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))

        # **Draw the Character Icon Next to the Health Bar**
        icon_size = 75  # Adjust as needed
        icon_x = bar_x - icon_size  # Move left of health bar
        icon_y = bar_y - (icon_size // 6)  # Align vertically
        pygame.draw.rect(screen, (0, 0, 88), (icon_x, icon_y, icon_size, icon_size))

        icon_x = bar_x - 75
        icon_y = bar_y - 10
        screen.blit(self.icon, (icon_x, icon_y))

        # **Draw Health Text**
        font = pygame.font.Font(None, 50)
        text = font.render(f"{self.health}/{self.max_health}", True, (255, 255, 255))
        screen.blit(text, (bar_x + 70, bar_y + 10))

        # **Red Pulsing Border When Low HP**
        if self.health <= 3:
            pulse_intensity = max(50, 255 - (self.health * 80))  # More intense at lower HP
            alpha = abs(math.sin(pygame.time.get_ticks() * 0.005)) * pulse_intensity  # Smooth pulsing

            border_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(border_surface, (255, 0, 0, int(alpha)), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 20)
            screen.blit(border_surface, (0, 0))

    def take_damage(self, amount):
        # Spawn blood splash effect at the entity's position
        blood_effect = BloodSplashEffect(self.rect.centerx, self.rect.centery)
        all_sprites.add(blood_effect)

        # Add check for skill3 invulnerability
        if self.is_using_skill3:  # Invulnerable during skills
            return
        current_time = pygame.time.get_ticks()
        if current_time - self.invulnerable_time >= PLAYER_INVULNERABLE:
            self.health -= amount
            self.invulnerable_time = current_time + PLAYER_INVULNERABLE  # 1 second invulnerability
            # Show hurt animation only if not using skills
            if not self.is_using_skill3:
                self.currentImages = self.hurt_images if self.facing_right else self.flipped_hurt_images
                self.currentImageIndex = 0

    def dead(self):
        self.currentImages = self.dead_images  # Set death animation frames
        self.currentImageIndex = 0  # Start from the first death frame
        self.animationCounter = 0  # Reset animation counter

    def update(self, keys):

        moving = False
        current_time = pygame.time.get_ticks()

        # Handle death animation
        if self.health == 0:
            if self.currentImageIndex < len(self.dead_images) - 1:
                self.animationCounter += 1
                if self.animationCounter % 10 == 0:  # Slow down the animation
                    self.currentImageIndex += 1
                    self.image = self.dead_images[self.currentImageIndex]

                # Check if 15 seconds have passed since transformation
        if self.health <= 0 or (current_time - self.transform_start_time >= self.transform_duration):
            self.revert_to_player()
            return

        if not self.is_attacking:
            if keys[pygame.K_a] and keys[pygame.K_w]:
                self.move("wa")
                moving = True
            elif keys[pygame.K_a] and keys[pygame.K_s]:
                self.move("sa")
                moving = True
            elif keys[pygame.K_d] and keys[pygame.K_w]:
                self.move("wd")
                moving = True
            elif keys[pygame.K_d] and keys[pygame.K_s]:
                self.move("sd")
                moving = True
            elif keys[pygame.K_a]:
                self.move("a")
                moving = True
            elif keys[pygame.K_d]:
                self.move("d")
                moving = True
            elif keys[pygame.K_w]:
                self.move("w")
                moving = True
            elif keys[pygame.K_s]:
                self.move("s")
                moving = True

        if keys[pygame.K_j]:
            self.attack()

        if keys[pygame.K_k] and not self.ulti_active and not self.is_using_skill3:
            self.use_skill3()

        if self.is_using_skill3:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.skill3_start_time

            # Handle left-facing movement during specific frames
            self.animationCounter += 1
            if self.animationCounter % 8 == 0:
                self.currentImageIndex += 1

                # Add movement offsets when facing left
                if not self.facing_right:
                    if self.currentImageIndex == 3:
                        self.rect.x -= 100
                        if self.rect.left < 430:
                            self.rect.left = 430
                    elif self.currentImageIndex == 6:
                        self.rect.x -= 150
                        if self.rect.left < 430:
                            self.rect.left = 430
                    elif self.currentImageIndex == 9:
                        self.rect.x -= 200
                        if self.rect.left < 430:
                            self.rect.left = 430

                # Add movement offsets when facing right
                else:
                    if self.currentImageIndex == 3:
                        self.rect.x += 100
                        if self.rect.right > MAP_WIDTH - 430:
                            self.rect.right = MAP_WIDTH - 430
                    elif self.currentImageIndex == 6:
                        self.rect.x += 150
                        if self.rect.right > MAP_WIDTH - 430:
                            self.rect.right = MAP_WIDTH - 430
                    elif self.currentImageIndex == 9:
                        self.rect.x += 200
                        if self.rect.right > MAP_WIDTH - 430:
                            self.rect.right = MAP_WIDTH - 430

                # Check animation completion
                if self.currentImageIndex >= len(self.currentImages):
                    self.is_using_skill3 = False  # Reset skill flag
                    self.currentImages = self.idle_images if self.facing_right else self.flipped_idle_images
                    self.currentImageIndex = 0
                else:
                    self.image = self.currentImages[self.currentImageIndex]

            if elapsed >= 500 and not self.skill3_effects_added[0]:  # Slice effect
                slice_x = self.rect.centerx + (150 if self.facing_right else -250)
                all_sprites.add(SliceEffect(slice_x, self.rect.centery, self.facing_right))
                self.skill3_effects_added[0] = True

            if elapsed >= 1300 and not self.skill3_effects_added[1]:  # Fire effects
                fire_x = self.rect.centerx + (150 if self.facing_right else -150)
                all_sprites.add(
                    Fire2Effect(fire_x, self.rect.centery - 100, self.facing_right),
                    Fire3Effect(fire_x, self.rect.centery - 100, self.facing_right)
                )
                self.skill3_effects_added[1] = True

            if elapsed >= 1700 and not self.skill3_effects_added[2]:  # Explosion effect
                explosion_x = self.rect.centerx + (150 if self.facing_right else -150)
                all_sprites.add(ExplosionEffect(explosion_x, self.rect.centery - 100, self.facing_right))
                self.skill3_effects_added[2] = True

            return  # Prevent other animations from overriding

        # Handle ultimate activation
        if keys[pygame.K_l] and not self.ulti_active and \
                (current_time - self.last_ulti_time >= self.ulti_cooldown):
            skill_channel = pygame.mixer.Channel(3)
            skill_channel.set_volume(0.3)
            skill_channel.play(lasersound)
            self.ulti_zoom = True  # Enable zoom
            self.ulti_active = True
            self.ulti_start_time = current_time
            self.last_ulti_time = current_time
            self.currentImages = self.attack_sets[2] if self.facing_right else self.flipped_attack_sets[2]
            self.currentImageIndex = 0  # Reset to start animation from beginning
            self.invulnerable_time = current_time + self.ulti_duration  # Make player invulnerable during ultimate
            fire_effect = ChargingEffect(
                self.rect.centerx - 30,  # X position stays centered on player
                self.rect.centery + 50,  # Add 50 pixels to Y position to place it lower
                self.ulti_duration
            )
            all_sprites.add(fire_effect)

        # Handle ultimate state
        if self.ulti_active:
            if current_time - self.ulti_start_time >= self.ulti_duration:
                self.ulti_zoom = False
                self.ulti_active = False
                self.currentImages = self.idle_images if self.facing_right else self.flipped_idle_images
                self.currentImageIndex = 0
                # Remove sword fire effect when ultimate ends
                if hasattr(self, 'sword_fire') and self.sword_fire.alive():
                    self.sword_fire.kill()
            else:
                # Calculate current frame based on elapsed time
                elapsed_time = current_time - self.ulti_start_time
                progress = elapsed_time / self.ulti_duration
                frame_index = int(progress * len(self.currentImages))
                frame_index = min(frame_index, len(self.currentImages) - 1)
                self.currentImageIndex = frame_index
                self.image = self.currentImages[self.currentImageIndex]

                # Add sword fire effect during last second
                if elapsed_time >= 3500:  # Last 1000ms of ultimate
                    # Calculate sword position based on facing direction
                    offset_x = 100 if self.facing_right else -300
                    fire_x = self.rect.centerx + offset_x
                    fire_y = self.rect.centery - 40

                    # Create/sword fire effect
                    if not hasattr(self, 'sword_fire') or not self.sword_fire.alive():
                        self.sword_fire = SwordFireEffect(fire_x, fire_y)
                        all_sprites.add(self.sword_fire)
                    else:
                        # Update fire position
                        self.sword_fire.rect.center = (fire_x + 230, fire_y - 20)
                else:
                    # Remove sword fire effect if not in the last second
                    if hasattr(self, 'sword_fire') and self.sword_fire.alive():
                        self.sword_fire.kill()

        # Modify attack condition to prevent normal attacks during ultimate
        if not self.ulti_active:
            self.animationCounter += 1
            if self.animationCounter % 8 == 0:
                self.currentImageIndex = (self.currentImageIndex + 1) % len(self.currentImages)
                self.image = self.currentImages[self.currentImageIndex]

        # Handle invulnerability flickering
        if current_time < self.invulnerable_time:
            if (current_time // 100) % 2 == 0:
                self.image.set_alpha(0)  # Make invisible
            else:
                self.image.set_alpha(255)  # Make visible
        else:
            self.image.set_alpha(255)  # Ensure visibility after invulnerability

        # Handle animation transitions
        if not self.ulti_active:
            if self.is_attacking:
                if self.currentImageIndex == len(self.currentImages) - 1:
                    self.is_attacking = False
                    self.currentImages = self.walk_images if moving else self.idle_images
                    if not self.facing_right:
                        self.currentImages = self.flipped_walk_images if moving else self.flipped_idle_images
                    self.currentImageIndex = 0
            elif moving:
                self.currentImages = self.walk_images if self.facing_right else self.flipped_walk_images
            else:
                self.currentImages = self.idle_images if self.facing_right else self.flipped_idle_images

        # Update sword fire effect if it exists
        if hasattr(self, 'sword_fire') and self.sword_fire.alive():
            self.sword_fire.update()

    def revert_to_player(self):
        # Play the transformation effect (same as when transforming to Samurai2)
        revertsound.set_volume(0.5)
        revertsound.play()
        transformation = TransformationEffect(self.rect.centerx, self.rect.centery - 60)
        all_sprites.add(transformation)

        # Create a new Player instance. Optionally, you may reset the health or carry over cooldowns.
        new_player = Player(self.skill1_learned, self.skill2_learned, self.Transform_learned,
                            self.recover_skill_selected)
        new_player.rect.center = self.rect.center
        # Optionally, you can restore health (for example, reset to full) rather than 0.
        new_player.health = self.max_health
        new_player.facing_right = self.facing_right

        # Copy cooldowns if you want them to persist
        new_player.last_skill1_time = self.last_skill1_time
        new_player.last_skill2_time = self.last_skill2_time
        if self.Transform_learned:
            new_player.transform_cooldown = self.transform_cooldown
            new_player.last_transform_time = self.last_transform_time
        new_player.recover_interval = self.recover_interval
        new_player.last_recover_time = self.last_recover_time

        # Remove Samurai2 and update the global player reference
        all_sprites.remove(self)
        all_sprites.add(new_player)
        global player
        player = new_player


class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.idle_images = bossidle
        self.walk_images = bosswalk
        self.attack_images = bossattack
        self.hurt_images = bosshurt
        self.dead_images = bossdead

        self.flipped_idle_images = [pygame.transform.flip(img, True, False) for img in self.idle_images]
        self.flipped_walk_images = [pygame.transform.flip(img, True, False) for img in self.walk_images]
        self.flipped_attack_images = [pygame.transform.flip(img, True, False) for img in self.attack_images]
        self.flipped_hurt_images = [pygame.transform.flip(img, True, False) for img in self.hurt_images]
        self.flipped_dead_images = [pygame.transform.flip(img, True, False) for img in self.dead_images]

        self.currentImages = self.idle_images
        self.currentImageIndex = 0
        self.image = self.currentImages[self.currentImageIndex]
        self.rect = self.image.get_rect(center=(x, y))
        self.animationCounter = 0
        self.speed = 3
        self.health = 500
        self.is_attacking = False
        self.last_attack_time = 0
        self.is_dying = False
        self.facing_right = True
        self.skill_cooldown = 10000  # 10 seconds
        self.last_skill_time = 0
        self.skill_duration = 1500  # 1.5 seconds
        self.hurt_cooldown = 500  # 0.5 seconds cooldown after being hurt
        self.last_hurt_time = 0
        self.skill_cooldown = 10000  # Changed from 10000 to 5000 (5 seconds)
        self.last_skill_time = pygame.time.get_ticks() - 5000  # Start ready to use

    def use_star_skill(self):
        bossskill_channel = pygame.mixer.Channel(4)
        bossskill_channel.set_volume(1)
        bossskill_channel.play(bossskillsound)
        # Positions relative to boss with larger offsets
        positions = [
            (self.rect.centerx + 100, self.rect.centery + 350),  # Right
            (self.rect.centerx - 100, self.rect.centery + 350),  # Left
            (self.rect.centerx, self.rect.centery + 450),  # Bottom
            (self.rect.centerx, self.rect.centery + 250),  # Top
            (self.rect.centerx + 70, self.rect.centery + 420),  # Right-bottom
            (self.rect.centerx - 70, self.rect.centery + 280),  # Left-bottom
            (self.rect.centerx + 70, self.rect.centery + 280),  # Right-top
            (self.rect.centerx - 70, self.rect.centery + 420),  # Left-top
        ]

        for pos in positions:
            star = StarEffect(pos[0], pos[1])
            star.is_boss_skill = True
            all_sprites.add(star)

        # Reset movement state
        self.is_attacking = False
        self.currentImages = self.walk_images if self.facing_right else self.flipped_walk_images
        self.currentImageIndex = 0

    def move_towards_player(self, player):
        if self.is_dying or self.health <= 0:
            return

        dx = player.rect.centerx - self.rect.centerx
        self.facing_right = dx > 0
        if not self.facing_right:
            self.currentImages = self.flipped_walk_images
        else:
            self.currentImages = self.walk_images

        dy = player.rect.centery - self.rect.centery
        dist = (dx ** 2 + dy ** 2) ** 0.5
        if dist != 0:
            self.rect.x += int(self.speed * dx / dist)
            self.rect.y += int(self.speed * dy / dist)

    def attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= 2000:  # 2 second attack cooldown
            self.is_attacking = True
            bossattacksound1.set_volume(1)
            bossattacksound2.set_volume(1)
            random.choice([bossattacksound1, bossattacksound2]).play()
            self.currentImageIndex = 0
            self.currentImages = self.attack_images if self.facing_right else self.flipped_attack_images
            self.last_attack_time = current_time

    def take_damage(self, damage):
        current_time = pygame.time.get_ticks()

        # Spawn blood splash effect at the entity's position
        blood_effect = BloodSplashEffect(self.rect.centerx, self.rect.centery)
        all_sprites.add(blood_effect)

        if self.is_dying:
            return

        self.health -= damage  # This line should ALWAYS execute regardless of damage source

        # Only apply knockback and animation for non-ultimate damage
        if not (isinstance(player, Samurai2) and player.ulti_active):
            self.last_hurt_time = current_time
            if player.facing_right:
                self.rect.x += 0.5
            else:
                self.rect.x -= 1.5

            if self.health > 0:
                self.currentImages = self.hurt_images if self.facing_right else self.flipped_hurt_images
                self.currentImageIndex = 0
        else:
            # Ultimate damage specific handling
            if self.health > 0:
                # Optional: Add visual feedback for ultimate damage
                red_flash = self.image.copy()
                red_overlay = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
                red_overlay.fill((255, 0, 0, 150))
                red_flash.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                self.image = red_flash
                self.flash_time = current_time + 100

        if self.health <= 0:
            self.die()

    def die(self):
        self.is_dying = True
        bossskill_channel = pygame.mixer.Channel(4)
        bossskill_channel.set_volume(1)
        bossskill_channel.play(bossdeadsound)
        self.currentImages = self.dead_images if self.facing_right else self.flipped_dead_images
        self.currentImageIndex = 0

    def update(self, player):
        if self.is_dying:
            if self.currentImageIndex < len(self.dead_images) - 1:
                self.animationCounter += 1
                if self.animationCounter % 20 == 0:
                    self.currentImageIndex += 1
                    self.image = self.dead_images[self.currentImageIndex]
            else:
                self.kill()  # Remove from all groups
                bosses.remove(self)

        current_time = pygame.time.get_ticks()

        if current_time - self.last_skill_time >= self.skill_cooldown:
            self.use_star_skill()
            self.last_skill_time = current_time  # Reset cooldown
        # Handle hurt animation completion
        if self.currentImages in [self.hurt_images, self.flipped_hurt_images]:
            if self.currentImageIndex >= len(self.hurt_images) - 1:
                # Reset to movement state after hurt animation
                self.currentImages = self.walk_images if self.facing_right else self.flipped_walk_images
                self.currentImageIndex = 0

        # Only update movement/attack if not in hurt state
        if current_time - self.last_hurt_time >= self.hurt_cooldown:
            dx = abs(player.rect.centerx - self.rect.centerx)
            dy = abs(player.rect.centery - self.rect.centery)

            if dx < 150 and dy < 100:
                self.attack()
            else:
                self.move_towards_player(player)

        # Animation updates
        self.animationCounter += 1
        if self.animationCounter % 5 == 0:
            self.currentImageIndex = (self.currentImageIndex + 1) % len(self.currentImages)
            self.image = self.currentImages[self.currentImageIndex]

        # Reset attack state
        if self.is_attacking and self.currentImageIndex >= len(self.currentImages) - 1:
            self.is_attacking = False


class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, variant):
        super().__init__()
        self.variant = variant
        if self.variant == 1:
            self.idle_images = zombie1idle
            self.walk_images = zombie1walk
            self.attack_images = zombie1attack
            self.hurt_images = zombie1hurt
            self.dead_images = zombie1dead
        else:
            self.idle_images = zombie2idle
            self.walk_images = zombie2walk
            self.attack_images = zombie2attack
            self.hurt_images = zombie2hurt
            self.dead_images = zombie2dead

        self.flipped_idle_images = [pygame.transform.flip(img, True, False) for img in self.idle_images]
        self.flipped_walk_images = [pygame.transform.flip(img, True, False) for img in self.walk_images]
        self.flipped_attack_sets = [pygame.transform.flip(img, True, False) for img in self.attack_images]
        self.flipped_hurt_images = [pygame.transform.flip(img, True, False) for img in self.hurt_images]
        self.flipped_dead_images = [pygame.transform.flip(img, True, False) for img in self.dead_images]

        self.currentImages = self.idle_images
        self.currentImageIndex = 0
        self.image = self.currentImages[self.currentImageIndex]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.animationCounter = 0
        self.speed = randint(3, 6)
        self.health = ZOMBIEHEALTH + HEALTHPERWAVE
        self.is_attacking = False
        self.last_attack_time = 0
        self.is_dying = False  # Track death animation state

    def move_towards_player(self, player):
        if self.health <= 0 or self.is_dying:
            return
        dx = player.rect.centerx - self.rect.centerx

        # Flip the zombie's images based on dx
        if dx < 0:  # Zombie is on the left of the player
            self.currentImages = self.flipped_idle_images if self.currentImages == self.idle_images else self.flipped_walk_images
        else:  # Zombie is on the right of the player
            self.currentImages = self.idle_images if self.currentImages == self.flipped_idle_images else self.walk_images

        dy = player.rect.centery - self.rect.centery
        dist = (dx ** 2 + dy ** 2) ** 0.5
        if dist != 0:
            self.rect.x += int(self.speed * dx / dist)
            self.rect.y += int(self.speed * dy / dist)

    def attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= ATTACK_COOLDOWN:
            zombie_channel = pygame.mixer.Channel(2)
            zombie_channel.set_volume(0.2)
            if not zombie_channel.get_busy():
                zombie_channel.play(zombieattacksound)
            self.is_attacking = True
            self.currentImageIndex = 0

            # Check if the zombie is facing left or right based on dx
            if self.rect.centerx < player.rect.centerx:  # Zombie is facing right (player is to the left)
                self.currentImages = self.attack_images
            else:  # Zombie is facing left (player is to the right)
                self.currentImages = self.flipped_attack_sets

            self.last_attack_time = current_time

    def take_damage(self, damage):
        # Spawn blood splash effect at the entity's position
        blood_effect = BloodSplashEffect(self.rect.centerx, self.rect.centery)
        all_sprites.add(blood_effect)

        if self.health <= 0 or self.is_dying:
            return

        self.health -= damage
        if self.health > 0:
            # Check if the zombie is facing left or right based on dx
            if self.rect.centerx < player.rect.centerx:  # Zombie is facing right (player is to the left)
                self.currentImages = self.hurt_images
            else:  # Zombie is facing left (player is to the right)
                self.currentImages = self.flipped_hurt_images
            self.currentImageIndex = 0

            # **Create a red flash effect**
            red_flash = self.image.copy()
            red_overlay = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            red_overlay.fill((255, 0, 0, 150))  # Red tint with transparency
            red_flash.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            self.image = red_flash  # Apply red effect

            # Schedule reverting to normal image after a short time
            self.flash_time = pygame.time.get_ticks() + 100

            # Knockback effect
            if self.rect.centerx < player.rect.centerx:  # Zombie is facing right
                self.rect.x -= KNOCKBACK
            else:  # Zombie is facing left
                self.rect.x += KNOCKBACK

        else:
            self.die()

    def die(self):
        self.is_dying = True
        zombiedead1sound.set_volume(0.2)
        zombiedead2sound.set_volume(0.2)
        random.choice([zombiedead1sound, zombiedead2sound]).play()

        # Check if the zombie is facing left or right based on dx
        if self.rect.centerx < player.rect.centerx:  # Zombie is facing right (player is to the left)
            self.currentImages = self.dead_images
        else:  # Zombie is facing left (player is to the right)
            self.currentImages = self.flipped_dead_images

        self.currentImageIndex = 0

    def update(self, player):
        if self.is_dying:
            if self.currentImageIndex < len(self.currentImages) - 1:
                self.animationCounter += 1
                if self.animationCounter % 20 == 0:  # Adjust timing for smooth animation
                    self.currentImageIndex += 1
                    self.image = self.currentImages[self.currentImageIndex]
            else:
                zombies.remove(self)  # Remove zombie after full animation
                all_sprites.remove(self)
                spawnZombie(1)
            return  # Stop further updates

        elif self.health > 0:
            dx = abs(player.rect.centerx - self.rect.centerx)
            dy = abs(player.rect.centery - self.rect.centery)

            if dx < 150 and dy < 100:
                self.attack()
            else:
                self.move_towards_player(player)

        self.animationCounter += 1
        if self.animationCounter % 5 == 0:
            self.currentImageIndex = (self.currentImageIndex + 1) % len(self.currentImages)
            self.image = self.currentImages[self.currentImageIndex]


# -------------------------------------------------------------------------------------------------------------------------------------
# User Interface
def mainmenu():
    waiting = True
    pygame.mixer.stop()
    mainmenumusic.set_volume(0.5)
    mainmenumusic.play(-1)

    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))

    # Fade in
    for alpha in range(0, 255, 5):  # Increase alpha gradually
        screen.blit(menu, (0, 0))
        fade_surface.set_alpha(255 - alpha)  # Decrease fade effect
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)  # Delay to control speed

    while waiting:
        screen.fill((0, 0, 0))
        screen.blit(menu, (0, 0))

        # Display "Zombie Survival Game" text with outline
        font = pygame.font.Font(None, 100)
        title_text = "Zombie Survival Game"

        # Outline color (black)
        outline_color = (0, 0, 0)
        # Main text color (gold)
        text_color = (255, 255, 255)

        # Render the text surface
        text_surface = font.render(title_text, True, text_color)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))

        # Create outline by rendering multiple black versions around the text
        for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2), (0, -2), (0, 2), (-2, 0), (2, 0)]:
            outline_surface = font.render(title_text, True, outline_color)
            outline_rect = outline_surface.get_rect(center=(text_rect.centerx + dx, text_rect.centery + dy))
            screen.blit(outline_surface, outline_rect)

        # Render the main text on top
        screen.blit(text_surface, text_rect)

        # Button dimensions
        button_width = 300
        button_height = 80

        # Positions
        button_x = (SCREEN_WIDTH - button_width) // 2
        button_y_try_again = SCREEN_HEIGHT // 2
        button_y_exit = SCREEN_HEIGHT // 2 + 120  # Position Exit button below Try Again

        # Draw "Try Again" button
        pygame.draw.rect(screen, (50, 50, 50), (button_x, button_y_try_again, button_width, button_height))
        pygame.draw.rect(screen, (255, 255, 255), (button_x, button_y_try_again, button_width, button_height), 5)
        button_font = pygame.font.Font(None, 60)
        button_text_try_again = button_font.render("Start", True, (255, 255, 255))
        button_text_rect_try_again = button_text_try_again.get_rect(
            center=(button_x + button_width // 2, button_y_try_again + button_height // 2))
        screen.blit(button_text_try_again, button_text_rect_try_again)

        # Draw "Exit" button
        pygame.draw.rect(screen, (50, 50, 50), (button_x, button_y_exit, button_width, button_height))
        pygame.draw.rect(screen, (255, 255, 255), (button_x, button_y_exit, button_width, button_height), 5)
        button_text_exit = button_font.render("Exit", True, (255, 255, 255))
        button_text_rect_exit = button_text_exit.get_rect(
            center=(button_x + button_width // 2, button_y_exit + button_height // 2))
        screen.blit(button_text_exit, button_text_rect_exit)

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Highlight and check for clicks on "Try Again"
        if button_x < mouse_x < button_x + button_width and button_y_try_again < mouse_y < button_y_try_again + button_height:
            pygame.draw.rect(screen, (80, 80, 80), (button_x, button_y_try_again, button_width, button_height))
            screen.blit(button_text_try_again, button_text_rect_try_again)

        # Highlight and check for clicks on "Exit"
        if button_x < mouse_x < button_x + button_width and button_y_exit < mouse_y < button_y_exit + button_height:
            pygame.draw.rect(screen, (80, 80, 80), (button_x, button_y_exit, button_width, button_height))
            screen.blit(button_text_exit, button_text_rect_exit)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if button_x < mouse_x < button_x + button_width and button_y_try_again < mouse_y < button_y_try_again + button_height:
                        selectionsound.play()
                        pygame.time.delay(200)
                        waiting = False

                        # Fade out
                        for alpha in range(0, 255, 5):  # Increase alpha
                            fade_surface.set_alpha(alpha)  # Increase fade effect
                            screen.blit(menu, (0, 0))
                            screen.blit(fade_surface, (0, 0))
                            pygame.display.update()
                            pygame.time.delay(10)  # Delay for smooth transition

                    if button_x < mouse_x < button_x + button_width and button_y_exit < mouse_y < button_y_exit + button_height:
                        selectionsound.play()
                        pygame.time.delay(200)
                        pygame.quit()
                        sys.exit()

        # Update the display
        pygame.display.update()


def helpscreen():
    waiting = True
    while waiting:
        screen.blit(helptips, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

        pygame.display.flip()


def skillSelection(round, selected_skill1, selected_skill2, selected_skill3, selected_skill4):
    global camera_x, camera_y

    # Set correct background based on the round
    background = background2 if round == 5 else background1

    # Recenter player to the middle of the game background (not just screen)
    player.rect.center = (MAP_WIDTH // 2, MAP_HEIGHT // 2)
    camera_x = player.rect.centerx - SCREEN_WIDTH // 2
    camera_y = player.rect.centery - SCREEN_HEIGHT // 2

    # Define positions for the four potions relative to the player's new centered position
    offset = 250  # Distance from the center for potion placement
    center_x, center_y = player.rect.center

    # **Create potion objects using the Potion class (Ensure correct positions)**
    potion_north = Potion("Assets\\Potions\\1.png", center_x, center_y - offset)
    potion_east = Potion("Assets\\Potions\\0.png", center_x + offset, center_y)
    potion_west = Potion("Assets\\Potions\\3.png", center_x - offset, center_y)
    potion_south = Potion("Assets\\Potions\\2.png", center_x, center_y + offset)  # Water potion

    if round == 1:
        # **Create a sprite group for potions**
        potions = pygame.sprite.Group(potion_north, potion_east, potion_west, potion_south)
        skills = {
            "NORTH": "Transform - Tranform into a big samurai for a short duration",
            "EAST": "Fireball - Unleashes a powerful ranged attack",
            "SOUTH": "Water - Does Nothing(?)",
            "WEST": "Dash Attack - Dash and cuts enemies in between"
        }

    elif round == 2:
        # **Create a sprite group for potions**
        potions = pygame.sprite.Group(potion_north, potion_east, potion_west, potion_south)
        skills = {
            "NORTH": "Intelligence - Increases Hp",
            "EAST": "Agility - Increases Speed",
            "SOUTH": "Water - Does Nothing(?)",
            "WEST": "Strength - Increases Attack"
        }



    elif round == 3:
        # **Create a sprite group for potions**
        potions = pygame.sprite.Group(potion_north, potion_east, potion_west, potion_south)
        if selected_skill1 == "Transform - Tranform into a big samurai for a short duration":
            skills = {
                "NORTH": "Well-Rested - Improved Recovery",
                "EAST": "Fireball - Unleashes a powerful ranged attack",
                "SOUTH": "Water - Does Nothing(?)",
                "WEST": "Dash Attack - Dash and cuts enemies in between"
            }
        elif selected_skill1 == "Dash Attack - Dash and cuts enemies in between":
            skills = {
                "NORTH": "Transform - Tranform into a big samurai for a short duration",
                "EAST": "Fireball - Unleashes a powerful ranged attack",
                "SOUTH": "Water - Does Nothing(?)",
                "WEST": "Smoke Screen - Increases invulnerable time after getting hit"
            }
        else:
            skills = {
                "NORTH": "Transform - Tranform into a big samurai for a short duration",
                "EAST": "Power Knockback - Improves Knockback",
                "SOUTH": "Water - Does Nothing(?)",
                "WEST": "Dash Attack - Dash and cuts enemies in between"
            }


    elif round == 4:
        # **Create a sprite group for potions**
        potions = pygame.sprite.Group(potion_north, potion_east, potion_west, potion_south)
        if selected_skill2 == "Intelligence - Increases Hp":
            skills = {
                "NORTH": "Well-Rested - Improved Recovery",
                "EAST": "Agility - Increases Speed",
                "SOUTH": "Water - Does Nothing(?)",
                "WEST": "Strength - Increases Attack"
            }
        elif selected_skill2 == "Agility - Increases Speed":
            skills = {
                "NORTH": "Intelligence - Increases Hp",
                "EAST": "Smoke Screen - Increases invulnerable time after getting hit",
                "SOUTH": "Water - Does Nothing(?)",
                "WEST": "Strength - Increases Attack"
            }
        else:
            skills = {
                "NORTH": "Intelligence - Increases Hp",
                "EAST": "Agility - Increases Speed",
                "SOUTH": "Water - Does Nothing(?)",
                "WEST": "Power Knockback - Improves Knockback"
            }

    # **Map skills to potion positions**
    potion_skills = {
        potion_north: skills["NORTH"],
        potion_east: skills["EAST"],
        potion_west: skills["WEST"],
        potion_south: skills["SOUTH"]
    }

    selected_skill = None
    clock = pygame.time.Clock()
    selection_made = False

    while not selection_made:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_j:
                for potion, skill in potion_skills.items():
                    if player.rect.colliderect(potion.rect):
                        selected_skill = skill
                        selection_made = True

        # **Allow player movement during skill selection**
        keys = pygame.key.get_pressed()
        player.update(keys)

        # **Update potion animations**
        potions.update()

        # **Draw background and elements**
        screen.blit(background, (-camera_x, -camera_y))

        # **Display "Choose an Ability" Text**
        font = pygame.font.SysFont(None, 80)
        text_surface = font.render("Choose an Ability", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(text_surface, text_rect)

        # **Draw Potions Relative to the Camera**
        for potion in potions:
            potion.draw(screen, camera_x, camera_y)  # Adjust potion draw to account for camera position

        # **Draw Player Relative to Camera**
        screen.blit(player.image, (player.rect.x - camera_x, player.rect.y - camera_y))

        # **Display Skill Name When Colliding With a Potion**
        font = pygame.font.SysFont(None, 30)
        collision_text = ""
        for potion, skill in potion_skills.items():
            if player.rect.colliderect(potion.rect):
                collision_text = skill

        if collision_text:
            text_surface = font.render(f"{collision_text}", True, (255, 255, 255))
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT - 100))

        pygame.display.flip()
        clock.tick(60)
    print(selected_skill)
    return selected_skill  # Returns the selected skill


def draw_cooldown_indicators(screen, player):
    current_time = pygame.time.get_ticks()

    # Define indicator size and positioning
    indicator_width = 50
    indicator_height = 10
    padding_right = 20
    padding_bottom = 20
    spacing = 10

    # Define base position for the first indicator
    x1 = SCREEN_WIDTH - indicator_width - padding_right
    y1 = SCREEN_HEIGHT - indicator_height - padding_bottom

    # Skill 1 (Dash Attack) indicator
    if player.skill1_learned:
        elapsed1 = current_time - player.last_skill1_time
        remaining1 = max(0, player.skill1_cooldown - elapsed1)
        ratio1 = remaining1 / player.skill1_cooldown if player.skill1_cooldown else 0
        pygame.draw.rect(screen, (100, 100, 100), (x1, y1, indicator_width, indicator_height))
        pygame.draw.rect(screen, (0, 0, 255), (x1, y1, indicator_width * (1 - ratio1), indicator_height))
        pygame.draw.rect(screen, (255, 255, 255), (x1, y1, indicator_width, indicator_height), 2)

    # For Skill 2, define its position regardless of whether Skill 1 is learned
    x2 = x1
    y2 = y1 - indicator_height - spacing
    if player.skill2_learned:
        elapsed2 = current_time - player.last_skill2_time
        remaining2 = max(0, player.skill2_cooldown - elapsed2)
        ratio2 = remaining2 / player.skill2_cooldown if player.skill2_cooldown else 0
        pygame.draw.rect(screen, (100, 100, 100), (x2, y2, indicator_width, indicator_height))
        pygame.draw.rect(screen, (0, 255, 0), (x2, y2, indicator_width * (1 - ratio2), indicator_height))
        pygame.draw.rect(screen, (255, 255, 255), (x2, y2, indicator_width, indicator_height), 2)

    # For the Transform skill indicator, define its position as well
    x3 = x1
    y3 = y2 - indicator_height - spacing
    if player.Transform_learned:
        elapsed_t = current_time - player.last_transform_time
        remaining_t = max(0, player.transform_cooldown - elapsed_t)
        ratio_t = remaining_t / player.transform_cooldown if player.transform_cooldown else 0
        pygame.draw.rect(screen, (100, 100, 100), (x3, y3, indicator_width, indicator_height))
        pygame.draw.rect(screen, (128, 0, 128), (x3, y3, indicator_width * (1 - ratio_t), indicator_height))
        pygame.draw.rect(screen, (255, 255, 255), (x3, y3, indicator_width, indicator_height), 2)


def draw_timer(screen, time_left):
    font = pygame.font.Font(None, 80)
    timer_text = font.render(f"{time_left}", True, (255, 255, 255))
    text_rect = timer_text.get_rect(center=(screen.get_width() // 2, 50))
    screen.blit(timer_text, text_rect)


def draw_wave(screen, round):
    font = pygame.font.Font(None, 80)
    wave_text = font.render(f"Wave {round}", True, (255, 255, 255))
    text_rect = wave_text.get_rect(center=(screen.get_width() - 120, 50))
    screen.blit(wave_text, text_rect)


def gameplay(round):
    if not player.health == 0 or not player.death_animation_finished:
        player.update(keys)

        # Attack hitbox sizes
        PLAYER_HITBOX_WIDTH = 80  # Attack range in width
        PLAYER_HITBOX_HEIGHT = 100  # Attack range in height
        ZOMBIE_HITBOX_WIDTH = 50  # Attack range for zombies
        ZOMBIE_HITBOX_HEIGHT = 100

        ATTACK_HITBOX_DELAY = 1000  # Delay in milliseconds (adjust as needed)

        for boss in list(bosses):
            boss.update(player)
            if boss.is_attacking and boss.rect.colliderect(player.rect):
                player.take_damage(1)

        # Boss takes damage from player attacks
        for boss in list(bosses):
            if player.is_attacking and player.rect.colliderect(boss.rect):
                boss.take_damage(1)  # Adjust damage value as needed
        for sprite in all_sprites:
            if isinstance(sprite, (SwordFireEffect, WaterExplosionEffect, TransformationEffect,
                                   ExplosionEffect, WaterEffect, WaterfallEffect, SliceEffect,
                                   Fire2Effect, Fire3Effect, StarEffect)):
                # Check collision FIRST
                for boss in bosses:
                    if pygame.sprite.collide_rect(sprite, boss):
                        if not (isinstance(sprite, StarEffect) and sprite.is_boss_skill):
                            boss.take_damage(sprite.damage / 2)

                # Then update the sprite
                sprite.update()

        # Update zombies and handle interactions
        for zombie in list(zombies):
            zombie.update(player)

            # **Zombie Attack Hitbox**
            if zombie.is_attacking and not hasattr(zombie, "attack_start_time"):
                zombie.attack_start_time = pygame.time.get_ticks()  # Store attack start time

            # **Check if Zombie Attack Hitbox Should Appear**
            if zombie.is_attacking and hasattr(zombie, "attack_start_time"):
                if pygame.time.get_ticks() - zombie.attack_start_time >= ATTACK_HITBOX_DELAY:
                    if zombie.rect.centerx < player.rect.centerx:
                        zombie_hitbox = pygame.Rect(zombie.rect.right, zombie.rect.top,
                                                    ZOMBIE_HITBOX_WIDTH, ZOMBIE_HITBOX_HEIGHT)
                    else:
                        zombie_hitbox = pygame.Rect(zombie.rect.left - ZOMBIE_HITBOX_WIDTH, zombie.rect.top,
                                                    ZOMBIE_HITBOX_WIDTH, ZOMBIE_HITBOX_HEIGHT)

                    # **Zombie Attacks**: If player is inside the zombie's attack hitbox, take damage
                    if zombie.is_attacking and player.rect.colliderect(zombie_hitbox):
                        player.take_damage(1)

                    del zombie.attack_start_time

            # Determine player's facing direction based on movement (assuming player has `facing` attribute)
            if player.rect.centerx < zombie.rect.centerx:
                player_facing_right = True  # Player is facing right (zombie is to the right)
            else:
                player_facing_right = False  # Player is facing left (zombie is to the left)

            # **Player Attack Hitbox**
            if player_facing_right:
                player_hitbox = pygame.Rect(player.rect.right, player.rect.top,
                                            PLAYER_HITBOX_WIDTH, PLAYER_HITBOX_HEIGHT)
            else:
                player_hitbox = pygame.Rect(player.rect.left - PLAYER_HITBOX_WIDTH, player.rect.top,
                                            PLAYER_HITBOX_WIDTH, PLAYER_HITBOX_HEIGHT)

            # **Player Attacks**: If a zombie is inside the player's attack hitbox, it takes damage
            if player.is_attacking and zombie.rect.colliderect(player_hitbox):
                Zombie.take_damage(zombie, damage)

        # Remove dead zombies (health <= 0) from groups
        for zombie in list(zombies):
            if zombie.health <= 0:
                zombie.update(zombie)

        # Draw everything with camera offset
        if round == 5:
            screen.blit(background2, (-camera_x, -camera_y))
            draw_cooldown_indicators(screen, player)
            draw_timer(screen, countdown)
            player.draw_health_bar(screen)
            draw_wave(screen, round)
            for sprite in all_sprites:
                if isinstance(sprite, (WaterExplosionEffect, ChargingEffect, TransformationEffect,
                                       ExplosionEffect, WaterEffect, WaterfallEffect, SliceEffect,
                                       Fire2Effect, Fire3Effect, StarEffect, HeartEffect, BloodSplashEffect)):
                    sprite.update()
                screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y - camera_y))
        else:
            screen.blit(background1, (-camera_x, -camera_y))
            draw_cooldown_indicators(screen, player)
            draw_timer(screen, countdown)
            player.draw_health_bar(screen)
            draw_wave(screen, round)
            for sprite in all_sprites:
                if isinstance(sprite, (WaterExplosionEffect, ChargingEffect, TransformationEffect,
                                       ExplosionEffect, WaterEffect, WaterfallEffect, SliceEffect,
                                       Fire2Effect, Fire3Effect, StarEffect, HeartEffect, BloodSplashEffect)):
                    sprite.update()
                screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y - camera_y))

    elif player.death_animation_finished:
        waiting = True
        pygame.mixer.stop()
        gameovermusic.set_volume(0.3)
        gameovermusic.play(-1)
        while waiting:  # Pause the game during game over screen
            screen.fill((0, 0, 0))

            # Display "GAME OVER" text
            font = pygame.font.Font(None, 100)
            text = font.render("GAME OVER", True, (255, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            screen.blit(text, text_rect)

            # Button dimensions
            button_width = 300
            button_height = 80

            # Positions
            button_x = (SCREEN_WIDTH - button_width) // 2
            button_y_try_again = SCREEN_HEIGHT // 2
            button_y_exit = SCREEN_HEIGHT // 2 + 120  # Position Exit button below Try Again

            # Draw "Try Again" button
            pygame.draw.rect(screen, (50, 50, 50), (button_x, button_y_try_again, button_width, button_height))
            pygame.draw.rect(screen, (255, 255, 255), (button_x, button_y_try_again, button_width, button_height), 5)
            button_font = pygame.font.Font(None, 60)
            button_text_try_again = button_font.render("Try Again", True, (255, 255, 255))
            button_text_rect_try_again = button_text_try_again.get_rect(
                center=(button_x + button_width // 2, button_y_try_again + button_height // 2))
            screen.blit(button_text_try_again, button_text_rect_try_again)

            # Draw "Exit" button
            pygame.draw.rect(screen, (50, 50, 50), (button_x, button_y_exit, button_width, button_height))
            pygame.draw.rect(screen, (255, 255, 255), (button_x, button_y_exit, button_width, button_height), 5)
            button_text_exit = button_font.render("Exit", True, (255, 255, 255))
            button_text_rect_exit = button_text_exit.get_rect(
                center=(button_x + button_width // 2, button_y_exit + button_height // 2))
            screen.blit(button_text_exit, button_text_rect_exit)

            # Get mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Highlight and check for clicks on "Try Again"
            if button_x < mouse_x < button_x + button_width and button_y_try_again < mouse_y < button_y_try_again + button_height:
                pygame.draw.rect(screen, (80, 80, 80), (button_x, button_y_try_again, button_width, button_height))
                screen.blit(button_text_try_again, button_text_rect_try_again)

            # Highlight and check for clicks on "Exit"
            if button_x < mouse_x < button_x + button_width and button_y_exit < mouse_y < button_y_exit + button_height:
                pygame.draw.rect(screen, (80, 80, 80), (button_x, button_y_exit, button_width, button_height))
                screen.blit(button_text_exit, button_text_rect_exit)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        if button_x < mouse_x < button_x + button_width and button_y_try_again < mouse_y < button_y_try_again + button_height:
                            pygame.time.delay(200)
                            waiting = False
                            return True  # Restart game
                        if button_x < mouse_x < button_x + button_width and button_y_exit < mouse_y < button_y_exit + button_height:
                            pygame.time.delay(200)
                            pygame.quit()
                            sys.exit()

            # Update the display
            pygame.display.update()

    pygame.display.flip()
    clock.tick(60)


def wave(wave):
    if wave == 1:
        spawnZombie(5)

    elif wave == 2:
        spawnZombie(10)

    elif wave == 3:
        spawnZombie(15)

    elif wave == 4:
        spawnZombie(20)

    elif wave == 5:
        spawnZombie(20)
        spawnBoss()
    else:
        pass


def spawnZombie(ENEMY_LIMIT):  # Spawn new zombies after a zombie death event is triggered
    for _ in range(ENEMY_LIMIT):
        corner = random.choice([1, 2, 3, 4])
        if corner == 1:
            x, y = 0, 0
        elif corner == 2:
            x, y = MAP_WIDTH, 0
        elif corner == 3:
            x, y = 0, MAP_HEIGHT
        elif corner == 4:
            x, y = MAP_WIDTH, MAP_HEIGHT

        variant = random.choice([1, 2])
        zombie = Zombie(x, y, variant)
        zombies.add(zombie)
        all_sprites.add(zombie)


def spawnBoss():
    # Spawn boss
    boss = Boss(MAP_WIDTH, 0)
    bosses.add(boss)
    all_sprites.add(boss)


def draw_text(surface, text, position, color=(255, 255, 255), speed=0.05):
    # Font settings
    font = pygame.font.Font(None, 32)  # Use a default font

    x, y = position
    words = ""
    for letter in text:
        words += letter
        render_text = font.render(words, True, color)
        surface.blit(render_text, (x, y))
        pygame.display.update()
        time.sleep(speed)


def Story1():
    pygame.mixer.stop()
    dialogmusic1.set_volume(0.2)
    dialogmusic1.play(-1)
    # Load assets
    background = pygame.image.load("Assets\\Menu.png")  # Replace with your background image
    character_left = pygame.image.load("Assets\\Samurai\\Idle\\0.png")  # Left character portrait
    character_right = pygame.image.load("Assets\\Zombie1\\Idle\\0.png")  # Right character portrait

    # Scale images
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    character_left = pygame.transform.scale(character_left, (200, 300))
    rightcharacter = pygame.transform.scale(character_right, (200, 300))
    right_character_flipped = pygame.transform.flip(rightcharacter, True, False)

    font = pygame.font.Font(None, 32)  # Use a default font
    # Dialogue data
    dialogues = [
        {"name": "Narrator", "text": "In a forest.", "side": "none"},
        {"name": "Samurai", "text": "Where am I...? Am I lost again?", "side": "left"},
        {"name": "Samurai", "text": "I guess I have to find a way out...", "side": "left"},
        {"name": "Zombie", "text": "Roar!", "side": "right"},
        {"name": "Samurai", "text": "What are those??!!", "side": "left"},
        {"name": "Zombie", "text": "ROAR ROAR ROAR!!!", "side": "right"},
        {"name": "Samurai", "text": "Well then, TRY ME!", "side": "left"},
    ]
    running = True
    dialogue_index = 0

    while running and dialogue_index < len(dialogues):
        screen.blit(background, (0, 0))  # Draw background

        current_dialogue = dialogues[dialogue_index]

        # Draw character portraits
        if current_dialogue["side"] == "none":
            pass
        elif current_dialogue["side"] == "left":
            screen.blit(character_left, (50, 300))  # Left character
        else:
            screen.blit(right_character_flipped, (800, 300))  # Right character

        # ** Draw a full black dialogue box **
        pygame.draw.rect(screen, (0, 0, 0), (0, SCREEN_HEIGHT - 250, SCREEN_WIDTH, 250))  # Black box
        pygame.draw.rect(screen, (255, 255, 255), (0, SCREEN_HEIGHT - 250, SCREEN_WIDTH, 250), 3)  # White border

        # Draw name
        name_text = font.render(f" {current_dialogue['name']} ", True, (255, 255, 0))
        screen.blit(name_text, (60, SCREEN_HEIGHT - 240))

        # Display text letter by letter
        draw_text(screen, current_dialogue["text"], (60, SCREEN_HEIGHT - 200))

        spacebar_text = font.render("Press SPACEBAR to continue", True, (200, 200, 200))
        screen.blit(spacebar_text, (SCREEN_WIDTH - 350, SCREEN_HEIGHT - 40))  # Bottom right corner
        pygame.display.update()

        # Wait for player input (press spacebar to continue)
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Press space to continue dialogue
                        dialogue_index += 1
                        waiting = False

        pygame.display.update()


def Story2():
    # Load assets
    background = pygame.image.load("Assets\\Menu.png")  # Replace with your background image
    character_left = pygame.image.load("Assets\\Samurai\\Idle\\0.png")  # Left character portrait
    character_right = pygame.image.load("Assets\\Boss\\Idle\\Idle.png")  # Right character portrait

    # Scale images
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    character_left = pygame.transform.scale(character_left, (200, 300))
    rightcharacter = pygame.transform.scale(character_right, (400, 400))
    right_character_flipped = pygame.transform.flip(rightcharacter, True, False)

    font = pygame.font.Font(None, 32)  # Use a default font
    # Dialogue data
    dialogues = [
        {"name": "Samurai", "text": "What is that sound?", "side": "left"},
        {"name": "Samurai", "text": "And WHO is that??", "side": "left"},
        {"name": "Boss", "text": "Hi cutie... Good job holding out until now.", "side": "right"},
        {"name": "Samurai", "text": "Who are you calling cutie?? And who are you??", "side": "left"},
        {"name": "Boss", "text": "As a reward, I will grant you... DEATH!", "side": "right"},
        {"name": "Samurai", "text": "I guess communication is meaningless. BRING IT ON!", "side": "left"}
    ]
    running = True
    dialogue_index = 0

    while running and dialogue_index < len(dialogues):
        screen.blit(background, (0, 0))  # Draw background

        current_dialogue = dialogues[dialogue_index]

        # Draw character portraits
        if current_dialogue["side"] == "left":
            screen.blit(character_left, (50, 300))  # Left character
        else:
            screen.blit(right_character_flipped, (650, 250))  # Right character

        # ** Draw a full black dialogue box **
        pygame.draw.rect(screen, (0, 0, 0), (0, SCREEN_HEIGHT - 250, SCREEN_WIDTH, 250))  # Black box
        pygame.draw.rect(screen, (255, 255, 255), (0, SCREEN_HEIGHT - 250, SCREEN_WIDTH, 250), 3)  # White border

        # Draw name
        name_text = font.render(f" {current_dialogue['name']} ", True, (255, 255, 0))
        screen.blit(name_text, (60, SCREEN_HEIGHT - 240))

        # Display text letter by letter
        draw_text(screen, current_dialogue["text"], (60, SCREEN_HEIGHT - 200))

        spacebar_text = font.render("Press SPACEBAR to continue", True, (200, 200, 200))
        screen.blit(spacebar_text, (SCREEN_WIDTH - 350, SCREEN_HEIGHT - 40))  # Bottom right corner
        pygame.display.update()

        # Wait for player input (press spacebar to continue)
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Press space to continue dialogue
                        dialogue_index += 1
                        waiting = False

        pygame.display.update()


def Story3():
    pygame.mixer.stop()
    dialogmusic1.set_volume(0.2)
    dialogmusic1.play(-1)
    # Load assets
    background = pygame.image.load("Assets\\Menu.png")  # Replace with your background image
    character_left = pygame.image.load("Assets\\Samurai\\Idle\\0.png")  # Left character portrait
    character_right = pygame.image.load("Assets\\Boss\\Idle\\Idle.png")  # Right character portrait

    # Scale images
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    character_left = pygame.transform.scale(character_left, (200, 300))
    rightcharacter = pygame.transform.scale(character_right, (400, 400))
    right_character_flipped = pygame.transform.flip(rightcharacter, True, False)

    font = pygame.font.Font(None, 32)  # Use a default font
    # Dialogue data
    dialogues = [
        {"name": "Boss", "text": "AAAAAaa... Dies*", "side": "right"},
        {"name": "Samurai", "text": "Too easy, no challenge.", "side": "left"},
        {"name": "Samurai", "text": "I am still lost though... Need to find a way out...", "side": "left"},
        {"name": "Narrator", "text": "After 2 hours of exploring...", "side": "none"},
        {"name": "Samurai", "text": "There is no exit... Am I stucked in this place?", "side": "left"},
        {"name": "Samurai", "text": "NOOOOOOOOOO...!", "side": "left"}
    ]
    running = True
    dialogue_index = 0

    while running and dialogue_index < len(dialogues):
        screen.blit(background, (0, 0))  # Draw background

        current_dialogue = dialogues[dialogue_index]

        # Draw character portraits
        if current_dialogue["side"] == "none":
            pass
        elif current_dialogue["side"] == "left":
            screen.blit(character_left, (50, 300))  # Left character
        else:
            screen.blit(right_character_flipped, (650, 250))  # Right character

        # ** Draw a full black dialogue box **
        pygame.draw.rect(screen, (0, 0, 0), (0, SCREEN_HEIGHT - 250, SCREEN_WIDTH, 250))  # Black box
        pygame.draw.rect(screen, (255, 255, 255), (0, SCREEN_HEIGHT - 250, SCREEN_WIDTH, 250), 3)  # White border

        # Draw name
        name_text = font.render(f" {current_dialogue['name']} ", True, (255, 255, 0))
        screen.blit(name_text, (60, SCREEN_HEIGHT - 240))

        # Display text letter by letter
        draw_text(screen, current_dialogue["text"], (60, SCREEN_HEIGHT - 200))

        spacebar_text = font.render("Press SPACEBAR to continue", True, (200, 200, 200))
        screen.blit(spacebar_text, (SCREEN_WIDTH - 350, SCREEN_HEIGHT - 40))  # Bottom right corner
        pygame.display.update()

        # Wait for player input (press spacebar to continue)
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Press space to continue dialogue
                        dialogue_index += 1
                        waiting = False

        pygame.display.update()


def victory():
    waiting = True
    pygame.mixer.stop()
    victorymusic.set_volume(0.5)
    victorymusic.play(-1)
    while waiting:  # Pause the game during game over screen
        screen.fill((0, 0, 0))

        # Display "VICTORY!" text
        font = pygame.font.Font(None, 100)
        text = font.render("VICTORY!", True, (0, 255, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(text, text_rect)

        # ** Display "Congratulations, you survived!" text **
        sub_font = pygame.font.Font(None, 50)  # Smaller font for subtitle
        sub_text = sub_font.render("Congratulations, you survived... for now", True, (255, 255, 255))
        sub_text_rect = sub_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 80))  # Slightly below "VICTORY!"
        screen.blit(sub_text, sub_text_rect)

        # Button dimensions
        button_width = 300
        button_height = 80

        # Positions
        button_x = (SCREEN_WIDTH - button_width) // 2
        button_y_try_again = SCREEN_HEIGHT // 2
        button_y_exit = SCREEN_HEIGHT // 2 + 120  # Position Exit button below Try Again

        # Draw "Try Again" button
        pygame.draw.rect(screen, (50, 50, 50), (button_x, button_y_try_again, button_width, button_height))
        pygame.draw.rect(screen, (255, 255, 255), (button_x, button_y_try_again, button_width, button_height), 5)
        button_font = pygame.font.Font(None, 60)
        button_text_try_again = button_font.render("Restart", True, (255, 255, 255))
        button_text_rect_try_again = button_text_try_again.get_rect(
            center=(button_x + button_width // 2, button_y_try_again + button_height // 2))
        screen.blit(button_text_try_again, button_text_rect_try_again)

        # Draw "Exit" button
        pygame.draw.rect(screen, (50, 50, 50), (button_x, button_y_exit, button_width, button_height))
        pygame.draw.rect(screen, (255, 255, 255), (button_x, button_y_exit, button_width, button_height), 5)
        button_text_exit = button_font.render("Exit", True, (255, 255, 255))
        button_text_rect_exit = button_text_exit.get_rect(
            center=(button_x + button_width // 2, button_y_exit + button_height // 2))
        screen.blit(button_text_exit, button_text_rect_exit)

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Highlight and check for clicks on "Try Again"
        if button_x < mouse_x < button_x + button_width and button_y_try_again < mouse_y < button_y_try_again + button_height:
            pygame.draw.rect(screen, (80, 80, 80), (button_x, button_y_try_again, button_width, button_height))
            screen.blit(button_text_try_again, button_text_rect_try_again)

        # Highlight and check for clicks on "Exit"
        if button_x < mouse_x < button_x + button_width and button_y_exit < mouse_y < button_y_exit + button_height:
            pygame.draw.rect(screen, (80, 80, 80), (button_x, button_y_exit, button_width, button_height))
            screen.blit(button_text_exit, button_text_rect_exit)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if button_x < mouse_x < button_x + button_width and button_y_try_again < mouse_y < button_y_try_again + button_height:
                        selectionsound.play()
                        pygame.time.delay(200)
                        waiting = False
                        return True  # Restart game
                    if button_x < mouse_x < button_x + button_width and button_y_exit < mouse_y < button_y_exit + button_height:
                        selectionsound.play()
                        pygame.time.delay(200)
                        pygame.quit()
                        sys.exit()

        # Update the display
        pygame.display.update()


# Game loop
ui_elements = pygame.sprite.Group()

mainmenu()
Story1()
helpscreen()
flag = 0
round = 1
damage = 1
selected_skill1 = ""
selected_skill2 = ""
selected_skill3 = ""
selected_skill4 = ""
while flag == 0:
    camera_x = SCREEN_WIDTH // 2
    camera_y = SCREEN_HEIGHT // 2

    damage = 1
    PLAYER_INVULNERABLE = 1000  # 1 second invulnerability after hit
    HEALTH = 5
    SPEED = 5
    KNOCKBACK = 10
    RECOVERYAMOUNT = 1
    WATER = 0
    HEALTHPERWAVE = 0

    skill1 = False
    skill2 = False
    Transform = False
    recovery = True

    countdown = 30

    pygame.mixer.stop()
    gamemusic.set_volume(0.3)
    gamemusic.play(-1)

    last_update_time = pygame.time.get_ticks()

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    bosses = pygame.sprite.Group()
    player = Player(skill1, skill2, Transform, recovery)
    all_sprites.add(player)

    zombies = pygame.sprite.Group()

    round = 1

    # Spawn 5 zombies at random positions (randomly choose variant 1 or 2)
    wave(round)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Calculate viewport size based on ultimate state
        if player.ulti_zoom and isinstance(player, Samurai2):
            current_viewport_width = int(BASE_SCREEN_WIDTH / ZOOM_FACTOR)
            current_viewport_height = int(BASE_SCREEN_HEIGHT / ZOOM_FACTOR)
        else:
            current_viewport_width = BASE_SCREEN_WIDTH
            current_viewport_height = BASE_SCREEN_HEIGHT

        desired_camera_x = player.rect.centerx - current_viewport_width // 2
        desired_camera_y = player.rect.centery - current_viewport_height // 2

        # Clamp camera position to map boundaries
        camera_x = max(0, min(MAP_WIDTH - current_viewport_width, desired_camera_x))
        camera_y = max(0, min(MAP_HEIGHT - current_viewport_height, desired_camera_y))

        # Create temporary render surface
        render_surface = pygame.Surface((current_viewport_width, current_viewport_height))

        # Draw background
        for sprite in all_sprites:
            render_surface.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y - camera_y))

        # Scale to screen size if zoomed
        if player.ulti_zoom and isinstance(player, Samurai2):
            scaled_surface = pygame.transform.scale(render_surface, (BASE_SCREEN_WIDTH, BASE_SCREEN_HEIGHT))
            screen.blit(scaled_surface, (0, 0))
        else:
            screen.blit(render_surface, (0, 0))

        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        # Decrease countdown every second
        if current_time - last_update_time >= 1000:
            countdown -= 1
            last_update_time = current_time

            # Update player and handle transition
            new_player = player.update(keys)
            if new_player:  # If transition occurred, replace the player
                player = new_player

            if active_transition_effect and active_transition_effect.done:
                new_player = player.transition_to_samurai2()
                all_sprites.remove(player)
                all_sprites.add(new_player)
                player = new_player
                player.is_transitioning = False  # Allow movement again
                active_transition_effect = None
            if active_transition_effect:
                active_transition_effect.update()

        result = gameplay(round)

        for sprite in all_sprites:
            screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y - camera_y))

        if result:
            break

        pygame.display.flip()

        if countdown <= 0:
            # **Trigger death animation for all zombies**
            for zombie in list(zombies):
                zombie.die()  # Set each zombie to play its death animation

            # **Display "SURVIVED" text**
            font = pygame.font.SysFont(None, 80)
            text_surface = font.render("SURVIVED", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))

            zombiedead1sound.set_volume(0.1)
            zombiedead2sound.set_volume(0.1)

            survived_channel = pygame.mixer.Channel(1)
            survived_channel.set_volume(1)
            survived_channel.play(survivedsound)

            survived_start_time = pygame.time.get_ticks()  # Get current time for delay
            survived_duration = 3000  # 3 seconds

            if round == 5:
                Story3()
                result = victory()

                if result:
                    break

            while pygame.time.get_ticks() - survived_start_time < survived_duration:
                # **Game continues running (no freeze)**
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                # **Allow player movement during "SURVIVED" phase**
                keys = pygame.key.get_pressed()
                player.update(keys)

                # **Update zombies (they will naturally finish their death animation)**
                zombies.update(player)

                # **Draw everything**
                if round >= 5:
                    screen.blit(background2, (-camera_x, -camera_y))
                else:
                    screen.blit(background1, (-camera_x, -camera_y))  # Keep showing background

                screen.blit(player.image, (player.rect.x - camera_x, player.rect.y - camera_y))  # Draw player

                # **Draw zombies (remove them when they finish dying)**
                for zombie in list(zombies):
                    if zombie.is_dying and zombie.currentImageIndex >= len(zombie.dead_images) - 1:
                        zombies.remove(zombie)  # Remove after death animation finishes
                        all_sprites.remove(zombie)
                    else:
                        screen.blit(zombie.image, (zombie.rect.x - camera_x, zombie.rect.y - camera_y))

                # **Show "SURVIVED" text**
                screen.blit(text_surface, text_rect)

                pygame.display.flip()
                clock.tick(60)  # Maintain FPS

            # **Proceed to Skill Selection**
            skill = skillSelection(round, selected_skill1, selected_skill2, selected_skill3, selected_skill4)
            potionsound.set_volume(1)
            potionsound.play()

            if round == 1:
                if skill == "Transform - Tranform into a big samurai for a short duration":
                    selected_skill1 = "Transform - Tranform into a big samurai for a short duration"
                    Transform = True
                elif skill == "Fireball - Unleashes a powerful ranged attack":
                    selected_skill1 = "Fireball - Unleashes a powerful ranged attack"
                    skill2 = True
                elif skill == "Dash Attack - Dash and cuts enemies in between":
                    selected_skill1 = "Dash Attack - Dash and cuts enemies in between"
                    skill1 = True
                else:
                    WATER += 1
            elif round == 2:
                if skill == "Intelligence - Increases Hp":
                    selected_skill2 = "Intelligence - Increases Hp"
                    HEALTH += 2
                elif skill == "Agility - Increases Speed":
                    selected_skill2 = "Agility - Increases Speed"
                    SPEED += 2
                elif skill == "Strength - Increases Attack":
                    selected_skill2 = "Strength - Increases Attack"
                    damage += 2
                else:
                    WATER += 1
            elif round == 3:
                if skill == "Well-Rested - Improved Recovery":
                    selected_skill3 = "Well-Rested - Improved Recovery"
                    RECOVERYAMOUNT += 1
                if skill == "Transform - Tranform into a big samurai for a short duration":
                    selected_skill3 = "Transform - Tranform into a big samurai for a short duration"
                    Transform = True
                elif skill == "Fireball - Unleashes a powerful ranged attack":
                    selected_skill3 = "Fireball - Unleashes a powerful ranged attack"
                    skill2 = True
                elif skill == "Dash Attack - Dash and cuts enemies in between":
                    selected_skill3 = "Dash Attack - Dash and cuts enemies in between"
                    skill1 = True
                elif skill == "Smoke Screen - Increases invulnerable time after getting hit":
                    selected_skill3 = "Smoke Screen - Increases invulnerable time after getting hit"
                    PLAYER_INVULNERABLE += 250
                elif skill == "Power Knockback - Improves Knockback":
                    selected_skill3 = "Power Knockback - Improves Knockback"
                    KNOCKBACK += 10
                else:
                    WATER += 1
            elif round == 4:
                if skill == "Well-Rested - Improved Recovery":
                    selected_skill4 = "Well-Rested - Improved Recovery"
                    RECOVERYAMOUNT += 1
                elif skill == "Intelligence - Increases Hp":
                    selected_skill4 = "Intelligence - Increases Hp"
                    HEALTH += 2
                elif skill == "Agility - Increases Speed":
                    selected_skill4 = "Agility - Increases Speed"
                    SPEED += 2
                elif skill == "Strength - Increases Attack":
                    selected_skill4 = "Strength - Increases Attack"
                    damage += 2
                elif skill == "Smoke Screen - Increases invulnerable time after getting hit":
                    selected_skill4 = "Smoke Screen - Increases invulnerable time after getting hit"
                    PLAYER_INVULNERABLE += 300
                elif skill == "Power Knockback - Improves Knockback":
                    selected_skill4 = "Power Knockback - Improves Knockback"
                    KNOCKBACK += 10
                else:
                    WATER += 1

            # Reset for the next round
            all_sprites = pygame.sprite.Group()
            player = Player(skill1, skill2, Transform, recovery)
            all_sprites.add(player)  # Re-add player
            camera_x = player.rect.centerx - SCREEN_WIDTH // 2
            camera_y = player.rect.centery - SCREEN_HEIGHT // 2
            zombies = pygame.sprite.Group()
            HEALTHPERWAVE += 3
            round += 1
            if round == 5:
                countdown = 60
                pygame.mixer.stop()
                bossmusic.set_volume(0.3)
                bossmusic.play(-1)
                Story2()
            else:
                countdown = 30
            wave(round)