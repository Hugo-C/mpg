class GameObject:
    def __init__(self, *, x=0, y=0, size=None):
        self.x = x
        self.y = y
        self.size = size

    def to_rect(self):
        """Return the gameobject to be display by qs.anim"""
        return [[self.x, self.y], self.size]

    def update(self):
        """Update the game object every frame"""
        pass


class Crab(GameObject):

    def __init__(self, x, y, size):
        GameObject.__init__(self, x=x, y=y, size=size)  # super() is not supported by pyckitup 0.1
        self.speed = 15

    def go_left(self, coefficient=1):
        self.x -= self.speed * coefficient

    def go_right(self, coefficient=1):
        self.x += self.speed * coefficient

    def refresh_position_on_platform(self, platform):
        self.y = platform.y - self.size[1]

    def can_catch_water_bubble(self, water_bubble):
        x_diff = abs(water_bubble.x - (self.x + self.size[0]/2))
        y_diff = abs(water_bubble.y - self.y - 15)
        return x_diff + y_diff < 40


class Platform(GameObject):
    """Platform on which the crab is standing"""
    max_height = 580

    def go_up(self):
        self.y -= 15

    def go_down(self):
        self.y = min(self.y + 5, self.max_height)


class WaterBubble(GameObject):

    def __init__(self, x, y, size, radius):
        GameObject.__init__(self, x=x, y=y, size=size)
        self.speed = 5
        self.radius = radius

    def update(self):
        self.y += self.speed

    def is_out_of_screen(self, screen_height):
        return self.y > screen_height + self.radius



