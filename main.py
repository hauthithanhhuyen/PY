import pygame
import os
import random
from ship import Ship
from asteroid import Asteroid
from explosion import Explosion

# === Khởi tạo pygame ===
pygame.init()
pygame.mixer.init()

# Màn hình
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ASTROCRASH_PROJECT")
clock = pygame.time.Clock()

# === Load hình nền (có file ảnh đẹp do bạn cung cấp) ===
background_path = os.path.join("assets", "background.png")
if os.path.exists(background_path):
    background = pygame.image.load(background_path).convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
else:
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill((0, 0, 0))
    for _ in range(100):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        pygame.draw.circle(background, (0, 255, 255), (x, y), 1)

# === Nhạc nền ===
try:
    music_path = os.path.join("assets", "background.wav")
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    else:
        print(">> background.wav không tồn tại.")
except pygame.error as e:
    print(">> Lỗi phát nhạc nền:", e)

# === Âm thanh nổ ===
try:
    boom_path = os.path.join("assets", "boom.wav")
    if os.path.exists(boom_path):
        boom_sound = pygame.mixer.Sound(boom_path)
        boom_sound.set_volume(0.7)
    else:
        print(">> boom.wav không tồn tại.")
        boom_sound = None
except pygame.error as e:
    print(">> Lỗi phát âm thanh boom:", e)
    boom_sound = None

# Font hiển thị điểm
font = pygame.font.SysFont(None, 36)

# Hàm vẽ chữ
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    rect = text_obj.get_rect(topleft=(x, y))
    surface.blit(text_obj, rect)

# === Tạo các nhóm sprite ===
def reset_game():
    global ship, ship_group, missile_group, asteroid_group, explosion_group, score
    ship = Ship()
    ship_group = pygame.sprite.Group(ship)
    missile_group = pygame.sprite.Group()
    asteroid_group = pygame.sprite.Group()
    explosion_group = pygame.sprite.Group()
    for _ in range(5):
        asteroid_group.add(Asteroid())
    score = 0

reset_game()
running = True
game_over = False

# === Vòng lặp game ===
while running:
    clock.tick(60)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ship.shoot(missile_group)
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game()
                game_over = False

    if not game_over:
        ship.update(keys)
        missile_group.update()
        asteroid_group.update()
        explosion_group.update()

        # Va chạm tên lửa và thiên thạch
        hits = pygame.sprite.groupcollide(missile_group, asteroid_group, True, True)
        for hit in hits:
            if boom_sound:
                boom_sound.play()
            explosion_group.add(Explosion(hit.rect.centerx, hit.rect.centery))
            asteroid_group.add(Asteroid())
            score += 10

        # Va chạm tàu và thiên thạch
        if pygame.sprite.spritecollideany(ship, asteroid_group):
            if boom_sound:
                boom_sound.play()
            explosion_group.add(Explosion(ship.rect.centerx, ship.rect.centery))
            game_over = True

    # Vẽ nền và các sprite
    screen.blit(background, (0, 0))
    ship_group.draw(screen)
    missile_group.draw(screen)
    asteroid_group.draw(screen)
    explosion_group.draw(screen)

    # Vẽ điểm
    draw_text(f"Score: {score}", font, (255, 255, 255), screen, 10, 10)

    # Thông báo game over
    if game_over:
        draw_text("GAME OVER - Press R to Restart", font, (255, 0, 0), screen, WIDTH//2 - 150, HEIGHT//2)

    pygame.display.flip()

pygame.quit()
