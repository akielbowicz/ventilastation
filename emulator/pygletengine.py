import pyglet
from pyglet.gl import *
from struct import unpack

window = pyglet.window.Window(config=Config(double_buffer=False))

def line_data_to_rgba(data):
    line_bytes = bytearray(data)
    bytes_list = (line_bytes[i:i+4] for i  in range(0, len(line_bytes), 4))
    rgba_list = (unpack('BBBB', byte) for byte in bytes_list)
    return rgba_list

def change_colors(vertex_list, data):
    colors = line_data_to_rgba(data)
    i = 0
    for a, b, g, r in colors:
        vertex_list.colors[i:i+4] = r, g, b, 255
        i += 4

LED_DOT = 4
LED_SIZE = min(window.width, window.height) / 1.9
R_ALPHA = max(window.height, window.width)

glLoadIdentity()
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glTranslatef(window.width / 2, window.height / 2, 0)


class PygletEngine():
    def __init__(self, led_count, line_iterator, vsync, revs_per_second):
        self.led_count = led_count
        self.line_iterator = line_iterator
        self.cur_angle = 0
        self.total_angle = 0
        self.vsync = vsync
        self.revs_per_second = revs_per_second
        led_step = int(LED_SIZE / led_count)

        vertex_pos = []
        for i in range(led_count):
            vertex_pos.extend([0, led_step * i])

        self.vertex_list = pyglet.graphics.vertex_list(
            led_count,
            ('v2i', vertex_pos),
            ('c4B', (0, 0, 0, 255) * led_count))

        glRotatef(180, 0, 0, 1)

        pyglet.clock.schedule_interval(self.update, 1/10000)
        self.loop()

    def loop(self):
        while True:
            pyglet.clock.tick()
            window.dispatch_events()

    def get_colors(self):
        return next(self.line_iterator)

    def draw_black(self):
        glColor4f(0, 0, 0, 0.005)
        pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
                                     [0, 1, 2, 0, 2, 3],
                                     ('v2i', (R_ALPHA, -R_ALPHA,
                                              R_ALPHA, R_ALPHA,
                                              -R_ALPHA, R_ALPHA,
                                              -R_ALPHA, -R_ALPHA)))

    def update(self, dt):
        angle = 360 * self.revs_per_second * dt

        colors = c2 = self.get_colors()
        while c2:
            colors = c2
            c2 = self.get_colors()
        if colors:
            change_colors(self.vertex_list, colors)

        self.draw_black()
        pyglet.gl.glPointSize(LED_DOT)
        self.vertex_list.draw(GL_POINTS)
        glRotatef(-angle, 0, 0, 1)

        self.cur_angle += angle
        self.total_angle += angle

        if self.total_angle > 360:
            self.vsync()
            self.total_angle -= 360

        glFlush()

