import random

import pyglet
from pyglet.gl import *

window = pyglet.window.Window(config=Config(double_buffer=False))

def change_colors(vertex_list, colors):
    i = 0
    for r, g, b, a in colors:
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
    def __init__(self, color_source, led_count):
        self.led_count = led_count
        self.color_source = color_source
        self.color_iterator = self.color_source.create_color_iterator()
        self.cur_angle = 0
        self.current_rpm = 1
        led_step = int(LED_SIZE / led_count)

        vertex_pos = []
        for i in range(led_count):
            vertex_pos.extend([0, led_step * i])

        self.vertex_list = pyglet.graphics.vertex_list(
            led_count,
            ('v2i', vertex_pos),
            ('c4B', (0, 0, 0, 255) * led_count))

        glRotatef(0, 0, 0, 1)

        pyglet.clock.schedule_interval(self.update, 1/200)
        pyglet.app.run()

    def get_colors(self):
        return next(self.color_iterator)

    def draw_black(self):
        glColor4f(0, 0, 0, 0.01)
        pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
                                     [0, 1, 2, 0, 2, 3],
                                     ('v2i', (R_ALPHA, -R_ALPHA,
                                              R_ALPHA, R_ALPHA,
                                              -R_ALPHA, R_ALPHA,
                                              -R_ALPHA, -R_ALPHA)))

    def adjust_rpm(self):
        if random.randrange(0, 10) == 0:
            self.current_rpm = random.randrange(1, 5)
            print('Adjusted RPM to {}'.format(self.current_rpm))

    def update(self, dt):
        angle = 360 * self.current_rpm * dt

        self.cur_angle += angle
        if self.cur_angle >= 360:
            self.cur_angle = self.cur_angle % 360
            self.color_source.send_tick()
            # self.adjust_rpm()

        colors = self.get_colors()
        if colors is not None:
            change_colors(self.vertex_list, colors)

        self.draw_black()
        pyglet.gl.glPointSize(LED_DOT)
        self.vertex_list.draw(GL_POINTS)
        glRotatef(angle, 0, 0, 1)

        glFlush()
