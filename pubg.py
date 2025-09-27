import pygame
import random
import math
import sys

# init
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Mini Battle Royale (PUBG-like prototype)")

# colors
WHITE = (255, 255, 255)
GREEN = (50, 200, 50)
RED = (200, 50, 50)
BLUE = (50, 100, 200)

# player
player = pygame.Rect(WIDTH//2, HEIGHT//2, 30, 30)
player_speed = 5
bullets = []
bullet_speed = 9

# enemies
enemies = [pygame.Rect(random.randint(0, WIDTH), random.randint(0, HEIGHT), 30, 30) for _ in range(10)]
enemy_speed = 2

# shrinking safe zone
safe_radius = 400
shrink_rate = 0.05

font = pygame.font.SysFont(None, 28)
score = 0

def draw():
    screen.fill((30, 30, 40))
    
    # safe zone
    pygame.draw.circle(screen, (0,100,0), (WIDTH//2, HEIGHT//2), int(safe_radius), 3)

    # player
    pygame.draw.rect(screen, BLUE, player)

    # bullets
    for b in bullets:
        pygame.draw.circle(screen, WHITE, (b.x, b.y), 5)

    # enemies
    for e in enemies:
        pygame.draw.rect(screen, RED, e)

    # HUD
    txt = font.render(f"Enemies left: {len(enemies)}  Score: {score}", True, WHITE)
    screen.blit(txt, (10, 10))

    pygame.display.flip()

def move_enemies():
    for e in enemies:
        dx = player.centerx - e.centerx
        dy = player.centery - e.centery
        dist = math.hypot(dx, dy)
        if dist != 0:
            e.x += int(enemy_speed * dx/dist)
            e.y += int(enemy_speed * dy/dist)

def handle_bullets():
    global score
    for b in bullets[:]:
        b.x += b.vx
        b.y += b.vy
        if not (0 <= b.x <= WIDTH and 0 <= b.y <= HEIGHT):
            bullets.remove(b)
            continue
        for e in enemies[:]:
            if e.collidepoint(b.x, b.y):
                enemies.remove(e)
                score += 1
                if b in bullets: bullets.remove(b)
                break

def shrink_zone():
    global safe_radius
    safe_radius -= shrink_rate
    if safe_radius < 50: safe_radius = 50
    # damage player if outside
    dx = player.centerx - WIDTH//2
    dy = player.centery - HEIGHT//2
    if math.hypot(dx, dy) > safe_radius:
        return True  # player taking damage
    return False

# bullet structure
class Bullet:
    def __init__(self, x, y, vx, vy):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy

# game loop
hp = 100
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            dx, dy = mx - player.centerx, my - player.centery
            dist = math.hypot(dx, dy)
            if dist != 0:
                vx, vy = bullet_speed * dx/dist, bullet_speed * dy/dist
                bullets.append(Bullet(player.centerx, player.centery, vx, vy))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: player.y -= player_speed
    if keys[pygame.K_s]: player.y += player_speed
    if keys[pygame.K_a]: player.x -= player_speed
    if keys[pygame.K_d]: player.x += player_speed

    move_enemies()
    handle_bullets()
    if shrink_zone():
        hp -= 0.1

    draw()

    if hp <= 0:
        print("Game Over! Final Score:", score)
        pygame.quit()
        sys.exit()

    clock.tick(60)
