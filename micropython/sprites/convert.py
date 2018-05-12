#!/usr/bin/env python3

from PIL import Image
import os
from itertools import zip_longest

MAGENTA = (255, 0, 255)

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

filenames = [f for f in os.listdir(".") if f.endswith(".png")]

images = [Image.open(f) for f in filenames]

w_size = (sum(i.width for i in images), max(i.height for i in images))

workspace = Image.new("RGB", w_size, (0,0,0))

x = 0
for i in images:
    workspace.paste(i, (x, 0, i.width, i.height))

workspace = workspace.convert("P", palette=Image.ADAPTIVE)
palette = list(grouper(workspace.getpalette(), 3))
mi = palette.index(MAGENTA)
palorder = list(range(256))
palorder[255] = mi
palorder[mi] = 255
workspace = workspace.remap_palette(palorder)
palette = list(grouper(workspace.getpalette(), 3))
mi = palette.index(MAGENTA)

def gamma(value,gamma=2.5,offset=0.5):
    assert 0 <= value <= 255
    return int( pow( float(value) / 255.0, gamma ) * 255.0 + offset )
    
with open("raw/palette.pal", "wb") as pal:
    for c in palette:
        r, g, b = c
        r, g, b = gamma(r), gamma(g), gamma(b)
        pal.write(bytearray((255, b, g, r)))

raws = []
sizes = []


for i in images:
    p = i.convert("RGB").quantize(palette=workspace)
    b = p.transpose(Image.ROTATE_90).tobytes()
    
    print(i.filename)
    if ("fondo.png" in i.filename):
        fn = "raw/" + i.filename.rsplit(".", 1)[0] + ".raw"
        with open(fn, "wb") as raw:
            raw.write(b)
    else:
        raws.append(b)
        sizes.append(p.size)

print(sizes)
with open("raw/images.raw", "wb") as raw:
    raw.write(b"".join(raws))
