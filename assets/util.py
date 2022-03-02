import os
import yaml
import mrcfile
import numpy as np
from scipy import ndimage
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


def to_scipy_border_mode(border, value=0):
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


# Affine ---------------------------------------------------------------------------------------------------------------
def matrix_rotate(angle_deg):
    """
    :param angle_deg: Rotation angle or ZYZ intrinsic euler angles, in degrees
    :return: Affine matrix encoding the rotation
    """

    def rot_y(deg):
        c = np.cos(np.deg2rad(deg))
        s = np.sin(np.deg2rad(deg))
        return np.array([[c, 0, -s, 0],
                         [0, 1, 0, 0],
                         [s, 0, c, 0],
                         [0, 0, 0, 1]])

    def rot_z(deg):
        c = np.cos(np.deg2rad(deg))
        s = np.sin(np.deg2rad(deg))
        return np.array([[1, 0, 0, 0],
                         [0, c, s, 0],
                         [0, -s, c, 0],
                         [0, 0, 0, 1]])

    if not hasattr(angle_deg, '__len__'):
        c = np.cos(np.deg2rad(angle_deg))
        s = np.sin(np.deg2rad(angle_deg))
        return np.array([[c, s, 0],
                         [-s, c, 0],
                         [0, 0, 1]])
    elif len(angle_deg) == 3:
        # ZYZ intrinsic
        return rot_z(angle_deg[0]) @ rot_y(angle_deg[1]) @ rot_z(angle_deg[2])
    else:
        raise RuntimeError


def matrix_translate(shift):
    """
    :param shift: [y,x] or [z,y,x] shifts
    :return: Affine matrix encoding the shift.
             It is meant to be used on array with [z,y,x] shape.
    """
    if len(shift) == 2:
        return np.array([[1, 0, shift[0]],
                         [0, 1, shift[1]],
                         [0, 0, 1]])
    elif len(shift) == 3:
        return np.array([[1, 0, 0, shift[0]],
                         [0, 1, 0, shift[1]],
                         [0, 0, 1, shift[2]],
                         [0, 0, 0, 1]])
    else:
        raise RuntimeError


def matrix_scale(scale):
    """
    :param scale: [y,x] or [z,y,x] scale
    :return: Affine matrix encoding the scale.
             It is meant to be used on array with [z,y,x] shape.
    """
    if len(scale) == 2:
        return np.array([[scale[0], 0, 0],
                         [0, scale[1], 0],
                         [0, 0, 1]])
    elif len(scale) == 3:
        return np.array([[scale[0], 0, 0, 0],
                         [0, scale[1], 0, 0],
                         [0, 0, scale[2], 0],
                         [0, 0, 0, 1]])
    else:
        raise RuntimeError


def transform_affine(array, matrix, noa_interp, noa_border, border_value):
    [scipy_interp_order, scipy_border, scipy_value] = to_scipy_interp_mode(noa_interp, noa_border, border_value)
    return ndimage.affine_transform(array, matrix,
                                    order=scipy_interp_order,
                                    mode=scipy_border,
                                    cval=scipy_value)


# FFT ------------------------------------------------------------------------------------------------------------------
def fft_get_phase_shift(shape, shift):
    """
    :param shape:   [y,x] or [z,y,x] shape
    :param shift:   [y,x] or [z,y,x] shifts
    :return: Phase shifts for redundant centered FFTs
    """
    if np.size(shape) == 2:
        x, y = (np.arange(shape[1], dtype=np.float32) - shape[1] // 2,  # -5 -4 -3 -2 -1 0 1 2 3 4
                np.arange(shape[0], dtype=np.float32) - shape[0] // 2)
        gx, gy = np.meshgrid(x, y)
        factors = -2 * np.pi * (shift[1] * gx / shape[1] +
                                shift[0] * gy / shape[0])

    elif np.size(shape) == 3:
        x, y, z = (np.reshape(np.arange(shape[2], dtype=np.float32) - shape[2] // 2, (1, 1, -1)),
                   np.reshape(np.arange(shape[1], dtype=np.float32) - shape[1] // 2, (1, -1, 1)),
                   np.reshape(np.arange(shape[0], dtype=np.float32) - shape[0] // 2, (-1, 1, 1)))
        gz, gy, gx = np.meshgrid(z, y, x, indexing='ij')
        factors = -2 * np.pi * (shift[1] * gx / shape[1] +
                                shift[1] * gy / shape[1] +
                                shift[0] * gz / shape[0])
    else:
        raise RuntimeError
    return np.cos(factors) + 1j * np.sin(factors)


def fft_get_mask_cutoff(shape, cutoff):
    """
    :param shape: [y,x] or [z,y,x] shape
    :param cutoff: Frequency cutoff, in cycle/pix
    :return: Mask meant to be applied on redundant centered FFTs of [(z,)y,x] shape,
             to remove all components after the specified cutoff.
    """
    shape = np.array(shape, dtype=float)
    vx = np.abs(np.arange(shape[-1], dtype=np.float32) - shape[-1] // 2) / (shape[-1] // 2 * 2)
    vy = np.abs(np.arange(shape[-2], dtype=np.float32) - shape[-2] // 2) / (shape[-2] // 2 * 2)

    if np.size(shape) == 2:
        mask = vy.reshape((-1, 1)) ** 2 + vx.reshape((1, -1)) ** 2
    elif np.size(shape) == 3:
        vz = np.abs(np.arange(shape[0], dtype=np.float32) - shape[0] // 2) / (shape[0] // 2 * 2)
        mask = (vz.reshape((-1, 1, 1)) ** 2 +
                vy.reshape((1, -1, 1)) ** 2 +
                vx.reshape((1, 1, -1)) ** 2)
    else:
        raise RuntimeError

    mask = np.sqrt(mask) <= cutoff
    return mask
