from pygletengine import PygletEngine
from struct import unpack


LINE_HEIGHT = 50

def convert_png_to_data(filename, out_filename):
    import matplotlib.image as mpimg
    with open(out_filename, 'wb') as out_file:
        img = mpimg.imread(filename)
        img = (255 * img).astype('uint8')
        for i in range(img.shape[1]):
            scan_line = img[:,i][::-1]
            out_file.write(scan_line.tostring())

# convert_png_to_data('data/m1.png', 'data/m1.dat')
# convert_png_to_data('data/m2.png', 'data/m2.dat')
# convert_png_to_data('data/m3.png', 'data/m3.dat')

def read_scanline(fd, line_position, out_buffer):
    fd.seek(0)
    fd.seek(line_position * LINE_HEIGHT * 4)
    out_buffer[:] = fd.read(LINE_HEIGHT * 4)

def line_data_to_rgba(line_bytes):
    bytes_list = (line_bytes[i:i+4] for i  in range(0, len(line_bytes), 4))
    rgba_list = (unpack('BBBB', byte) for byte in bytes_list)
    return rgba_list

class Drawable():
    def __init__ (self, sprite_buffer, pos_inicial, width, height):
        self.posicion = pos_inicial
        self.width = width
        self.height = height
        self._cur_frame = 0
        self._frame_size = 4 * width * height
        self._frame_length = len(sprite_buffer) / self._frame_size
        self._buffer = sprite_buffer#bytearray(self.width * self.height)

    def next_frame(self):
        self._cur_frame += 1
        if self._cur_frame >= self._frame_length:
            self._cur_frame = 0

    def draw(self, scan_position, _buffer):
        width_position = self.posicion[0] - scan_position
        should_draw = 0 <= (width_position) < self.width
        if should_draw:
            a = self._cur_frame * self._frame_size + width_position * self.height * 4
            b = a + self.height * 4
            buf_a = self.posicion[1]*4
            buf_b = buf_a + self.height*4
            _buffer[buf_a:buf_b] = self._buffer[a:b]

def game_iterator():
    fd = open('data/fondo.dat', 'rb')
    _buffer = bytearray(LINE_HEIGHT * 4)
    cur_line = 0

    fd2 = open('data/character.dat', 'rb')
    sprite_buffer = fd2.read()

    character = Drawable(sprite_buffer, (64, 10), 24, 24)
    while True:
        for scan_position in range(128):
            if scan_position == 0:
                character.next_frame()
            if scan_position < 10 or scan_position > 118:
                yield [[0,0,0,0]] * 50
            else:
                read_scanline(fd, line_position=cur_line+scan_position, out_buffer=_buffer)
                character.draw(scan_position, _buffer)
                yield line_data_to_rgba(_buffer)
        cur_line += 1

PygletEngine(led_count=50, steps=128, line_iterator=game_iterator())
