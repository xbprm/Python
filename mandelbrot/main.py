import numpy as np
import matplotlib.pyplot as plt


"""
This function calculates the Mandelbrot set for a given complex number c using the specified maximum number of iterations.

:param c: The complex number c for which to calculate the Mandelbrot set.
:param max_iter: The maximum number of iterations to use when calculating the Mandelbrot set.
:return: The number of iterations required to escape the Mandelbrot set, or max_iter if the point never escapes.
"""
def mandelbrot(c, max_iter):
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z * z + c
    return max_iter

"""
This function calculates the Mandelbrot set for a given range of complex numbers using the specified maximum number of iterations.

:param x_min: The minimum real component of the complex numbers.
:param x_max: The maximum real component of the complex numbers.
:param y_min: The minimum imaginary component of the complex numbers.
:param y_max: The maximum imaginary component of the complex numbers.
:param width: The width of the output image.
:param height: The height of the output image.
:param max_iter: The maximum number of iterations to use when calculating the Mandelbrot set.
:return: A numpy array containing the Mandelbrot set values for each point in the grid.
"""
def mandelbrot_set(x_min, x_max, y_min, y_max, width, height, max_iter):
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    mset = np.zeros((width, height))
    for i in range(width):
        for j in range(height):
            mset[i, j] = mandelbrot(complex(x[j], y[i]), max_iter)
    return mset

"""
This function generates an image of the Mandelbrot set for a given range of complex numbers using the specified maximum number of iterations.

:param x_min: The minimum real component of the complex numbers.
:param x_max: The maximum real component of the complex numbers.
:param y_min: The minimum imaginary component of the complex numbers.
:param y_max: The maximum imaginary component of the complex numbers.
:param width: The width of the output image.
:param height: The height of the output image.
:param max_iter: The maximum number of iterations to use when calculating the Mandelbrot set.
"""
def mandelbrot_image(x_min, x_max, y_min, y_max, width, height, max_iter):
    plt.imshow(mandelbrot_set(x_min, x_max, y_min, y_max, width, height, max_iter), extent=[x_min, x_max, y_min, y_max], cmap='hot')
    plt.colorbar()
    plt.title('Mandelbrot Set')
    plt.xlabel('Re(c)')
    plt.ylabel('Im(c)')
    plt.show()

if __name__ == '__main__':
    x_min, x_max, y_min, y_max = -2.0, 1.0, -1.5, 1.5
    width, height = 1000, 1000
    max_iter = 100
    mandelbrot_image(x_min, x_max, y_min, y_max, width, height, max_iter)
