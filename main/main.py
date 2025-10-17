import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
double_jump = False
dt = 0
gravity = 0
velocity = 0
jump_time = 0
can_jump = True
jumping = False
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
co_left = 0.3
co_right = 0.3
speed = 800
scale = 4
facing = 'left'

floor_tile = pygame.image.load('Assets/F0.png')
floor_tile = pygame.transform.scale(floor_tile, (96, 96))
wizard = pygame.image.load('Assets/IMG_0015.PNG')
wizard = pygame.transform.scale(wizard, (wizard.get_width() / scale, wizard.get_height() / scale))


def build_floor(offset, height):
    i = 0
    while i < (screen.get_width() / offset):
        screen.blit(floor_tile, (offset * i, screen.get_height() - height))
        i += 1


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if double_jump:
                    double_jump = False
                    print("Double jump off")
                else:
                    double_jump = True
                    print("Double jump on")

    screen.fill((70, 200, 255))

    if facing == 'left':
        screen.blit(wizard, player_pos)
    elif facing == 'right':
        screen.blit(pygame.transform.flip(wizard, True, False), player_pos)
    # collisions
    floor = pygame.Rect(0, screen.get_height() - floor_tile.get_height() - 1, screen.get_width(), floor_tile.get_height() + 1)
    player = pygame.Rect(player_pos.x, player_pos.y, wizard.get_width(), wizard.get_height())
    touching_floor = pygame.Rect.colliderect(player, floor)
    build_floor(floor_tile.get_width(), floor_tile.get_height())
    jump_time += 1

    if touching_floor:
        gravity = 0
        can_jump = True
        jumping = False
    elif velocity != 0:
        gravity = 0
    else:
        gravity += 75

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        if not keys[pygame.K_d]:
            facing = 'left'
        if not touching_floor and jump_time > 8:
            player_pos.x -= speed * dt * co_left * 0.8
        else:
            player_pos.x -= speed * dt * co_left
        if co_left < 1:
            co_left += 0.05
    else:
        co_left = 0.3
    if keys[pygame.K_d]:
        if not keys[pygame.K_a]:
            facing = 'right'
        if not touching_floor and jump_time > 8:
            player_pos.x += speed * dt * co_right * 0.8
        else:
            player_pos.x += speed * dt * co_right
        if co_right < 1:
            co_right += 0.05
    else:
        co_right = 0.3
    # jumping
    if (keys[pygame.K_w] or keys[pygame.K_SPACE] or jumping) and (can_jump or velocity > 0):
        velocity = 1500 - jump_time * 75
        jumping = True
        can_jump = double_jump
        if velocity < 0:
            velocity = 0
            jumping = False
    else:
        velocity = 0
        jump_time = 0
    # toggle double jump
    if (player_pos.y + (gravity - velocity) * dt) > (screen.get_height() - floor_tile.get_height() - wizard.get_height()):
        player_pos.y = screen.get_height() - floor_tile.get_height() - wizard.get_height()
    else:
        player_pos.y += (gravity - velocity) * dt

    if player_pos.x > screen.get_width() - wizard.get_width():
        player_pos.x = screen.get_width() - wizard.get_width()
    elif player_pos.x < 0:
        player_pos.x = 0

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
