import pyglet
from pyglet.gl import *

window = pyglet.window.Window(config=Config(double_buffer=False))

# platform = pyglet.window.get_platform()
# display = platform.get_default_display()

def change_colors(vertex_list, colors):
    i = 0
    for col in colors:
        vertex_list.colors[i:i+4] = col
        i += 4

from itertools import chain

led_count = 50
led_dot = 3

margin = 10
led_size = min(window.width, window.height) / 2 - margin
led_step = int(led_size / led_count)

# pos_x = [0] * led_count
# pos_y = range(0, led_step * led_count, led_step)
# vertex_pos = chain.from_iterable(zip(pos_x, pos_y))

vertex_pos = []
for i in range(led_count):
    vertex_pos.extend([0, led_step * i])

vertex_list = pyglet.graphics.vertex_list(
    led_count,
    ('v2i', vertex_pos),
    ('c4B', (0, 0, 0, 255) * led_count))

angle = 0

glLoadIdentity()
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glTranslatef(window.width / 2, window.height / 2, 0)

# fps_display = pyglet.clock.ClockDisplay()

R_ALPHA = max(window.height, window.width)

revs_per_second = 10


colors = [[255, 0, 0, 255]] * led_count

def get_colors():
    return colors

def update(dt):
    angle = 360 * revs_per_second * dt

    glRotatef(angle, 0, 0, 1)
    glColor4f(0, 0, 0, 0.01)

    pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
                                 [0, 1, 2, 0, 2, 3],
                                 ('v2i', (R_ALPHA, -R_ALPHA,
                                          R_ALPHA, R_ALPHA,
                                          -R_ALPHA, R_ALPHA,
                                          -R_ALPHA, -R_ALPHA)))

    pyglet.gl.glPointSize(led_dot)
    change_colors(vertex_list, get_colors())
    vertex_list.draw(GL_POINTS)
    glFlush()

pyglet.clock.schedule_interval(update, 1/200)

pyglet.app.run()
