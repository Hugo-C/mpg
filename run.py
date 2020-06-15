import qs

from common import BLACK, BLUE
from game_manager import GameManager

CRAB_ANIM = 'crab-up'


def init():
    qs.init_anims([
        # name, path, nframes, duration(s)
        [CRAB_ANIM, 'crab-up.png', 2, 1.],
    ])
    return {
        'game_manager': GameManager(),
        'color': [0, 0, 0, 1],
    }


def update(state):
    game_manager = state['game_manager']
    if game_manager.pause:
        return
    crab = game_manager.crab

    x = qs.mouse_pos()['x']
    half_screen_width = GameManager.SCREEN_WIDTH / 2
    if x < half_screen_width:
        crab.go_left(coefficient=(half_screen_width - x) / half_screen_width)
    else:
        crab.go_right(coefficient=(x - half_screen_width) / half_screen_width)
    game_manager.update()

    state['color'][0] += 0.001
    state['color'][1] += 0.002
    state['color'][2] += 0.003
    state['color'][0] %= 1
    state['color'][1] %= 1
    state['color'][2] %= 1


def draw(state):
    game_manager = state['game_manager']
    crab = game_manager.crab
    platform = game_manager.platform

    qs.clear(state['color'])

    qs.anim(CRAB_ANIM, rect=crab.to_rect())
    qs.anim(CRAB_ANIM, rect=crab.to_rect())
    for water_bubble in game_manager.water_bubbles:
        qs.circ([water_bubble.x, water_bubble.y], water_bubble.radius, color=BLUE)

    qs.rect(platform.to_rect(), color=BLACK)
    screen_size = [GameManager.SCREEN_WIDTH, GameManager.SCREEN_HEIGHT * 2]
    water_rect = [[0, platform.y + platform.size[1]], screen_size]
    qs.rect(water_rect, color=BLUE)


def event(state, event):
    game_manager = state['game_manager']

    if event['event'] == 'key' and event['key'] == 'Escape' and event['state'] == 'Pressed':
        game_manager.pause = not game_manager.pause
