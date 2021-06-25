import numpy as np
import mrcfile
import os

from scipy import signal


def save_mrc(filename, data):
    with mrcfile.new(filename, overwrite=True) as mrc:
        mrc.set_data(data.astype(np.float32))


def get_vector(size):
    return np.arange(size, dtype=np.float64) - size // 2


def get_kernel(size, sigma):
    return np.exp(-0.5 * (get_vector(size) / sigma) ** 2)


if __name__ == '__main__':
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    # 2D
    shape_2D = (1, 250, 251)
    elements_2D = np.prod(shape_2D)
    img_2D = np.ones(shape_2D).astype(np.float64)
    img_2D += np.random.randn(1, 250, 251)
    img_2D[:, 100:150, :] += 100
    img_2D[:, :, 90:130] += 50
    save_mrc("tmp_conv_img_2D.mrc", img_2D)

    # 3D
    shape_3D = (152, 151, 150)
    elements_3D = np.prod(shape_3D)
    img_3D = np.ones(shape_3D).astype(np.float64)
    img_3D += np.random.randn(152, 151, 150)
    img_3D[30:91, :, :] += 100
    img_3D[:, 0:30, :] += 20
    img_3D[:, :, 80:130] += 40
    save_mrc("tmp_conv_img_3D.mrc", img_3D)

    # kernels
    size = 31
    sigma = 5
    filter_1D = np.zeros((1, 2, size), dtype=np.float64)
    filter_1D[0, 0, :] = get_kernel(size, sigma)
    filter_1D /= np.sum(filter_1D)
    save_mrc("tmp_conv_filter_1D.mrc", filter_1D)

    shape = (1, 9, 17)
    sigma = 3
    filter_2D = np.zeros(shape, dtype=np.float64)
    filter_2D += get_kernel(shape[2], sigma).reshape((1, 1, shape[2]))
    filter_2D += get_kernel(shape[1], sigma).reshape((1, shape[1], 1))
    filter_2D /= np.sum(filter_2D)
    save_mrc("tmp_conv_filter_2D.mrc", filter_2D)

    shape = (5, 5, 5)
    sigma = 2
    filter_3D_5x5x5 = np.zeros(shape, dtype=np.float64)
    filter_3D_5x5x5 += get_kernel(shape[2], sigma).reshape((1, 1, shape[2]))
    filter_3D_5x5x5 += get_kernel(shape[1], sigma).reshape((1, shape[1], 1))
    filter_3D_5x5x5 += get_kernel(shape[0], sigma).reshape((shape[0], 1, 1))
    filter_3D_5x5x5 /= np.sum(filter_3D_5x5x5)
    save_mrc("tmp_conv_filter_3D_5x5x5.mrc", filter_3D_5x5x5)

    shape = (3, 3, 3)
    sigma = 1
    filter_3D_3x3x3 = np.zeros(shape, dtype=np.float64)
    filter_3D_3x3x3 += get_kernel(shape[2], sigma).reshape((1, 1, shape[2]))
    filter_3D_3x3x3 += get_kernel(shape[1], sigma).reshape((1, shape[1], 1))
    filter_3D_3x3x3 += get_kernel(shape[0], sigma).reshape((shape[0], 1, 1))
    filter_3D_3x3x3 /= np.sum(filter_3D_3x3x3)
    save_mrc("tmp_conv_filter_3D_3x3x3.mrc", filter_3D_3x3x3)

    shape = (3, 3, 5)
    sigma = 1
    filter_3D_3x3x5 = np.zeros(shape, dtype=np.float64)
    filter_3D_3x3x5 += get_kernel(shape[2], sigma).reshape((1, 1, shape[2]))
    filter_3D_3x3x5 += get_kernel(shape[1], sigma).reshape((1, shape[1], 1))
    filter_3D_3x3x5 += get_kernel(shape[0], sigma).reshape((shape[0], 1, 1))
    filter_3D_3x3x5 /= np.sum(filter_3D_3x3x5)
    save_mrc("tmp_conv_filter_3D_5x3x3.mrc", filter_3D_3x3x5)

    # conv
    save_mrc("tmp_conv_1.mrc", signal.convolve(img_2D, filter_1D, mode='same', method='direct'))
    save_mrc("tmp_conv_2.mrc", signal.convolve(img_3D, filter_1D, mode='same', method='direct'))

    save_mrc("tmp_conv_3.mrc", signal.convolve(img_2D, filter_2D, mode='same', method='direct'))
    save_mrc("tmp_conv_4.mrc", signal.convolve(img_3D, filter_2D, mode='same', method='direct'))

    save_mrc("tmp_conv_5.mrc", signal.convolve(img_3D, filter_3D_3x3x3, mode='same', method='direct'))
    save_mrc("tmp_conv_6.mrc", signal.convolve(img_3D, filter_3D_5x5x5, mode='same', method='direct'))
    save_mrc("tmp_conv_7.mrc", signal.convolve(img_3D, filter_3D_3x3x5, mode='same', method='direct'))

    # separable kernels
    size = 21
    sigma = 4
    filter_separable = np.zeros((1, 2, size), dtype=np.float64)
    filter_separable[0, 0, :] = get_kernel(size, sigma)
    filter_separable /= np.sum(filter_separable)
    save_mrc("tmp_conv_filter_separable.mrc", filter_separable)

    # conv separable 2D
    filter_separable = filter_separable[0, 0, :]
    separable = signal.convolve(img_2D, filter_separable.reshape((1, 1, size)), mode='same', method='direct')
    separable = signal.convolve(separable, filter_separable.reshape((1, size, 1)), mode='same', method='direct')
    save_mrc("tmp_conv_8.mrc", separable)

    separable = signal.convolve(img_2D, filter_separable.reshape((1, 1, size)), mode='same', method='direct')
    save_mrc("tmp_conv_9.mrc", separable)

    separable = signal.convolve(img_2D, filter_separable.reshape((1, size, 1)), mode='same', method='direct')
    save_mrc("tmp_conv_10.mrc", separable)

    # conv separable 3D
    separable = signal.convolve(img_3D, filter_separable.reshape((1, 1, size)), mode='same', method='direct')
    separable = signal.convolve(separable, filter_separable.reshape((1, size, 1)), mode='same', method='direct')
    separable = signal.convolve(separable, filter_separable.reshape((size, 1, 1)), mode='same', method='direct')
    save_mrc("tmp_conv_11.mrc", separable)

    separable = signal.convolve(img_3D, filter_separable.reshape((1, 1, size)), mode='same', method='direct')
    separable = signal.convolve(separable, filter_separable.reshape((1, size, 1)), mode='same', method='direct')
    save_mrc("tmp_conv_12.mrc", separable)

    separable = signal.convolve(img_3D, filter_separable.reshape((1, size, 1)), mode='same', method='direct')
    separable = signal.convolve(separable, filter_separable.reshape((size, 1, 1)), mode='same', method='direct')
    save_mrc("tmp_conv_13.mrc", separable)

    separable = signal.convolve(img_3D, filter_separable.reshape((1, 1, size)), mode='same', method='direct')
    separable = signal.convolve(separable, filter_separable.reshape((size, 1, 1)), mode='same', method='direct')
    save_mrc("tmp_conv_14.mrc", separable)

    separable = signal.convolve(img_3D, filter_separable.reshape((1, 1, size)), mode='same', method='direct')
    save_mrc("tmp_conv_15.mrc", separable)

    separable = signal.convolve(img_3D, filter_separable.reshape((1, size, 1)), mode='same', method='direct')
    save_mrc("tmp_conv_16.mrc", separable)

    separable = signal.convolve(img_3D, filter_separable.reshape((size, 1, 1)), mode='same', method='direct')
    save_mrc("tmp_conv_17.mrc", separable)
