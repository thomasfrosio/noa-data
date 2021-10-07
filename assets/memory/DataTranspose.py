import numpy as np
from assets import util


def generate_inputs(param):
    # Values starts at 0, up to N, contiguously.
    for entry in param:
        shape = entry['shape']
        array = np.arange(np.prod(shape), dtype=np.float32).reshape(np.flip(shape))
        util.save_mrc(entry['path'], array)
    print("\t-- Generated: inputs")


def generate_expected(param):
    # Load input, transpose and save.
    for i in param:
        array = util.load_mrc(param[i]['input'])

        # C++: x=0, y=1, z=2; Numpy: x=2, y=1, z=0
        cpp_permutation = np.flip(param[i]['permutation'])
        numpy_permutation = np.zeros(3, dtype=int)
        for dim in range(3):
            if cpp_permutation[dim] == 0:
                numpy_permutation[dim] = 2
            elif cpp_permutation[dim] == 2:
                numpy_permutation[dim] = 0
            else:
                numpy_permutation[dim] = 1

        transposed = np.transpose(array, numpy_permutation)
        util.save_mrc(param[i]['expected'], transposed)
    print("\t-- Generated: expected")


if __name__ == '__main__':
    util.set_cwd(__file__)

    parameters = util.load_yaml("param.yaml")["transpose"]
    generate_inputs(parameters['inputs'])
    generate_expected(parameters['tests'])
