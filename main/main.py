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

floor_tile = pygame.image.load('Assets/F0.png')
floor_tile = pygame.transform.scale(floor_tile, (96, 96))


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

    pygame.draw.circle(screen, "purple", player_pos, 40)  # player
    # collisions
    floor = pygame.Rect(0, screen.get_height() - floor_tile.get_height() - 1, screen.get_width(), floor_tile.get_height() + 1)
    player = pygame.Rect(player_pos.x, player_pos.y, 40, 40)
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
        if not touching_floor and jump_time > 8:
            player_pos.x -= speed * dt * co_left * 0.8
        else:
            player_pos.x -= speed * dt * co_left
        if co_left < 1:
            co_left += 0.05
    else:
        co_left = 0.3
    if keys[pygame.K_d]:
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
    if (player_pos.y + (gravity - velocity) * dt) > (screen.get_height() - floor_tile.get_height() - 40):
        player_pos.y = screen.get_height() - floor_tile.get_height() - 40
    else:
        player_pos.y += (gravity - velocity) * dt

    if player_pos.x > screen.get_width() - 40:
        player_pos.x = screen.get_width() - 40
    elif player_pos.x < 40:
        player_pos.x = 40

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
