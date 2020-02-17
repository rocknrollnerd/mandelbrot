import numpy as np
import matplotlib.pyplot as plt

from matplotlib.widgets import RectangleSelector

from calc import do_calc

left, bottom, right, top = -3.0, -1.0, 1.0, 1.0
width = 2000
height = int(width * (top - bottom) / (right - left))
max_iter = 500


def draw_img():
    img = np.array(
        do_calc(left, bottom, right, top, width, height, max_iter)
    )
    print(img, img.shape, np.max(img), np.min(img))
    plt.imshow(img, interpolation='none', cmap='twilight_shifted', origin='lower')

    plt.axes().set_aspect('equal')
    plt.axis('off')
    plt.tight_layout()


def selector_callback(eclick, erelease):
    global left, bottom, right, top, width, height

    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata

    print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))

    new_width = width
    new_height = int(new_width * abs(y2 - y1) / abs(x2 - x1))

    new_left = left + (right - left) * (x1 / width)
    new_right = left + (right - left) * (x2 / width)
    new_bottom = bottom + (top - bottom) * (y1 / height)
    new_top = bottom + (top - bottom) * (y2 / height)

    left = new_left
    bottom = new_bottom
    right = new_right
    top = new_top

    width = new_width
    height = new_height

    global max_iter

    max_iter = int(max_iter * 1.1)

    plt.cla()
    draw_img()
    plt.draw()


def main():
    plt.figure(figsize=(12, 12))

    RS = RectangleSelector(
        plt.gca(),
        selector_callback,
        drawtype='box',
        useblit=True,
        button=[1, 3],  # don't use middle button
        minspanx=5, minspany=5,
        spancoords='pixels',
        interactive=False
    )

    draw_img()

    plt.show()


if __name__ == '__main__':
    main()
