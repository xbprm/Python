import numpy as np
import matplotlib.pyplot as plt


def mandelbrot(c, max_iter):
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z * z + c
    return max_iter

def mandelbrot_set(x_min, x_max, y_min, y_max, width, height, max_iter):
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    mset = np.zeros((width, height))
    for i in range(width):
        for j in range(height):
            mset[i, j] = mandelbrot(complex(x[j], y[i]), max_iter)
    return mset

x_min, x_max, y_min, y_max = -2.0, 1.0, -1.5, 1.5
width, height = 1000, 1000
max_iter = 100

mandelbrot_image = mandelbrot_set(x_min, x_max, y_min, y_max, width, height, max_iter)

plt.imshow(mandelbrot_image, extent=[x_min, x_max, y_min, y_max], cmap='hot')
plt.colorbar()
plt.title('Mandelbrot Set')
plt.xlabel('Re(c)')
plt.ylabel('Im(c)')
plt.show()
