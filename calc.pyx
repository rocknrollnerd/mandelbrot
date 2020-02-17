# distutils: language=c++
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True

cimport cython
from cython.view cimport array as cvarray
from cython.parallel import prange
from libc.math cimport fabs
from libcpp.vector cimport vector
import numpy as np


cdef double get_real(double x, double y, double cx) nogil:
    return x * x - y * y + cx

cdef double get_img(double x, double y, double cy) nogil:
    return 2 * x * y + cy


cpdef int[:, :] do_calc(double left, double bottom, double right, double top, int width, int height, int max_iters):
    result = cvarray(shape=(height, width), itemsize=sizeof(int), format="i")
    cdef int[:, :] result_view = result
    cdef double cx, cy, x, y, new_x, new_y, fwidth, fheight
    cdef int _iter, i, j,
    fwidth = width
    fheight = height
    for j in prange(height, nogil=True):
        for i in range(width):
            cx = left + (right - left) * (i / fwidth)
            cy = bottom + (top - bottom) * (j / fheight)
            x = 0
            y = 0

            # run iterations
            for _iter in range(max_iters):
                if x * x + y * y > 4:
                    break
                new_x = get_real(x, y, cx)
                new_y = get_img(x, y, cy)
                x = new_x
                y = new_y

            result_view[j, i] = _iter

    return result_view
