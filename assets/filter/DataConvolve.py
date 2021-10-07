import numpy as np
from scipy import signal

from assets import util


def get_kernel(size, sigma):
    vector = np.arange(size, dtype=np.float64) - size // 2
    return np.exp(-0.5 * (vector / sigma) ** 2)


def generate_inputs(param):
    # 2D
    shape_2d = np.flip(param['2D']['shape'])
    img_2d = np.ones(shape_2d).astype(np.float64)
    img_2d += np.random.randn(shape_2d[0], shape_2d[1], shape_2d[2])
    img_2d[:, 100:150, :] += 100
    img_2d[:, :, 90:130] += 50
    util.save_mrc(param['2D']['path'], img_2d)

    # 3D
    shape_3d = np.flip(param['3D']['shape'])
    img_3d = np.ones(shape_3d).astype(np.float64)
    img_3d += np.random.randn(shape_3d[0], shape_3d[1], shape_3d[2])
    img_3d[30:91, :, :] += 100
    img_3d[:, 0:30, :] += 20
    img_3d[:, :, 80:130] += 40
    util.save_mrc(param['3D']['path'], img_3d)
    print("\t-- Generated: inputs")


def generate_filters(param):
    for i in param:
        shape = param[i]['shape']
        sigma = param[i]['sigma']
        if len(shape) == 1:
            kernel = np.zeros((1, 2, shape[0]), dtype=np.float64)  # 2D because of mrcfile
            kernel[0, 0, :] = get_kernel(shape[0], sigma)
            kernel /= np.sum(kernel)
            util.save_mrc(param[i]['path'], kernel)
        elif len(shape) == 2:
            kernel = np.zeros((1, shape[1], shape[0]), dtype=np.float64)
            kernel += get_kernel(shape[0], sigma).reshape((1, 1, shape[0]))
            kernel += get_kernel(shape[1], sigma).reshape((1, shape[1], 1))
            kernel /= np.sum(kernel)
            util.save_mrc(param[i]['path'], kernel)
        elif len(shape) == 3:
            kernel = np.zeros(np.flip(shape), dtype=np.float64)
            kernel += get_kernel(shape[0], sigma).reshape((1, 1, shape[0]))
            kernel += get_kernel(shape[1], sigma).reshape((1, shape[1], 1))
            kernel += get_kernel(shape[2], sigma).reshape((shape[2], 1, 1))
            kernel /= np.sum(kernel)
            util.save_mrc(param[i]['path'], kernel)
    print("\t-- Generated: filters")


def scipy_convolve(array, kernel):
    return signal.convolve(array, kernel, mode='same', method='direct')


def generate_conv(param):
    for i in param:
        array = util.load_mrc(param[i]['input'])
        kernel = util.load_mrc(param[i]['filter'])
        if kernel.shape[0] == 1 and kernel.shape[1] == 2:  # 1D kernel...
            kernel = kernel[0, 0, :].reshape((1, 1, kernel.shape[2]))
        convolved = signal.convolve(array, kernel, mode='same', method='direct')
        util.save_mrc(param[i]['expected'], convolved)
        print("\t-- Generated: convolve nb {}".format(i))


def generate_filter_separable(param):
    size = param['size']
    sigma = param['sigma']
    kernel = np.zeros((1, 2, size), dtype=np.float64)  # 2D because of mrcfile
    kernel[0, 0, :] = get_kernel(size, sigma)
    kernel /= np.sum(kernel)
    util.save_mrc(param['path'], kernel)


def generate_conv_separable(param):
    for i in param:
        array = util.load_mrc(param[i]['input'])
        kernel = util.load_mrc(param[i]['filter'])[0, 0, :]  # 2D because of mrcfile
        kernel_size = kernel.size
        dims = param[i]['dim']
        for dim in dims:
            if dim == 0:
                array = scipy_convolve(array, kernel.reshape((1, 1, kernel_size)))
            elif dim == 1:
                array = scipy_convolve(array, kernel.reshape((1, kernel_size, 1)))
            elif dim == 2:
                array = scipy_convolve(array, kernel.reshape((kernel_size, 1, 1)))
            else:
                raise RuntimeError
        util.save_mrc(param[i]['expected'], array)
        print("\t-- Generated: convolve separable nb {}".format(i))


if __name__ == '__main__':
    util.set_cwd(__file__)

    parameters = util.load_yaml('param.yaml')
    generate_inputs(parameters['convolve']['inputs'])
    generate_filters(parameters['convolve']['filters'])
    generate_conv(parameters['convolve']['tests'])

    generate_filter_separable(parameters['convolve_separable']['filter'])
    generate_conv_separable(parameters['convolve_separable']['tests'])
