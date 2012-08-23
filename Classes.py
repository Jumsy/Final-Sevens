import random

class Colors:
    def __init__(self):
        # Static colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.off_black = (20, 20, 20)
        self.silver = (192, 192, 192)

        # The color list for mapping numbers to colors. Changes.
        self.colors = [ (255, 255, 255),  # White
                        (255, 0, 0),      # Red
                        (0, 128, 0),      # Green
                        (0, 0, 255),      # Blue
                        (255, 0, 255),    # Fuchsia
                        (255, 255, 0),    # Yellow
                        (0, 255, 0),      # Lime
                      ]

        # A copy of the colors for resetting it back to normal when changed
        self.normalColors = list(self.colors)
    
    def make_uniform(self, color=(255, 255, 255)):
        for i in range(len(self.colors)):
           self.colors[i] = color

    def randomize(self):
        for i in range(len(self.colors)):
            self.colors[i] = (random.randrange(1, 256),
                              random.randrange(1, 256),
                              random.randrange(1, 256),)

    def reset(self):
        self.colors = self.normalColors[:]


class Shape:
    """The player-controlled shape
    """
    def __init__(self):
        self.exists = False
        self.blocks = []

    def set_new(self, blocks):
        self.exists = True
        self.blocks = blocks[:]

    def rotate(self):
        pass

    def delete(self):
        self.exists = False
        self.blocks = []

    def get_printable_blocks(self):
        return [block[:] for block in self.blocks]

    def move(self, dimension, dir):
        if dimension == 'x':
            for block in self.blocks:
                block[1].centerx += dir
        elif dimension == 'y':
            for block in self.blocks:
                block[1].centery += dir
