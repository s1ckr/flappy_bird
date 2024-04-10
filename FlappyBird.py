from pygame import *
import sys
import random

font.init()
mixer.init()

W = 1000
H = 500
window = display.set_mode((W, H))
clock = time.Clock()
display.set_caption('Flappy Bird')

sprite = transform.scale(image.load('../../../../Downloads/Telegram Desktop/bird_new.png'), (80, 50))
sprite_incline = transform.scale(image.load('bird_alpha.png'), (80, 50))
bg = transform.scale(image.load('../../../../Downloads/Telegram Desktop/background.png'), (W, H))
go = transform.scale(image.load('../../../../Downloads/Telegram Desktop/game_over_2.png'), ((W // 2) - 50, H // 2))
space = transform.scale(image.load('../../../../Downloads/Telegram Desktop/space.png'), (W // 2, H // 4))
restart = transform.scale(image.load('restart.png'), (W // 2, H // 8))

score_numbers = font.Font("pixel_font.ttf", 100)

mixer.music.load('music.mp3')
mixer.music.play(-1)


pipes = []

counter_animation = 0
start_counter = 0

game_over = False
game_started = False


class Hero:
    def __init__(self, x, y, x_right, height):
        self.x = x
        self.y = y
        self.is_jump = False
        self.velocity = -1
        self.x_right = x_right - 10
        self.height = height
        self.score = 0

    def jump(self):
        self.velocity = 8

    def update_position(self):
        if self.velocity >= -20:
            self.velocity -= 0.5
        self.y -= self.velocity


class Pipe:
    start_speed = 2
    speed = 2
    levels = []

    def __init__(self, top_x, top_y, width, low_y):
        self.top_x = top_x
        self.top_y = top_y
        self.width = width
        self.low_y = low_y
        self.step = 0
        self.is_scored = False


def create_new_pipe():
    global counter_animation, pipes
    if counter_animation >= (150 * (Pipe.start_speed / Pipe.speed)):
        w = random.randint(150, 250)

        p_up = Pipe(W, 0, 50, w)
        p_down = Pipe(W, w + 200, 50, H)

        pipes.append([p_up, p_down])

        counter_animation = 0


def moving_pipes():
    global pipes, bird, game_over
    for p_up, p_down in pipes:
        p_up.top_x -= p_up.speed
        p_down.top_x -= p_down.speed

        game_is_over(p_up, p_down)

    draw_pipes(pipes)


def update_score():
    global pipes, bird
    for p_up, p_down in pipes:
        if (p_up.top_x + p_up.width) <= bird.x and p_up.is_scored is False:
            bird.score += 1
            p_up.is_scored = True


def draw_pipes(pipes_arr):
    for p_up, p_down in pipes_arr:
        new_p_up = Rect(p_up.top_x, p_up.top_y, p_up.width, p_up.low_y)
        new_p_down = Rect(p_down.top_x, p_down.top_y, p_down.width, p_down.low_y)

        draw.rect(window, (0, 255, 0), new_p_up, 0)
        draw.rect(window, (0, 255, 0), new_p_down, 0)
        draw.rect(window, [0, 0, 0], new_p_up, 5)
        draw.rect(window, [0, 0, 0], new_p_down, 5)


def check_borders(player_bird):
    global H, game_over
    if player_bird.y < 0:
        game_over = True
    if player_bird.y > H:
        game_over = True


def game_is_over(p_up, p_down):
    global bird, game_over

    # coords = [[bird.x, bird.y], [bird.x_right, bird.y], [bird.x, bird.y + bird.height],
    #           [bird.x_right, bird.y + bird.height], [bird.x + 20, bird.y + 15], [bird.x_right - 10, bird.y + 5],
    #           [bird.x + 10, bird.y + bird.height + 5], [bird.x_right - 10, bird.y + bird.height + 5]]
    coords = [[bird.x, bird.y + bird.height],
              [bird.x_right, bird.y + bird.height], [bird.x + 10, bird.y + 10], [bird.x_right - 10, bird.y + 10],
              [bird.x + 10, bird.y + bird.height + 5], [bird.x_right - 10, bird.y + bird.height + 5]]

    for x, y in coords:
        if ((p_up.top_y <= y <= p_up.low_y) or (p_down.top_y <= y <= p_down.low_y)) and (
                p_up.top_x <= x <= (p_up.top_x + p_up.width)):
            game_over = True

    if bird.y < 0 or bird.y > H:
        game_over = True


def game_cycle():
    global game_started
    keys_arr = key.get_pressed()
    if keys_arr[K_SPACE]:
        bird.jump()

    bird.update_position()
    create_new_pipe()
    moving_pipes()
    update_score()
    update_speed()


bird = Hero(30, H // 2, 30 + 80, 50)


def restart_game():
    global bird, pipes, counter_animation, game_over, game_started
    bird = Hero(30, H // 2, 30 + 80, 50)
    pipes = []
    counter_animation = 0
    game_started = True
    game_over = False
    Pipe.start_speed = 2
    Pipe.speed = 2
    Pipe.levels = []


def update_speed():
    global bird, start_counter
    if bird.score % 5 == 0 and bird.score != 0 and (bird.score not in Pipe.levels):
        Pipe.speed += 1
        Pipe.levels.append(bird.score)


# def remove_pipes():
#     global pipes
#     for p in pipes:
#         if (p[0].top_x + p[0].width) < 0:
#             pipes.remove(p)


while True:
    clock.tick(60)
    for e in event.get():
        if e.type == QUIT:
            quit()
            sys.exit()

    window.blit(bg, (0, 0))

    if bird.velocity > 0:
        window.blit(sprite_incline, (bird.x, bird.y))
    else:
        window.blit(sprite, (bird.x, bird.y))

    draw_pipes(pipes)

    if not game_started:
        keys = key.get_pressed()
        window.blit(space, ((W // 2) - 250, (H // 2) - 90))
        if keys[K_SPACE]:
            game_started = True
    elif not game_over:
        game_cycle()
    else:
        pass

    if game_over:
        window.blit(go, ((W // 2) - 225, (H // 2) - 125))
        window.blit(restart, ((W // 2) - 250, (H // 2 + 125)))
        keys = key.get_pressed()
        if keys[K_r]:
            restart_game()

    text = score_numbers.render(f"{bird.score}", True, (255, 255, 255))
    window.blit(text, (W // 2 - 20, H // 2 - 200))

    counter_animation += 1
    if start_counter < 5000:
        start_counter += 1
    display.update()
