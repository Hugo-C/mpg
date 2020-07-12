import qs

from common import BLACK, BLUE
from game_manager import GameManager

CRAB_ANIM = 'crab-up'

DEFAULT_UPDATE_RATE = 14


def init():
    qs.init_anims([
        # name, path, nframes, duration(s)
        [CRAB_ANIM, 'crab-up.png', 2, 1.],
    ])
    return {
        'game_manager': GameManager(),
    }


def onload(state):
    qs.set_update_rate(DEFAULT_UPDATE_RATE)


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


def draw(state):
    game_manager = state['game_manager']
    crab = game_manager.crab
    platform = game_manager.platform

    qs.clear(game_manager.background_color.format())

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

    if event['event'] == 'key' and event['state'] == 'Pressed':
        if event['key'] == 'Escape':
            game_manager.pause = not game_manager.pause
        elif event['key'] == 'Right':
            qs.set_update_rate(qs.update_rate() - 2)
        elif event['key'] == 'Left':
            qs.set_update_rate(qs.update_rate() + 2)
        elif event['key'] == 'Space':
            qs.set_update_rate(DEFAULT_UPDATE_RATE)
