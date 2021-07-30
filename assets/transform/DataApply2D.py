import os
import mrcfile
import numpy as np
from scipy import ndimage


def save_mrc(filename, data):
    with mrcfile.new(filename, overwrite=True) as mrc:
        mrc.set_data(data.astype(np.float32))


def matrix_rotate(angle):
    c = np.cos(np.deg2rad(angle))
    s = np.sin(np.deg2rad(angle))
    return np.array([[c, -s, 0],
                     [s, c, 0],
                     [0, 0, 1]])


def matrix_translate(dx, dy):
    return np.array([[1, 0, dx],
                     [0, 1, dy],
                     [0, 0, 1]])


def matrix_scale(sx, sy):
    return np.array([[sx, 0, 0],
                     [0, sy, 0],
                     [0, 0, 1]])


def interp(array, affine, order, mode, cval):
    return ndimage.affine_transform(array, affine, order=order, mode=mode, cval=cval)


if __name__ == '__main__':
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    n = 256
    image2D = np.ones((n, n), dtype=np.float32)
    image2D[50:200, 100:140] += 1
    image2D[50:80, 140:170] = 3
    image2D[200::, 230::] = 2
    image2D[:65, :75] = np.linspace(-1, 1, 65 * 75).reshape((65, 75))
    image2D[127, :] = (np.arange(n) - n // 2) / (n // 2)
    image2D[::10, ::12] += 0.5
    image2D[::11, ::13] += 0.5
    image2D[1::10, 1::13] += 1
    save_mrc("tmp_image2D.mrc", image2D)

    # This is spline interpolation, so order=3 is cubic spline which is not quite equivalent to INTERP_CUBIC and
    # INTERP_CUBIC_BSPLINE from noa. So here just compute nearest and linear. The other interpolation methods will
    # be tested against manually checked data.
    count = 0
    for order in [0, 1]:
        for mode in ['zero', 'grid-constant', 'nearest', 'mirror', 'grid-mirror', 'grid-wrap']:
            # rotate2D
            if mode == 'zero':
                value = 0
                mode = 'grid-constant'
            else:
                value = 1.3
            matrix = matrix_rotate(-45)
            out = ndimage.affine_transform(image2D, matrix, order=order, mode=mode, cval=value)
            save_mrc("tmp_rotate2D_test{:02}.mrc".format(count), out)
            count += 1

    count = 0
    for order in [0, 1]:
        for mode in ['zero', 'grid-constant', 'nearest', 'mirror', 'grid-mirror', 'grid-wrap']:
            # translate
            if mode == 'zero':
                value = 0
                mode = 'grid-constant'
            else:
                value = 1.3
            matrix = matrix_translate(20.6, -10)
            out = ndimage.affine_transform(image2D, matrix, order=order, mode=mode, cval=value)
            save_mrc("tmp_translate2D_test{:02}.mrc".format(count), out)
            count += 1

    count = 0
    for order in [0, 1]:
        for mode in ['zero', 'grid-constant', 'nearest', 'mirror', 'grid-mirror', 'grid-wrap']:
            # scale
            if mode == 'zero':
                value = 0
                mode = 'grid-constant'
            else:
                value = 1.3
            center = n // 2
            matrix = np.linalg.inv(matrix_translate(center, center) @
                                   matrix_scale(0.7, 0.6) @
                                   matrix_translate(-center, -center))
            out = ndimage.affine_transform(image2D, matrix, order=order, mode=mode, cval=value)
            save_mrc("tmp_scale2D_test{:02}.mrc".format(count), out)
            count += 1

    count = 0
    for order in [0, 1]:
        for mode in ['zero', 'grid-constant', 'nearest', 'mirror', 'grid-mirror', 'grid-wrap']:
            # scale, rotate, translate
            if mode == 'zero':
                value = 0
                mode = 'grid-constant'
            else:
                value = 1.3
            center = n // 2
            matrix = (matrix_translate(-25.5, 5.5) @
                      matrix_translate(center, center) @
                      matrix_rotate(-35.5) @
                      matrix_scale(0.7, 0.7) @
                      matrix_translate(-center, -center))
            out = ndimage.affine_transform(image2D, np.linalg.inv(matrix), order=order, mode=mode, cval=value)
            save_mrc("tmp_apply2D_test{:02}.mrc".format(count), out)

            # For noa, positive angle is CCW looking at the center and (x,y) order.
            matrix = (matrix_translate(5.5, -25.5) @
                      matrix_translate(center, center) @
                      matrix_rotate(35.5) @
                      matrix_scale(0.7, 0.7) @
                      matrix_translate(-center, -center))
            save_mrc("tmp_apply2D_test{:02}_matrix33.mrc".format(count), matrix)
            count += 1
