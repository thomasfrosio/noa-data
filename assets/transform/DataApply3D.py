# Global:
import numpy as np
from scipy import ndimage

# Local:
from assets import util


def rot_y(angle_deg):
    # In C++ noa, Y is the second axis, like here.
    # Positive angle -> rotate CW looking at origin
    # This is the inverse of what we have in noa, but it looks like that's what scipy uses.
    c = np.cos(np.deg2rad(-angle_deg))
    s = np.sin(np.deg2rad(-angle_deg))
    return np.array([[c, 0, s, 0],
                     [0, 1, 0, 0],
                     [-s, 0, c, 0],
                     [0, 0, 0, 1]])


def rot_z(angle_deg):
    # In C++ noa, Z is the third axis. Here, it is the first axis.
    # Positive angle -> rotate CW looking at origin
    # This is the inverse of what we have in noa, but it looks like that's what scipy uses.
    c = np.cos(np.deg2rad(-angle_deg))
    s = np.sin(np.deg2rad(-angle_deg))
    return np.array([[1, 0, 0, 0],
                     [0, c, -s, 0],
                     [0, s, c, 0],
                     [0, 0, 0, 1]])


def euler2matrix(euler):
    # ZYZ intrinsic
    return rot_z(euler[0]) @ rot_y(euler[1]) @ rot_z(euler[2])


def matrix_translate(shifts):
    # shift is XYZ, so convert to ZYX.
    return np.array([[1, 0, 0, shifts[2]],
                     [0, 1, 0, shifts[1]],
                     [0, 0, 1, shifts[0]],
                     [0, 0, 0, 1]])


def matrix_scale(scale):
    # scale is XYZ, so convert to ZYX.
    return np.array([[scale[2], 0, 0, 0],
                     [0, scale[1], 0, 0],
                     [0, 0, scale[0], 0],
                     [0, 0, 0, 1]])


def compute_expected(array, matrix, noa_interp, noa_border, border_value):
    [scipy_interp_order, scipy_border, scipy_value] = util.to_scipy_interp_mode(noa_interp, noa_border, border_value)
    return ndimage.affine_transform(array, matrix,
                                    order=scipy_interp_order,
                                    mode=scipy_border,
                                    cval=scipy_value)


def generate_input(filename):
    n = 64
    image3d = np.linspace(-1, 1, n ** 3, dtype=np.float32).reshape((n, n, n))
    image3d[20:60, 10:30, 40:50] += 2
    image3d[55::, 50::, 40::] = 2
    image3d[::5, ::5, ::6] += 0.5
    image3d[1::5, 1::5, 1::6] += 1
    util.save_mrc(filename, image3d)
    print("\t-- Generated: input")


def generate_rotate3d(param):
    image = util.load_mrc(param['input'])
    border_value = param['border_value']
    rotate = euler2matrix(param['euler'])
    center = np.array(param['center'])

    matrix = np.linalg.inv(matrix_translate(center) @
                           rotate @
                           matrix_translate(-center))

    tests = param['tests']
    for i in tests:
        expected = compute_expected(image, matrix, tests[i]['interp'], tests[i]['border'], border_value)
        util.save_mrc(tests[i]['expected'], expected)
    print("\t-- Generated: rotate")


def generate_scale3d(param):
    image = util.load_mrc(param['input'])
    border_value = param['border_value']
    scale = param['scale']
    center = np.array(param['center'])

    matrix = np.linalg.inv(matrix_translate(center) @
                           matrix_scale(scale) @
                           matrix_translate(-center))

    tests = param['tests']
    for i in tests:
        expected = compute_expected(image, matrix, tests[i]['interp'], tests[i]['border'], border_value)
        util.save_mrc(tests[i]['expected'], expected)
    print("\t-- Generated: scale")


def generate_translate3d(param):
    image = util.load_mrc(param['input'])
    border_value = param['border_value']
    shift = param['shift']

    matrix = np.linalg.inv(matrix_translate(shift))

    tests = param['tests']
    for i in tests:
        expected = compute_expected(image, matrix, tests[i]['interp'], tests[i]['border'], border_value)
        util.save_mrc(tests[i]['expected'], expected)
    print("\t-- Generated: translate")


def generate_apply3d(param):
    image = util.load_mrc(param['input'])
    border_value = param['border_value']
    center = np.array(param['center'])
    scale = param['scale']
    rotate = euler2matrix(param['euler'])
    shift = param['shift']

    matrix = np.linalg.inv(matrix_translate(shift) @
                           matrix_translate(center) @
                           rotate @
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
    generate_input(parameters['input3D'])

    # This is spline interpolation, so order=3 is cubic spline which is not quite equivalent to INTERP_CUBIC and
    # INTERP_CUBIC_BSPLINE from noa. So here just compute nearest and linear. The other interpolation methods will
    # be tested against manually checked data.
    generate_rotate3d(parameters['rotate3D'])
    generate_scale3d(parameters['scale3D'])
    generate_translate3d(parameters['translate3D'])
    generate_apply3d(parameters['apply3D'])
