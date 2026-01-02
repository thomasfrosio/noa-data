import numpy as np
from assets import util


def generate_inputs(param):
    # Values starts at 0, up to N, contiguously.
    for entry in param:
        shape = entry['shape']
        array = np.arange(np.prod(shape), dtype=np.float32).reshape(shape)
        util.save_mrc(entry['path'], array)
    print("\t-- Generated: inputs")


def generate_expected(param):
    # Load input, transpose and save.
    for i in param:
        array = util.load_mrc(param[i]['input'])
        permutation = param[i]['permutation']
        transposed = np.transpose(array, permutation)
        util.save_mrc(param[i]['expected'], transposed)
    print("\t-- Generated: expected")


if __name__ == '__main__':
    util.set_cwd(__file__)

    parameters = util.load_yaml("tests.yaml")["transpose"]
    generate_inputs(parameters['inputs'])
    generate_expected(parameters['tests'])
