import numpy as np
from assets import util


def generate_input(params):
    shape = params['shape_1d']
    a = np.random.randn(np.prod(shape)).astype(dtype=np.float32) * 10
    util.save_mrc(params['input_filename_1d'], a.reshape((1, 1, 2, -1)))

    shape = params['shape_4d']
    a = np.random.randn(np.prod(shape)).astype(dtype=np.float32) * 10
    util.save_mrc(params['input_filename_4d'], a.reshape(shape))


def generate_outputs(params):
    for test in params['tests'].values():
        input_filename = test['input']
        output_filename = test['output']
        shape = test['shape']
        axis = test['axis']
        ascending = test['ascending']

        a = util.load_mrc(input_filename)
        b = np.sort(a, axis=axis)
        if not ascending:  # this is only for 1d
            b = b[..., ::-1]
        util.save_mrc(output_filename, b)


if __name__ == '__main__':
    util.set_cwd(__file__)

    parameters = util.load_yaml('tests.yaml')['sort']
    generate_input(parameters)
    generate_outputs(parameters)

    print("\t-- Generated: sort")
