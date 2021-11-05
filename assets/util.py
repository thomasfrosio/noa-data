import os
import yaml
import mrcfile
import numpy as np
import warnings


def set_cwd(filename):
    os.chdir(os.path.abspath(os.path.dirname(filename)))


def save_mrc(filename, data):
    with mrcfile.new(filename, overwrite=True) as mrc:
        if data.dtype == np.complex64 or data.dtype == np.complex128:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=np.ComplexWarning)
                mrc.set_data(data.astype(np.complex64))
        else:
            mrc.set_data(data.astype(np.float32))


def save_txt(filename, string):
    with open(filename, 'w+') as file:
        file.write(string)


def save_yaml(filename, data):
    with open(filename, 'w+') as file:
        yaml.dump(data, file)


def load_mrc(filename):
    with mrcfile.open(filename) as mrc:
        array = mrc.data
    return array


def load_yaml(filename):
    with open(filename, 'r') as stream:
        parameters = yaml.safe_load(stream)
    return parameters


def to_scipy_border_mode(border, value):
    # BorderMode
    if border == 'BORDER_ZERO':
        scipy_border = 'grid-constant'
        scipy_value = 0
    elif border == 'BORDER_VALUE':
        scipy_border = 'grid-constant'
        scipy_value = value
    elif border == 'BORDER_CLAMP':
        scipy_border = 'nearest'
        scipy_value = value
    elif border == 'BORDER_REFLECT':
        scipy_border = 'mirror'
        scipy_value = value
    elif border == 'BORDER_MIRROR':
        scipy_border = 'grid-mirror'
        scipy_value = value
    elif border == 'BORDER_PERIODIC':
        scipy_border = 'grid-wrap'
        scipy_value = value
    else:
        raise RuntimeError

    return scipy_border, scipy_value


def to_scipy_interp_mode(interp, border, value):
    [scipy_border, scipy_value] = to_scipy_border_mode(border, value)

    # InterpMode
    if interp == 'INTERP_NEAREST':
        scipy_interp_order = 0
    elif interp == 'INTERP_LINEAR':
        scipy_interp_order = 1
    else:
        raise RuntimeError

    return scipy_interp_order, scipy_border, scipy_value


def get_phase_shift(shape, shift):
    """
    :param shape:   [x,y] or [x,y,z] shape
    :param shift:   [x,y] or [x,y,z] shifts
    :return: Phase shifts for redundant centered FFTs
    """
    if np.size(shape) == 2:
        x, y = (np.arange(shape[0], dtype=np.float32) - shape[0] // 2,
                np.arange(shape[1], dtype=np.float32) - shape[1] // 2)
        gx, gy = np.meshgrid(x, y)
        factors = -2 * np.pi * (shift[0] * gx / shape[0] +
                                shift[1] * gy / shape[1])

    elif np.size(shape) == 3:
        x, y, z = (np.reshape(np.arange(shape[0], dtype=np.float32) - shape[0] // 2, (1, 1, -1)),
                   np.reshape(np.arange(shape[1], dtype=np.float32) - shape[1] // 2, (1, -1, 1)),
                   np.reshape(np.arange(shape[2], dtype=np.float32) - shape[2] // 2, (-1, 1, 1)))
        gz, gy, gx = np.meshgrid(z, y, x, indexing='ij')
        factors = -2 * np.pi * (shift[0] * gx / shape[0] +
                                shift[1] * gy / shape[1] +
                                shift[2] * gz / shape[2])
    else:
        raise RuntimeError
    return np.cos(factors) + 1j * np.sin(factors)
