from common import random, norm_random
from game_object import Crab, Platform, WaterBubble


class GameManager:
    """Class to orchestrate the game and store all objects"""
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    def __init__(self):
        self.crab = Crab(x=self.SCREEN_WIDTH/2, y=0, size=[100, 100])
        self.platform = Platform(x=0, y=550, size=[self.SCREEN_WIDTH, 10])
        self.water_bubbles = []
        self._water_bubbles_to_remove = set()
        self._random_number = 3
        self._frames_since_bubble_spawn = 0
        self.speed_of_water_bubble_spawn = 10

    def update(self):
        """Update the game logic (after player input has been processed) every frame"""
        self._frames_since_bubble_spawn += 1
        self.crab.refresh_position_on_platform(self.platform)

        self._water_bubbles_to_remove = []
        for bubble in self.water_bubbles:
            bubble.update()
            if self.crab.can_catch_water_bubble(bubble):
                self._water_bubbles_to_remove.append(bubble)
            if bubble.is_out_of_screen(self.SCREEN_HEIGHT):
                self._water_bubbles_to_remove.append(bubble)

        # Clean bubbles
        for water_bubble in self._water_bubbles_to_remove:
            if water_bubble in self.water_bubbles:
                self.water_bubbles.remove(water_bubble)

        if self._frames_since_bubble_spawn > self.speed_of_water_bubble_spawn:
            self.spawn_water_bubble()

    def spawn_water_bubble(self):
        self._random_number = random(self._random_number)
        x = norm_random(self._random_number, self.SCREEN_WIDTH) + 30
        self.water_bubbles.append(WaterBubble(x=x, y=-25, size=[800, 10], radius=25))
        self._frames_since_bubble_spawn = 0
