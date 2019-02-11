import os
import pygame
import math

FPS = 100000;
pygame.init()
size = width, height = 1366, 768
screen = pygame.display.set_mode(size)
screen.fill((0, 30, 0))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


'''
def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)
'''
tile_images = {
    'wall': load_image('wall.png'),
    'empty': load_image('grass.png')
}


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            128 * pos_x, 128 * pos_y)


class PlayerSoldier(pygame.sprite.Sprite):
    frames = [load_image('image_part_001.png'), load_image('image_part_002.png'),
              load_image('image_part_003.png'), load_image('image_part_004.png')]

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x * 128, y * 128)
        self.pos_x = x * 128
        self.pos_y = y * 128

    def update(self, angle1):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.rotate(self.image, angle1 - 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def moving(self, cos1, sin1):
        self.pos_x += 35 * cos1
        self.pos_y += 35 * sin1
        self.rect.center = (self.pos_x, self.pos_y)

    def fire(self, sin12, cos12, x, y):
        Bullet(x, y, sin12, cos12)


class Zombie(pygame.sprite.Sprite):
    frames = [load_image('image_part_017.png'), load_image('image_part_018.png'),
              load_image('image_part_019.png'), load_image('image_part_020.png')]

    def __init__(self, x, y):
        super().__init__(zombies)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x * 128, y * 128)
        self.pos_x = x * 128
        self.pos_y = y * 128

    def update(self, angle1):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.rotate(self.image, angle1 - 90)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.pos_x += 10 * math.sin(angle1)
        self.pos_y += 10 * math.cos(angle1)
        self.rect.center = (self.pos_x, self.pos_y)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                x1, y1 = x, y
            elif level[y][x] == 'z':
                Tile('empty', x, y)
                Zombie(x, y)
    new_player = PlayerSoldier(x1, y1)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, sin12, angle12):
        super().__init__(bullets)
        print(1)
        self.cur_frame = 0
        self.image = load_image('pixil-frame-0.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.pos_x = x
        self.pos_y = y
        self.speed_x = sin12 * 75
        print(angle)
        self.speed_y = angle12 * 75

    def update(self, *args):
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y
        self.rect.center = (self.pos_x, self.pos_y)


clock = pygame.time.Clock()
zombies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player, width, height = generate_level(load_level("file"))
lenghtOfGun = player.rect.width / 2
running = True
going = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                going = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                going = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if pos[1] - player.rect.y - 29 == 0:
                cos_angle = 0
            elif pos[1] - player.rect.y - 29 > 0:
                cos_angle = (pos[1] - player.rect.y - 29) / \
                            ((pos[1] - player.rect.y - 29) ** 2 + (
                                    pos[0] - player.rect.x - 29) ** 2) ** .5
            else:
                cos_angle = (pos[1] - player.rect.y - 29) / \
                            ((pos[1] - player.rect.y - 29) ** 2 + (
                                    pos[0] - player.rect.x - 29) ** 2) ** .5
            if pos[0] - player.rect.x - 29 == 0:
                sin_angle = 0
            if pos[0] - player.rect.x - 29 > 0:
                sin_angle = (pos[0] - player.rect.x - 29) / \
                            ((pos[1] - player.rect.y - 29) ** 2 + (
                                    pos[0] - player.rect.x - 29) ** 2) ** .5
            else:
                sin_angle = (pos[0] - player.rect.x - 29) / (
                        (pos[1] - player.rect.y - 29) ** 2 + (
                        pos[0] - player.rect.x - 29) ** 2) ** .5
            x = (pos[0] - player.rect.x) * lenghtOfGun / (
                    (pos[1] - player.rect.y) ** 2 + (
                    pos[0] - player.rect.x) ** 2) ** .5 + player.rect.x + 19
            y = (pos[1] - player.rect.y) * lenghtOfGun / (
                    (pos[1] - player.rect.y) ** 2 + (
                    pos[0] - player.rect.x) ** 2) ** .5 + player.rect.y + 19
            player.fire(sin_angle, cos_angle, x, y)
    if going:
        pos = pygame.mouse.get_pos()
        if pos[1] - player.rect.y - player.rect.height // 2 == 0:
            cos_angle = 0
        elif pos[1] - player.rect.y - player.rect.height // 2 > 0:
            cos_angle = (pos[1] - player.rect.y - player.rect.height // 2) / \
                        ((pos[1] - player.rect.y - player.rect.height // 2) ** 2 + (
                                pos[0] - player.rect.x - player.rect.width // 2) ** 2) ** .5
        else:
            cos_angle = (pos[1] - player.rect.y - player.rect.height // 2) / \
                        ((pos[1] - player.rect.y - player.rect.height // 2) ** 2 + (
                                pos[0] - player.rect.x - player.rect.width // 2) ** 2) ** .5
        if pos[0] - player.rect.x - player.rect.width // 2 == 0:
            sin_angle = 0
        if pos[0] - player.rect.x - player.rect.width // 2 > 0:
            sin_angle = (pos[0] - player.rect.x - player.rect.width // 2) / \
                        ((pos[1] - player.rect.y - player.rect.height // 2) ** 2 + (
                                pos[0] - player.rect.x - player.rect.width // 2) ** 2) ** .5
        else:
            sin_angle = (pos[0] - player.rect.x - player.rect.width // 2) / (
                    (pos[1] - player.rect.y - player.rect.height // 2) ** 2 + (
                     pos[0] - player.rect.x - player.rect.width // 2) ** 2) ** .5
        angle = str(int(round(math.degrees(math.atan2(pos[0] - player.rect.x, pos[1] - player.rect.y)))))
        player.moving(sin_angle, cos_angle)
    pos = pygame.mouse.get_pos()
    angle = int(round(math.degrees(
        math.atan2(pos[0] - player.rect.x - player.rect.width // 2, pos[1] - player.rect.y - player.rect.height // 2))))
    tiles_group.draw(screen)
    all_sprites.draw(screen)
    zombies.draw(screen)
    for i in zombies:
        i.update(int(round(math.degrees(
            math.atan2(player.rect.x + player.rect.width // 6 - i.rect.x,
                       player.rect.y + player.rect.height // 6 - i.rect.y)))))
    bullets.draw(screen)
    all_sprites.update(angle)
    bullets.update()
    pygame.display.flip()
    screen.fill((0, 30, 0))
    clock.tick(20)
