# Global:
import numpy as np

# Local:
from assets import util


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
    euler = param['euler']
    center = np.array(param['center'])

    matrix = np.linalg.inv(util.matrix_translate(center) @
                           util.matrix_rotate(euler) @
                           util.matrix_translate(-center))

    tests = param['tests']
    for i in tests:
        expected = util.transform_affine(image, matrix, tests[i]['interp'], tests[i]['border'], border_value)
        util.save_mrc(tests[i]['expected'], expected)
    print("\t-- Generated: rotate")


def generate_scale3d(param):
    image = util.load_mrc(param['input'])
    border_value = param['border_value']
    scale = param['scale']
    center = np.array(param['center'])

    matrix = np.linalg.inv(util.matrix_translate(center) @
                           util.matrix_scale(scale) @
                           util.matrix_translate(-center))

    tests = param['tests']
    for i in tests:
        expected = util.transform_affine(image, matrix, tests[i]['interp'], tests[i]['border'], border_value)
        util.save_mrc(tests[i]['expected'], expected)
    print("\t-- Generated: scale")


def generate_translate3d(param):
    image = util.load_mrc(param['input'])
    border_value = param['border_value']
    shift = param['shift']

    matrix = np.linalg.inv(util.matrix_translate(shift))

    tests = param['tests']
    for i in tests:
        expected = util.transform_affine(image, matrix, tests[i]['interp'], tests[i]['border'], border_value)
        util.save_mrc(tests[i]['expected'], expected)
    print("\t-- Generated: translate")


def generate_apply3d(param):
    image = util.load_mrc(param['input'])
    border_value = param['border_value']
    center = np.array(param['center'])
    scale = param['scale']
    euler = param['euler']
    shift = param['shift']

    matrix = np.linalg.inv(util.matrix_translate(shift) @
                           util.matrix_translate(center) @
                           util.matrix_rotate(euler) @
                           util.matrix_scale(scale) @
                           util.matrix_translate(-center))

    tests = param['tests']
    for i in tests:
        expected = util.transform_affine(image, matrix, tests[i]['interp'], tests[i]['border'], border_value)
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
    generate_translate3d(parameters['shift3D'])
    generate_apply3d(parameters['transform3D'])
