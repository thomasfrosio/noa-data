import os
import yaml
import mrcfile
import numpy as np


def set_cwd(filename):
    os.chdir(os.path.abspath(os.path.dirname(filename)))


def save_mrc(filename, data):
    with mrcfile.new(filename, overwrite=True) as mrc:
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
