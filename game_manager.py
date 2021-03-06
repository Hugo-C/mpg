from color import BackgroundColor
from common import random, norm_random, lerp
from game_object import Crab, Platform, WaterBubble, WaterBubblePool


class GameManager:
    """Class to orchestrate the game and store all objects"""
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    PLATFORM_INITIAL_HEIGHT = 550
    BUBBLE_INITIAL_SPAWN_SPEED = 100
    BUBBLE_MAX_SPAWN_SPEED = 50
    BUBBLE_SPAWN_ACCELERATION = 0.05

    def __init__(self):
        self.crab = Crab(x=self.SCREEN_WIDTH / 2, y=10, size=[100, 100])
        self.platform = Platform(
            x=0,
            y=self.PLATFORM_INITIAL_HEIGHT,
            size=[self.SCREEN_WIDTH, 10],
            screen_height=self.SCREEN_HEIGHT,
        )
        self.water_bubbles_pool = WaterBubblePool()
        self.water_bubbles = []
        self._random_number = 3
        self._frames_since_bubble_spawn = 0
        self.speed_of_water_bubble_spawn = self.BUBBLE_INITIAL_SPAWN_SPEED
        self.pause = False

        self.background_color = BackgroundColor()

        self.up_0 = True
        self.up_1 = True
        self.up_2 = True

    def update(self):
        """Update the game logic (after player input has been processed) every frame"""
        if self.pause:
            return

        if self.crab.y <= 0:
            self.restart()
            return

        self._frames_since_bubble_spawn += 1

        water_bubbles_to_keep = []
        for bubble in self.water_bubbles:
            bubble.update()
            if bubble.is_below(self.platform):
                self.platform.go_up()
                self.water_bubbles_pool.add(bubble)
            elif self.crab.can_catch_water_bubble(bubble):
                self.platform.go_down()
                self.water_bubbles_pool.add(bubble)
            else:
                water_bubbles_to_keep.append(bubble)
        self.platform.refresh_height()
        self.crab.refresh_position_on_platform(self.platform)

        self.background_color.update(self.player_situation())

        # Clean bubbles
        self.water_bubbles = water_bubbles_to_keep

        if self._frames_since_bubble_spawn > self.speed_of_water_bubble_spawn:
            self.spawn_water_bubble()
            self.refresh_spawn_rate()

    def refresh_spawn_rate(self):
        current = self.speed_of_water_bubble_spawn
        lowest = self.BUBBLE_MAX_SPAWN_SPEED
        highest = self.BUBBLE_INITIAL_SPAWN_SPEED
        actual = (current - lowest) / (highest - lowest)
        c = actual * (1 - self.BUBBLE_SPAWN_ACCELERATION)
        self.speed_of_water_bubble_spawn = lerp(highest, lowest, c)

    def spawn_water_bubble(self, x=None, y=-25):
        if not x:
            self._random_number = random(self._random_number)
            x = norm_random(self._random_number)
        x = x * self.SCREEN_WIDTH + 30
        new_water_bubble = self.water_bubbles_pool.get(x=x, y=y, size=[800, 10], radius=25)
        self.water_bubbles.append(new_water_bubble)
        self._frames_since_bubble_spawn = 0

    def player_situation(self):
        """Return a value between 0 and 1
        the closer to 0, the more the player is close to loose
        """
        return self.platform.y / self.SCREEN_WIDTH

    def restart(self):
        self.water_bubbles = []
        self._frames_since_bubble_spawn = 0
        self.speed_of_water_bubble_spawn = self.BUBBLE_INITIAL_SPAWN_SPEED
        self.platform.y = self.PLATFORM_INITIAL_HEIGHT
        self.platform.y_target = self.platform.y
        self.crab.x = self.SCREEN_WIDTH / 2
        self.crab.refresh_position_on_platform(self.platform)
