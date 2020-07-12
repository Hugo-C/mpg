class Color:

    def __init__(self, r=1., g=1., b=1., a=1.):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def format(self):
        """Format the output for qs"""
        return [self.r, self.g, self.b, self.a]


class BackgroundColor(Color):
    """Class managing the logic behind the color pattern of the background"""

    MIN_COLOR_VALUE = 0.15  # Shouldn't be lower than 0, allow the game to be brighter

    def __init__(self):
        Color.__init__(self)
        self.r_is_going_up = False
        self.g_is_going_up = False
        self.b_is_going_up = False

    def update(self, player_situation):
        """Simple color roll, speed up when the player is in a bad situation"""
        situation = (1 - player_situation) * 20

        change = 0.0001 * situation
        r_change = change
        if self.r_is_going_up:
            if self.r + r_change >= 1.:
                self.r_is_going_up = False
            else:
                self.r += r_change
        else:
            if self.r - r_change <= self.MIN_COLOR_VALUE:
                self.r_is_going_up = True
            else:
                self.r -= r_change

        b_change = change + 0.0001
        if self.b_is_going_up:
            if self.g + b_change >= 1.:
                self.b_is_going_up = False
            else:
                self.g += b_change
        else:
            if self.g - b_change <= self.MIN_COLOR_VALUE:
                self.b_is_going_up = True
            else:
                self.g -= b_change

        g_change = change + 0.0002
        if self.g_is_going_up:
            if self.b + g_change >= 1.:
                self.g_is_going_up = False
            else:
                self.b += g_change
        else:
            if self.b - g_change <= self.MIN_COLOR_VALUE:
                self.g_is_going_up = True
            else:
                self.b -= g_change
