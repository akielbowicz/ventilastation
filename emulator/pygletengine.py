import pyglet
from pyglet.gl import *

window = pyglet.window.Window(config=Config(double_buffer=False))

# platform = pyglet.window.get_platform()
# display = platform.get_default_display()

def change_colors(vertex_list, colors):
    i = 0
    for r, g, b, a in colors:
        vertex_list.colors[i:i+4] = r, g, b, 255
        i += 4

LED_DOT = 3
LED_SIZE = min(window.width, window.height) / 1.9
R_ALPHA = max(window.height, window.width)
REVS_PER_SECOND = 10

glLoadIdentity()
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glTranslatef(window.width / 2, window.height / 2, 0)


class PygletEngine():
    def __init__(self, led_count, steps, line_iterator):
        self.led_count = led_count
        self.line_iterator = line_iterator
        self.step_angle = 360 / steps
        self.cur_angle = 0
        led_step = int(LED_SIZE / led_count)

        vertex_pos = []
        for i in range(led_count):
            vertex_pos.extend([0, led_step * i])

        self.vertex_list = pyglet.graphics.vertex_list(
            led_count,
            ('v2i', vertex_pos),
            ('c4B', (0, 0, 0, 255) * led_count))

        glRotatef(180, 0, 0, 1)

        pyglet.clock.schedule_interval(self.update, 1/200)
        pyglet.app.run()

    def get_colors(self):
        # return [[255, 0, 0, 255]] * self.led_count
        return [next(self.line_iterator) for _ in range(self.led_count)]

    def draw_black(self):
        glColor4f(0, 0, 0, 0.01)
        pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
                                     [0, 1, 2, 0, 2, 3],
                                     ('v2i', (R_ALPHA, -R_ALPHA,
                                              R_ALPHA, R_ALPHA,
                                              -R_ALPHA, R_ALPHA,
                                              -R_ALPHA, -R_ALPHA)))

    def update(self, dt):
        #angle = 360 * REVS_PER_SECOND * dt

        frac = 1
        angle = self.step_angle / frac

#        if self.cur_angle > self.step_angle:
        colors = self.get_colors()
        change_colors(self.vertex_list, colors)

        for i in range(frac):
            glRotatef(angle, 0, 0, 1)
            self.draw_black()
            pyglet.gl.glPointSize(LED_DOT)
            self.vertex_list.draw(GL_POINTS)

        # self.cur_angle += angle
        # if self.cur_angle > self.step_angle:
        #     self.cur_angle -= self.step_angle

        glFlush()
