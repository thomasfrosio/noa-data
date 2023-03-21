# Global:
import numpy as np

# Local:
from assets import util


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


def generate_transform2d(param):
    image = util.load_mrc(param['input'])

    for i in param['tests']:
        test = param['tests'][i]
        cvalue = test['cvalue']
        center = np.array(test['center'])
        scale = np.array(test['scale'])
        rotate = test['rotate']
        shift = np.array(test['shift'])
        matrix = np.linalg.inv(util.matrix_translate(shift) @
                               util.matrix_translate(center) @
                               util.matrix_rotate(rotate) @
                               util.matrix_scale(scale) @
                               util.matrix_translate(-center))
        expected = util.transform_affine(image, matrix, test['interp'], test['border'], cvalue)
        util.save_mrc(test['expected'], expected)

    print("\t-- Generated: transform 2D")


if __name__ == '__main__':
    util.set_cwd(__file__)

    parameters = util.load_yaml('tests.yaml')
    generate_input(parameters['input2D'])

    # This is spline interpolation, so order=3 is cubic spline which is not quite equivalent to INTERP_CUBIC and
    # INTERP_CUBIC_BSPLINE from noa. So here just compute nearest and linear. The other interpolation methods will
    # be tested against manually checked data.
    generate_transform2d(parameters['transform_2d'])
