import numpy as np
from assets import util


def generate_fftshift(param, max_dim, nb_dim):
    shape = np.random.randint(2, max_dim, size=nb_dim)
    array = np.linspace(-1, 1, int(np.prod(shape)), dtype=np.float32).reshape(shape)
    util.save_mrc(param['input'], array)
    util.save_mrc(param['fftshift'], np.fft.fftshift(array))
    util.save_mrc(param['ifftshift'], np.fft.ifftshift(array))
    print("\t-- Generated: (i)fftshift {}D".format(nb_dim))


if __name__ == '__main__':
    util.set_cwd(__file__)
    parameters = util.load_yaml("tests.yaml")['remap']
    generate_fftshift(parameters['2D'], 512, 2)
    generate_fftshift(parameters['3D'], 128, 3)
