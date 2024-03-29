import pygame
from game.shared.bomber_constants import *
from game.shared.bombermap import *

block_size = (blockW, blockH)

def scale_image(img, size = block_size):
    return pygame.transform.scale(img, size)

player_image = pygame.image.load('img/player.png')
computer_image = pygame.image.load('img/computer.png')
bomb_image = pygame.image.load('img/squarebomb.png')
explosion_image = pygame.image.load('img/explosion.png')

player_image = scale_image(player_image, block_size)
computer_image = scale_image(computer_image, block_size)
bomb_image = scale_image(bomb_image, block_size)
explosion_image = scale_image(explosion_image, block_size)

powerup_images = ['img/powerup_extrabombs.png', 'img/powerup_extrapower.png']
for i in range(len(powerup_images)):
    powerup_images[i] = pygame.image.load(powerup_images[i])
    powerup_images[i] = scale_image(powerup_images[i])

block_images = [None, 'img/wall.png', 'img/brick.png']
for i in range(1, len(block_images)):
    block_images[i] = pygame.image.load(block_images[i])
    block_images[i] = scale_image(block_images[i])


standard_rect = pygame.Rect(0, 0, blockW, blockH)

def pos_to_pixel(pos):
    return [pos[0]*blockW, pos[1]*blockH]

def get_rect(pos):
    rect = standard_rect
    rect.left, rect.top = pos_to_pixel(pos)
    return rect

def horiz_center_rect(rect):
    rect.left = width/2 - rect.width/2

def vert_center_rect(rect):
    rect.top = height/2 - rect.height/2

def center_rect(rect):
    horiz_center_rect(rect)
    vert_center_rect(rect)

def draw_menu_items(menu_screen, first_item_top=100, item_distance = 40):
    font_path = 'fonts/GUBBLABLO.ttf'
    font = pygame.font.Font(font_path, int(20*scale))
    y = first_item_top

    for i in range(menu_screen.length):
        text = menu_screen.choices[i].upper()
        if menu_screen.selector == i:
            surface = font.render(text, True, black, nice_blue)
        else:
            surface = font.render(text, True, white)
        rect = surface.get_rect()
        rect.top = y
        horiz_center_rect(rect)
        screen.blit(surface, rect)
        y += rect.height + item_distance

def draw_menu(menu_screen, background=True, first_item_top = 100*scale, item_distance = 40*scale):
    font_path = 'fonts/GUBBLABLO.ttf'
    background_color = 15,15,15
    if background:
        screen.fill(background_color)

    #draw title
    title_font = pygame.font.Font(font_path, int(40*scale))
    title = title_font.render("BOMBERMAN", True, nice_red)
    title_rect = title.get_rect().move((100, 20))
    horiz_center_rect(title_rect)
    screen.blit(title, title_rect)

    draw_menu_items(menu_screen, first_item_top, item_distance)

    pygame.display.flip()


def draw_text(text, y=60*scale):
    text = text.upper()
    lines = text.split('\n')
    font_path = 'fonts/Square.ttf'
    font = pygame.font.Font(font_path, 15)

    for line in lines:
        surface = font.render(line, True, white)
        rect = surface.get_rect()
        rect.top = y
        horiz_center_rect(rect)
        screen.blit(surface, rect)
        y += rect.height + 5
    return y

def draw_player(p):
    rect = get_rect(p.position)
    screen.blit(player_image, rect)

def draw_computer(p):
    rect = get_rect(p.position)
    screen.blit(computer_image, rect)

def draw_block(b, pos):
    if b.btype == BlockType.blank:
        return
    rect = get_rect(pos)
    img = block_images[b.btype]
    screen.blit(img, rect)

def draw_bomb(b):
    rect = get_rect(b.position)
    screen.blit(bomb_image, rect)

def draw_map():
    for x in range(mapW):
        for y in range(mapH):
            draw_block(map[x][y], [x,y])

def draw_explosion(e):
    positions = e.exploded_positions
    for p in positions:
        rect = get_rect(p)
        screen.blit(explosion_image, rect)

def draw_powerup(p):
    rect = get_rect(p.position)
    screen.blit(powerup_images[p.type], rect)

def draw_list_function(func, l):
    def f():
        for x in l:
            func(x)
    return f

draw_bombs = draw_list_function(draw_bomb, bombs)
draw_explosions = draw_list_function(draw_explosion, explosions)
draw_powerups = draw_list_function(draw_powerup, powerups)

def draw_players():
    for h in humans:
        draw_player(h)
    for c in computers:
        draw_computer(c)

white = 255,255,255
black = 0,0,0
red = 255,0,0
green = 0,255,0
blue = 0,0,255
chartreuse = 127,255,0
light_green = 131,255,100
nice_red = 207,45,64
sky_blue = 100,244,255
nice_blue = 0,194,255

def draw_game_over():
    font_path = 'fonts/GUBBLO___.ttf'
#    font_path = 'fonts/Square.ttf'
    font_size = int(20*scale)

    game_over_font = pygame.font.Font(font_path, font_size*2)
    other_font = pygame.font.Font(font_path, font_size)

    y = height/2 - game_over_font.get_height()/2 - other_font.get_height()/2 * 2

    game_over_text = game_over_font.render("GAME OVER", True, black, white)
    game_over_rect = pygame.Rect((y, 150), game_over_text.get_size())
    horiz_center_rect(game_over_rect)
    screen.blit(game_over_text, game_over_rect)


    space_text = other_font.render("PRESS [SPACE] TO RESTART.", True, black, white)
    space_rect = space_text.get_rect().move([0, game_over_rect.bottom])
    horiz_center_rect(space_rect)
    screen.blit(space_text, space_rect)

    esc_text = other_font.render("PRESS [ESC] FOR MAIN MENU.", True, black, white)
    esc_rect = esc_text.get_rect().move([0, space_rect.bottom])
    horiz_center_rect(esc_rect)
    screen.blit(esc_text, esc_rect)


def draw_stuff(game_over=False):
    screen.fill(white)
    draw_map()
    draw_powerups()
    draw_bombs()
    draw_players()
    draw_explosions()
    if game_over:
        draw_game_over()
    pygame.display.flip()
