from ventilagon.levels import current_level
from ventilagon.transformations import transformations
import urandom
import utime


seed = 0
def randrange(low, high):
    global seed
    _range = high - low
    seed += urandom.getrandbits(32)
    return (seed % _range) + low
    

class Pattern:
    def __init__(self):
        urandom.seed(utime.ticks_us())
        self.randomize()
        self.block_height = current_level.block_height
        self.current_height = self.block_height
        self.current_value = 0

    def randomize(self):
        # init current_height to max, so first call to next_row() calculates
        # the value of row zero
        self.current_height = self.block_height = current_level.block_height
        self.transformation_base = randrange(0, 12) << 6
        new_pattern = randrange(0, len(current_level.patterns))
        self.rows = current_level.patterns[new_pattern]
        self.rows_len = self.rows[0]
        self.row = 1

    def transform(self, b):
        return transformations[self.transformation_base + b]

    def next_row(self):
        self.current_height += 1
        if self.current_height >= self.block_height:
            self.current_height = 0
            base_value = self.rows[self.row]
            self.row += 1
            self.current_value = self.transform(base_value)
        return self.current_value

    def finished(self):
        #print("finished?")
        #print(self.row, self.rows_len, self.current_height, self.block_height)
        return (self.row > self.rows_len) # and (self.current_height >= self.block_height)
