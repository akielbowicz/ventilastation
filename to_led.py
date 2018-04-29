import matplotlib.image as mpimg
from numpy import sin, cos, pi
from struct import pack

"""
La funcion toma un archivo *.png y devuelve en binario (RGBI) la secuencia 
de n_leds prendidos para n_ang diferentes
"""

def to_led(path=None, n_led=50, n_ang = 32):
    
    img = mpimg.imread(path)        # Levanta la imagen

    wx, wy, dim = img.shape         # Me da las dimensiones del frame en pixeles
    center_x = int((wx-1)/2)        # Calcula la cordenada x del centro de la imagen
    center_y = int((wy-1)/2)        # Calcula la cordenada y del centro de la imagen
    rad = min(center_x, center_y)   # Calcula el radio que barre la imagen dentro del frame

    led = []
    
    for m in range(0,n_ang):
        for n in range(0,n_led):
            x = center_x + int(rad * (n+1)/n_led * cos(m * 2*pi/n_ang)) 
            y = center_y + int(rad * (n+1)/n_led * sin(m * 2*pi/n_ang))
            tupla = tuple(int(255 * g) for g in img[x,y,0:3]) + (31,)
            led.append(pack('BBBB', *tupla))
    return b''.join(led)
