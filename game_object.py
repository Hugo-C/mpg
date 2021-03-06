class GameObject:
    def __init__(self, *, x=0, y=0, size=None):
        self.x = x
        self.y = y
        self.size = size
        self.half_width = self.size[0] / 2.

    def to_rect(self):
        """Return the gameobject to be display by qs.anim"""
        return [[self.x, self.y], self.size]

    def update(self):
        """Update the game object every frame"""
        pass

    def reset_values(self, *, x=0, y=0, size=None):
        self.x = x
        self.y = y
        self.size = size
        self.half_width = self.size[0] / 2.


class Crab(GameObject):

    def __init__(self, x, y, size, min_x=0, max_x=800):
        GameObject.__init__(self, x=x, y=y, size=size)  # super() is not supported by pyckitup 0.1
        self.speed = 15
        self.min_x = min_x - self.size[0]  # take into account sprite size
        self.max_x = max_x
        self.move_smoother = 0.9

    def go_left(self, coefficient=1):
        self.x -= (self.speed * coefficient) ** self.move_smoother
        self.x = max(self.min_x, self.x)

    def go_right(self, coefficient=1):
        self.x += (self.speed * coefficient) ** self.move_smoother
        self.x = min(self.max_x, self.x)

    def refresh_position_on_platform(self, platform):
        self.y = platform.y - self.size[1]

    def can_catch_water_bubble(self, water_bubble):
        y_diff = water_bubble.y - self.y - 15
        if y_diff < 0:  # Handmade abs for performances
            y_diff = -y_diff
        if y_diff > 40:
            return False  # Hack for performances
        x_diff = water_bubble.x - (self.x + self.half_width)
        if x_diff < 0:
            x_diff = -x_diff
        return x_diff + y_diff < 40


class Platform(GameObject):
    """Platform on which the crab is standing"""
    max_height = 580
    min_up = 10
    max_up = 30
    min_down = 10
    max_down = 100

    def __init__(self, x, y, size, screen_height):
        GameObject.__init__(self, x=x, y=y, size=size)
        self.y_target = y
        self.screen_height = screen_height

    def refresh_height(self):
        if self.y < self.y_target:
            self.y += 1
        elif self.y > self.y_target:
            self.y -= 1

    def go_up(self):
        up_by = self.min_up + (self.y_target / self.screen_height * (self.max_up - self.min_up))
        self.y_target -= up_by

    def go_down(self):
        down_by = self.min_down + (1. - self.y_target / self.screen_height) * (self.max_down - self.min_down)
        self.y_target += down_by
        self.y_target = min(self.y_target, self.max_height)


class WaterBubble(GameObject):

    def __init__(self, x, y, size, radius):
        GameObject.__init__(self, x=x, y=y, size=size)
        self.speed = 5
        self.radius = radius

    def update(self):
        self.y += self.speed

    def is_below(self, gameobject):
        return self.y >= gameobject.y + self.radius

    def reset_values(self, *, x=0, y=0, size=None, radius=0):
        GameObject.reset_values(self, x=x, y=y, size=size)
        self.radius = radius


class WaterBubblePool:
    """Pool of water bubble used to avoid creating/destroying object in repetition"""

    def __init__(self):
        self.unused_water_bubble = []

    def add(self, water_bubble):
        self.unused_water_bubble.append(water_bubble)

    def get(self, **kwargs):
        if len(self.unused_water_bubble) > 1:
            water_bubble = self.unused_water_bubble.pop()
            water_bubble.reset_values(**kwargs)
            return water_bubble
        else:
            return WaterBubble(**kwargs)


