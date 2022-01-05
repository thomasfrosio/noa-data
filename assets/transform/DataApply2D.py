# Global:
import numpy as np
from scipy import ndimage

# Local:
from assets import util


def matrix_rotate(angle_deg):
    # Positive angle -> rotate CW looking at origin
    # This is the inverse of what we have in noa, but it looks like that's what scipy uses.
    c = np.cos(np.deg2rad(-angle_deg))
    s = np.sin(np.deg2rad(-angle_deg))
    return np.array([[c, -s, 0],
                     [s, c, 0],
                     [0, 0, 1]])


def matrix_translate(shift):
    # shift is [X,Y], so convert to [Y,X]
    return np.array([[1, 0, shift[1]],
                     [0, 1, shift[0]],
                     [0, 0, 1]])


def matrix_scale(scale):
    # scale is [X,Y], so convert to [Y,X]
    return np.array([[scale[1], 0, 0],
                     [0, scale[0], 0],
                     [0, 0, 1]])


def compute_expected(array, matrix, noa_interp, noa_border, border_value):
    [scipy_interp_order, scipy_border, scipy_value] = util.to_scipy_interp_mode(noa_interp, noa_border, border_value)
    return ndimage.affine_transform(array, matrix,
                                    order=scipy_interp_order,
                                    mode=scipy_border,
                                    cval=scipy_value)


def generate_input(filename):
    n = 256
    image2d = np.ones((n, n), dtype=np.float32)
    image2d[50:200, 100:140] += 1
    image2d[50:80, 140:170] = 3
    image2d[200::, 230::] = 2
    image2d[:65, :75] = np.linspace(-1, 1, 65 * 75).reshape((65, 75))
    image2d[127, :] = (np.arange(n) - n // 2) / (n // 2)
    image2d[::10, ::12] += 0.5
    image2d[::11, ::13] += 0.5
    image2d[1::10, 1::13] += 1
    util.save_mrc(filename, image2d)
    print("\t-- Generated: input")


def generate_rotate2d(param):
    image = util.load_mrc(param['input'])
    border_value = param['border_value']
    rotate = param['rotate']
    center = np.array(param['center'])

    matrix = np.linalg.inv(matrix_translate(center) @
                           matrix_rotate(rotate) @
                           matrix_translate(-center))

    tests = param['tests']
    for i in tests:
        expected = compute_expected(image, matrix, tests[i]['interp'], tests[i]['border'], border_value)
        util.save_mrc(tests[i]['expected'], expected)
    print("\t-- Generated: rotate")


def generate_scale2d(param):
    image = util.load_mrc(param['input'])
    border_value = param['border_value']
    scale = np.array(param['scale'])
    center = np.array(param['center'])

    matrix = np.linalg.inv(matrix_translate(center) @
                           matrix_scale(scale) @
                           matrix_translate(-center))

    tests = param['tests']
    for i in tests:
        expected = compute_expected(image, matrix, tests[i]['interp'], tests[i]['border'], border_value)
        util.save_mrc(tests[i]['expected'], expected)
    print("\t-- Generated: scale")


def generate_translate2d(param):
    image = util.load_mrc(param['input'])
    border_value = param['border_value']
    shift = np.array(param['shift'])

    matrix = np.linalg.inv(matrix_translate(shift))

    tests = param['tests']
    for i in tests:
        expected = compute_expected(image, matrix, tests[i]['interp'], tests[i]['border'], border_value)
        util.save_mrc(tests[i]['expected'], expected)
    print("\t-- Generated: translate")


def generate_apply2d(param):
    image = util.load_mrc(param['input'])
    border_value = param['border_value']
    center = np.array(param['center'])
    scale = np.array(param['scale'])
    rotate = param['rotate']
    shift = np.array(param['shift'])

    matrix = np.linalg.inv(matrix_translate(shift) @
                           matrix_translate(center) @
                           matrix_rotate(rotate) @
                           matrix_scale(scale) @
                           matrix_translate(-center))

    tests = param['tests']
    for i in tests:
        expected = compute_expected(image, matrix, tests[i]['interp'], tests[i]['border'], border_value)
        util.save_mrc(tests[i]['expected'], expected)
    print("\t-- Generated: apply")


if __name__ == '__main__':
    util.set_cwd(__file__)

    parameters = util.load_yaml('tests.yaml')
    generate_input(parameters['input2D'])

    # This is spline interpolation, so order=3 is cubic spline which is not quite equivalent to INTERP_CUBIC and
    # INTERP_CUBIC_BSPLINE from noa. So here just compute nearest and linear. The other interpolation methods will
    # be tested against manually checked data.
    generate_rotate2d(parameters['rotate2D'])
    generate_scale2d(parameters['scale2D'])
    generate_translate2d(parameters['translate2D'])
    generate_apply2d(parameters['apply2D'])
