import numpy as np
import eulerangles
from assets import util


def generate_euler_angles(parameters):
    valid_axes = parameters['axes']
    eulers = parameters['angles']
    matrices = np.zeros((len(valid_axes) * 4, 1, 3, 3))
    count = 0
    for axes in valid_axes:
        for intrinsic in (True, False):
            for right_handed_rotation in (True, False):
                matrices[count] = eulerangles.euler2matrix(
                    eulers,
                    axes=axes,
                    intrinsic=intrinsic,
                    right_handed_rotation=right_handed_rotation
                )
                count += 1
    util.save_mrc(parameters['file'], matrices)


if __name__ == '__main__':
    util.set_cwd(__file__)
    parameters = util.load_yaml('tests.yaml')['euler2matrix']
    generate_euler_angles(parameters)
