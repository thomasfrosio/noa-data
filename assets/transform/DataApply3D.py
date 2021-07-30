import os
import math
import mrcfile
import numpy as np
from scipy import ndimage


def save_mrc(filename, data):
    with mrcfile.new(filename, overwrite=True) as mrc:
        mrc.set_data(data.astype(np.float32))


def rot_y(angle):
    c = math.cos(angle)
    s = math.sin(angle)
    return np.array([[c, 0, s, 0],
                     [0, 1, 0, 0],
                     [-s, 0, c, 0],
                     [0, 0, 0, 1]])


def rot_z(angle):
    # z is the first axis here
    c = math.cos(angle)
    s = math.sin(angle)
    return np.array([[1, 0, 0, 0],
                     [0, c, -s, 0],
                     [0, s, c, 0],
                     [0, 0, 0, 1]])


def noa_rot_z(angle):
    c = math.cos(angle)
    s = math.sin(angle)
    return np.array([[c, -s, 0, 0],
                     [s, c, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])


def euler2matrix(a1, a2, a3):
    return rot_z(math.radians(a1)) @ rot_y(math.radians(a2)) @ rot_z(math.radians(a3))


def matrix_translate(dx, dy, dz):
    return np.array([[1, 0, 0, dx],
                     [0, 1, 0, dy],
                     [0, 0, 1, dz],
                     [0, 0, 0, 1]])


def matrix_scale(sx, sy, sz):
    return np.array([[sx, 0, 0, 0],
                     [0, sy, 0, 0],
                     [0, 0, sz, 0],
                     [0, 0, 0, 1]])


def interp(array, affine, order, mode, cval):
    return ndimage.affine_transform(array, affine, order=order, mode=mode, cval=cval)


if __name__ == '__main__':
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    n = 64
    image3D = np.linspace(-1, 1, n ** 3, dtype=np.float32).reshape((n, n, n))
    image3D[20:60, 10:30, 40:50] += 2
    image3D[55::, 50::, 40::] = 2
    image3D[::5, ::5, ::6] += 0.5
    image3D[1::5, 1::5, 1::6] += 1
    save_mrc("tmp_image3D.mrc", image3D)

    # This is spline interpolation, so order=3 is cubic spline which is not quite equivalent to INTERP_CUBIC and
    # INTERP_CUBIC_BSPLINE from noa. So here just compute nearest and linear. The other interpolation methods will
    # be tested against manually checked data.

    # rotate2D
    count = 0
    center = (n - 1) / 2
    matrix = np.linalg.inv(matrix_translate(center, center, center) @
                           euler2matrix(60, 0, -20) @
                           matrix_translate(-center, -center, -center))
    for order in [0, 1]:
        for mode in ['zero', 'grid-constant', 'nearest', 'mirror', 'grid-mirror', 'grid-wrap']:
            if mode == 'zero':
                value = 0
                mode = 'grid-constant'
            else:
                value = 1.3
            out = ndimage.affine_transform(image3D, matrix, order=order, mode=mode, cval=value)
            save_mrc("tmp_rotate3D_test{:02}.mrc".format(count), out)
            count += 1

    # translate
    count = 0
    matrix = np.linalg.inv(matrix_translate(-20.6, 10, -5.4))
    for order in [0, 1]:
        for mode in ['zero', 'grid-constant', 'nearest', 'mirror', 'grid-mirror', 'grid-wrap']:
            if mode == 'zero':
                value = 0
                mode = 'grid-constant'
            else:
                value = 1.3

            out = ndimage.affine_transform(image3D, matrix, order=order, mode=mode, cval=value)
            save_mrc("tmp_translate3D_test{:02}.mrc".format(count), out)
            count += 1

    count = 0
    center = (n - 1) / 2
    matrix = np.linalg.inv(matrix_translate(center, center, center) @
                           matrix_scale(1.1, 0.6, 0.8) @
                           matrix_translate(-center, -center, -center))
    for order in [0, 1]:
        for mode in ['zero', 'grid-constant', 'nearest', 'mirror', 'grid-mirror', 'grid-wrap']:
            # scale
            if mode == 'zero':
                value = 0
                mode = 'grid-constant'
            else:
                value = 1.3
            out = ndimage.affine_transform(image3D, matrix, order=order, mode=mode, cval=value)
            save_mrc("tmp_scale3D_test{:02}.mrc".format(count), out)
            count += 1

    # scale, rotate, translate
    count = 0
    center = (n - 1) / 2

    for order in [0, 1]:
        for mode in ['zero', 'grid-constant', 'nearest', 'mirror', 'grid-mirror', 'grid-wrap']:
            if mode == 'zero':
                value = 0
                mode = 'grid-constant'
            else:
                value = 1.3

            matrix = (matrix_translate(-5.2, 5.6, 4.7) @
                      matrix_translate(center, center, center) @
                      euler2matrix(-90, 30, -45) @
                      matrix_scale(0.7, 0.7, 0.7) @
                      matrix_translate(-center, -center, -center))
            out = ndimage.affine_transform(image3D, np.linalg.inv(matrix), order=order, mode=mode, cval=value)
            save_mrc("tmp_apply3D_test{:02}.mrc".format(count), out)

            # For noa, positive angle is CCW looking at the center and (x,y) order.
            matrix = (matrix_translate(4.7, 5.6, -5.2) @
                      matrix_translate(center, center, center) @
                      (noa_rot_z(math.radians(90)) @ rot_y(math.radians(-30)) @ noa_rot_z(math.radians(45))) @
                      matrix_scale(0.7, 0.7, 0.7) @
                      matrix_translate(-center, -center, -center))
            save_mrc("tmp_apply3D_test{:02}_matrix44.mrc".format(count), matrix)
            count += 1
