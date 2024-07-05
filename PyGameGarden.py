"""
Игра 'Весёлый огород'
ЛКМ - посадить, ПКМ - отменить
Уровни: Дачник, Фермер

Разработчик: Боброва Екатерина Викторовна
Дизайнер: @alin42
"""
import pygame
import random
import os
import sys

FPS = 50 # количество кадров в секунду
size = width, height = 600, 600
number = 3 # поле 3x3 клетки
numberoftrees = 1

def load_image(name, colorkey=None, size=(100, 100)):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    image = pygame.transform.scale(image, size)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def load_hs(name):  # загрузить highscore
    fullname = os.path.join('data', name)
    # если файл не существует, то highscore = 0
    if not os.path.isfile(fullname):
        highscore = 0
    else:
        with open(fullname, 'r+') as f:
            highscore = int(f.read())
    print("highscore", highscore)
    return highscore
                
def terminate():
    pygame.quit()
    sys.exit()

def rules_screen():
    intro_text = ["В нашем огороде несколько грядок и яблоня.",
                  "Яблоня даёт тень на соседние грядки, поэтому ",
                  "рядом нужно сажать теневыносливые растения.",
                  "К светолюбивым относят клубнику и огурцы,",
                  "а корнеплоды не нуждаются в большом ",
                  "количестве солнечного света.",
                  "Нужно посадить не менее трёх грядок картошки, ",
                  "хотя бы по одной грядке с морковкой и свёклой,",
                  "не менее двух грядок с клубникой и не более ",
                  "двух грядок с луком и огурцами. ",
                  "Картофелю полезно соседство лука, потому что",
                  "он препятствуют размножению спор фитофторы — ",
                  "губительного грибкового заболевания. ",
                  "Но близость огурцов, наоборот, вредна.",
                  "К корнеплодам относятся морковь, свёкла,",
                  "картофель."]
    fon = pygame.transform.scale(load_image('0.png', size=size), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    string_rendered = font.render("ПРАВИЛА ИГРЫ", 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 50
    intro_rect.x = width // 2 - string_rendered.get_width() // 2
    screen.blit(string_rendered, intro_rect)
    text_coord = 80
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 40
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return mainMenu(size)
        pygame.display.flip()
        clock.tick(FPS)


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, dx, dy):
        super().__init__(fire_group)
        self.image = random.choice(fire)
        self.rect = self.image.get_rect()
        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos
        # гравитация будет одинаковой
        self.gravity = 0.25

    def update(self):
        # применяем гравитационный эффект: 
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect((0, 0, width, height)):
            self.kill()

def game_over(score, highscore):
    def create_particles():
        # количество создаваемых частиц
        particle_count = 20
        # возможные скорости
        numbers = range(-5, 6)
        coords = range(50, 550)
        center = (random.choice(coords), random.choice(coords))
        for _ in range(particle_count):
            Particle(center, random.choice(numbers), random.choice(numbers))
        
    intro_text = ["ПОСАДКИ ВЫПОЛНЕНЫ",""]
    if score > highscore:
        highscore = score
        intro_text.append("Новый рекорд урожая!")
        with open(os.path.join('data', 'highscore'), 'w') as f:
            f.write(str(score))
    intro_text.append("Урожай: " + str(score))
    intro_text.append("Нажмите любую клавишу")
    fon = pygame.transform.scale(load_image('0.png', size=size), size)
    font = pygame.font.Font(None, 30)
    create_particles()
    redraw = 0
    
    def screen_update():
        text_coord = 50
        screen.blit(fon, (0, 0))
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = width // 2 - string_rendered.get_width() // 2
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return mainMenu(size)
        screen_update()
        redraw += 1
        if redraw >= 30:
            create_particles()
            redraw = 0
        # отрисовка и изменение свойств объектов
        fire_group.draw(screen)
        fire_group.update()
        pygame.display.flip()
        # временная задержка
        clock.tick(FPS)


class Button:
    def __init__(self, x, y, width, height, text=''):
        self.color = (255, 220, 200)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        if self.text != '':
            font = pygame.font.SysFont(None, 60)
            text = font.render(self.text, 1, (100, 50, 0))
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                     self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [['0'] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.score = 0

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        
    def get_cell(self, mouse_pos):
        mx, my = mouse_pos
        if not self.left < mx < self.cell_size * self.width + self.left or \
           not self.top < my < self.cell_size * self.height + self.top:
            return None
        return ((mx - self.left) // self.cell_size, (my - self.top) // self.cell_size)
        
    def get_click(self, mouse_pos, tile_type):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell, tile_type)
        

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class Gardener(Board):
    # создание поля
    def __init__(self, width, height, numberoftrees):
        super().__init__(width, height)
        tree = 0
        while tree < numberoftrees:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.board[y][x] == '0':
                self.board[y][x] = '1'
                tree += 1
        self.highscore = load_hs('highscore')

    def open_cell(self, cell_coords, tile_type):
        x, y = cell_coords
        self.board[y][x] = tile_type
        
    def on_click(self, cell_coords, tile_type):
        # print(cell_coords)
        # print(self.board)
        if cell_coords == None:
            return
        x, y = cell_coords
        if self.board[y][x] != '0':
            self.score -= 10
            return
        if self.board[y][x] == '0':
            self.open_cell(cell_coords, tile_type)
            self.score += 10
            Tile(tile_type, x * self.cell_size + self.left, y * self.cell_size + self.top)

    def count(self, t):
        s = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == t:
                    s += 1
        return s

    def count_score(self):
        score, p = 0, 0,
        s = self.count('strawberry')
        c = self.count('carrot')
        cu = self.count('cucumber')
        on = self.count('onion')
        b = self.count('beet')
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 'tree':
                    if y > 0 and ((self.board[y - 1][x] == 'strawberry') or
                                  (self.board[y - 1][x] == 'cucumber')):
                        score -= 5
                    if x > 0 and ((self.board[y][x - 1] == 'strawberry') or
                                  (self.board[y][x - 1] == 'cucumber')):
                        score -= 5
                    if y < number - 1 and ((self.board[y + 1][x] == 'strawberry') or
                                           (self.board[y + 1][x] == 'cucumber')):
                        score -= 5
                    if x < number - 1 and ((self.board[y][x + 1] == 'strawberry') or
                                           (self.board[y][x + 1] == 'cucumber')):
                        score -= 5
                if self.board[y][x] == 'potato':
                    p += 1
                    if y > 0 and (self.board[y - 1][x] == 'onion'):
                        score += 5
                    if x > 0 and (self.board[y][x - 1] == 'onion'):
                        score += 5
                    if y < number - 1 and (self.board[y + 1][x] == 'onion'):
                        score += 5
                    if x < number - 1 and (self.board[y][x + 1] == 'onion'):
                        score += 5
                    if y > 0 and (self.board[y - 1][x] == 'cucumber'):
                        score -= 5
                    if x > 0 and (self.board[y][x - 1] == 'cucumber'):
                        score -= 5
                    if y < number - 1 and (self.board[y + 1][x] == 'cucumber'):
                        score -= 5
                    if x < number - 1 and (self.board[y][x + 1] == 'cucumber'):
                        score -= 5
        score += 5 if p >= 3 else -5
        score += 5 if c >=1 and b >= 1 else -5 
        score += 5 if s >= 2 else -5
        score += 5 if cu <= 2 and on <= 2 else -5
        # print('potato', p, 'carrot', c, 'strawberry', s, 'cucumber', cu, 'onion', on, 'beet', b, score)
        return score

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == '0':  # земля
                    Tile('ground', x * self.cell_size + self.left, y * self.cell_size + self.top)
                if self.board[y][x] == '1':  # дерево
                    Tile('tree', x * self.cell_size + self.left, y * self.cell_size + self.top)


def play_game(shift=0):
    board = Gardener(number + shift, number+ shift, numberoftrees+ shift)  # поле 3 на 3 грядки и 1 яблоня
    board.set_view(width // 4 - shift * 50, height // 4, 100)
    t = random.randint(2, len(tile_images) - 1)
    tile = Tile(list(tile_images.keys())[t], width // 2 - 50, 10)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    board.score -= 5
                    # print(list(tile_images.keys())[t], board)
                else: # TODO: Нажатие на игровое поле левой кнопкой
                    board.get_click(event.pos, list(tile_images.keys())[t])
                t = random.randint(2, len(tile_images) - 1)
                tile = Tile(list(tile_images.keys())[t], width // 2 - 50, 10)
                if board.count('0') == 0: # нет пустых клеток
                    board.score += board.count_score()
                    running = game_over(board.score, board.highscore)
        screen.fill((10, 10, 10))
        font = pygame.font.Font(None, 50)
        text = font.render('Урожай: ' + str(board.score), True, (100, 255, 100))
        screen.blit(text, (10, 10))
        board.render(screen)
        # отрисовка и изменение свойств объектов
        all_sprites.draw(screen)
        pygame.display.flip()
        # временная задержка
        clock.tick(FPS)
    return 1

def mainMenu(size):
    menu_bg_img = pygame.transform.scale(load_image('veselii-ogorod.jpg', size=size), size)
    menu_bg = menu_bg_img.get_rect()
    screen.blit(menu_bg_img, menu_bg)
    startButton1 = Button(width // 5, 70, 160, 45, "Дачник")
    startButton1.draw(screen)
    startButton2 = Button(width // 2, 70, 160, 45, "Фермер")
    startButton2.draw(screen)
    rulesButton = Button(width // 2 - 90, 140, 180, 45, "Правила")
    rulesButton.draw(screen)
    quitButton = Button(width - 150, height - 55, 140, 45, "Выйти")
    quitButton.draw(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONDOWN and quitButton.isOver(event.pos)):
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and startButton1.isOver(event.pos):
                running = play_game()
            if event.type == pygame.MOUSEBUTTONDOWN and startButton2.isOver(event.pos):
                running = play_game(1)
            if event.type == pygame.MOUSEBUTTONDOWN and rulesButton.isOver(event.pos):
                running = rules_screen()
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Garden')
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()  
    # создадим группу, содержащую все спрайты
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    fire_group = pygame.sprite.Group()
    tile_width = tile_height = 50
    tile_images = {
    'ground': load_image('0.png'),
    'tree': load_image('1.png'),
    'potato': load_image('61.png'),
    'carrot': load_image('62.png'),
    'strawberry': load_image('63.png'),
    'onion': load_image('64.png'),
    'cucumber': load_image('65.png'),
    'beet': load_image('66.png')
    }
    # сгенерируем частицы разного размера
    fire = []
    emptyApple = load_image('apple4.png')
    fire.append(pygame.transform.scale(load_image('apple1.png'), (50, 50)))
    fire.append(pygame.transform.scale(load_image('apple2.png'), (50, 50)))
    fire.append(pygame.transform.scale(load_image('apple3.png'), (50, 50)))
    for scale in (15, 25, 35):
        fire.append(pygame.transform.scale(emptyApple, (scale, scale)))
        fire.append(pygame.transform.scale(emptyApple, (scale, scale)))
        fire.append(pygame.transform.scale(emptyApple, (scale, scale)))
    mainMenu(size)
    terminate()
