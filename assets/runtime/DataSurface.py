import numpy as np
import scipy.linalg
from assets import util


def fit_surface(image, order):
    dtype = np.float32
    image = np.asarray(image, dtype=dtype)

    # regular grid covering the domain of the data
    X, Y = np.meshgrid(np.arange(image.shape[-1], dtype=dtype), np.arange(image.shape[-2], dtype=dtype))
    XX = X.flatten()
    YY = Y.flatten()
    ZZ = image.flatten()

    if order == 1:  # best-fit linear plane
        A = np.c_[np.ones(XX.size, dtype=dtype), XX, YY]
    elif order == 2:  # best-fit quadratic curve
        A = np.c_[np.ones(XX.size, dtype=dtype), XX, YY, XX * YY, XX ** 2, YY ** 2]
    elif order == 3:  # best fit cubic curve
        A = np.c_[np.ones(XX.size, dtype=dtype), XX, YY, XX * YY, XX ** 2, YY ** 2,
                  XX ** 2 * YY, XX * YY ** 2, XX ** 3, YY ** 3]
    else:
        raise RuntimeError(f"Polynomial order should be 1, 2 or 3, got {order}")

    # solve and evaluate it on a grid
    lapack_driver = 'gelsy'
    C, _, _, _ = scipy.linalg.lstsq(A, ZZ, lapack_driver=lapack_driver)  # coefficients
    surface = np.dot(A, C).reshape(X.shape)

    return C, image - surface


if __name__ == '__main__':
    util.set_cwd(__file__)

    test_file = util.load_yaml('tests.yaml')['surface']

    image = np.asarray(util.load_mrc(test_file['input']).copy(), dtype=np.float32)
    solutions = {}
    for i in range(1, 4):
        solution, image_subtracted = fit_surface(image, i)
        util.save_mrc(f"{test_file['prefix_surface']}{i}.mrc", image_subtracted)

        parameters = {}
        for p, v in enumerate(solution):
            parameters[p] = float(v)
        solutions[i] = parameters

    util.save_yaml(test_file['solution'], solutions)
    print("\t-- Generated: surface fit")
