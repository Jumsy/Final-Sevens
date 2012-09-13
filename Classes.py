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
        self.blocks = blocks

    def sync(self, newPositions):
        for i, position in enumerate(newPositions):
            self.blocks[i][1].centerx = position[0]
            self.blocks[i][1].centery = position[1]

    def rotate(self):
        """This function extracts the coordinate data from each block
        then gets the edge locations of a square encompassing every
        block. The coordinates are rotated within this square and returned.
        """
        if not self.blocks: return

        blocks = [ [block[1].centerx, block[1].centery] for block in self.blocks ]
        blockWidth = self.blocks[0][1].right - self.blocks[0][1].left

        limit = 100000
        left = max
        right = 0
        bottom = 0
        top = limit 

        for block in blocks:
            left = min(left, block[0] - (blockWidth/2))
            right = max(right, block[0] + (blockWidth/2))
            bottom = max(bottom, block[1] + (blockWidth/2))
            top = min(top, block[1] - (blockWidth/2))

        height = top - bottom
        width = right - left
        
        height = width = max(height, width)

        left = right - width
        top = bottom - height
        
        if left < 0 or top < 0:
            return

        for block in blocks:
            dx = (block[0] - left)
            dy = (block[1] - top)
            block[0] = right - dy
            block[1] = top + dx

        return blocks

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
