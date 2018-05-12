from ucollections import namedtuple

Level = namedtuple("Level", ("step_delay", "block_height", "rotation_speed",
"song", "color", "bg1", "bg2", "patterns", "drift_calculator"))

def no_drift(drift_speed):
    return 0

solo_A = [
    10,
    0b010101,
    0b000000,
    0b010101,
    0b000000,
    0b000000,
    0b000000,
    0b111011,
    0b000000,
    0b000000,
    0b000000,
]

solo_B = [
    9,
    0b010101,
    0b010101,
    0b000000,
    0b000000,
    0b000000,
    0b111011,
    0b000000,
    0b000000,
    0b000000,
]

solo_C = [
    10,
    0b010010,
    0b000000,
    0b010010,
    0b000000,
    0b000000,
    0b000000,
    0b111011,
    0b000000,
    0b000000,
    0b000000,
]

solo_D = [
    9,
    0b010010,
    0b010010,
    0b000000,
    0b000000,
    0b000000,
    0b111011,
    0b000000,
    0b000000,
    0b000000,
]

triple_C = [
    12,
    0b101111,
    0b000000,
    0b000000,
    0b000000,
    0b111101,
    0b000000,
    0b000000,
    0b000000,
    0b101111,
    0b000000,
    0b000000,
    0b000000,
]

bat = [
    15,
    0b011111,
    0b001110,
    0b001110,
    0b001110,
    0b000100,
    0b100100,
    0b100100,
    0b110001,
    0b110001,
    0b111011,
    0b111011,
    0b010001,
    0b000000,
    0b000000,
    0b000000,
]

whirpool = [
    18,
    0b011111,
    0b001111,
    0b000111,
    0b000011,
    0b100001,
    0b110000,
    0b011000,
    0b001100,
    0b000110,
    0b000011,
    0b100001,
    0b110000,
    0b111000,
    0b111100,
    0b111110,
    0b000000,
    0b000000,
    0b000000,
]

ladder = [
    16,
    0b110110,
    0b010010,
    0b010010,
    0b011011,
    0b010010,
    0b010010,
    0b110110,
    0b010010,
    0b010010,
    0b011011,
    0b010010,
    0b010010,
    0b110110,
    0b000000,
    0b000000,
    0b000000,
]

patterns_level1 = [
    solo_A,
    solo_B,
    solo_C,
    solo_D,
    triple_C,
    whirpool,
    bat,
    ladder,
]

levels = [
    Level(50000, 4, 5, '1', 0x0000ff, 0x000000, 0x000001, patterns_level1, no_drift),
]

current_level = levels[0]
