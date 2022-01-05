import numpy as np
from scipy import ndimage

from assets import util


def generate_inputs(param):
    # 2D
    shape = np.flip(param['2D']['shape'])
    elements = np.prod(shape)
    img = np.arange(elements).astype(np.float32)
    img[np.random.randint(0, elements - 1, size=elements // 100)] *= 100
    img = img.reshape(shape)
    util.save_mrc(param['2D']['path'], img)

    # 3D
    shape = np.flip(param['3D']['shape'])
    elements = np.prod(shape)
    img = np.arange(elements).astype(np.float32)
    img[np.random.randint(0, elements - 1, size=elements // 100)] *= 100
    img = img.reshape(shape)
    util.save_mrc(param['3D']['path'], img)
    print("\t-- Generated: inputs")


def generate_medfilt(param):
    for i in range(len(param)):
        array = util.load_mrc(param[i]['input'])
        [border, _] = util.to_scipy_border_mode(param[i]['border'], 0)
        window = param[i]['window']
        dim = param[i]['dim']
        if dim == 1:
            out = ndimage.median_filter(array, (1, 1, window), mode=border, cval=0)
        elif dim == 2:
            out = ndimage.median_filter(array, (1, window, window), mode=border, cval=0)
        elif dim == 3:
            out = ndimage.median_filter(array, (window, window, window), mode=border, cval=0)
        else:
            raise RuntimeError
        util.save_mrc(param[i]['expected'], out)
    print("\t-- Generated: filtered data")


if __name__ == '__main__':
    util.set_cwd(__file__)

    parameters = util.load_yaml('tests.yaml')['median']
    generate_inputs(parameters['inputs'])
    generate_medfilt(parameters['tests'])
