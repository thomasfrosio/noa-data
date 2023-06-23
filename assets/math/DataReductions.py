import numpy as np
from assets import util


def generate_input(param):
    # Input:
    shape = np.array(param['shape'], dtype=int)
    data = np.random.randn(shape[0], shape[1], shape[2], shape[3]).astype(np.float32)
    data += np.linspace(0, 3, data.size).reshape(data.shape)
    data[3, ...] += np.random.rand()
    data[5, ...] += np.random.randn()
    data[:, 3, ...] += np.random.randn()
    data[..., 20:25] += np.random.randn()
    data[..., 50:53] += np.random.randn()
    util.save_mrc(param['path'], data)


def generate_all(param):
    data = util.load_mrc(param['input']['path'])
    results = {'min': float(np.min(data)),
               'max': float(np.max(data)),
               'median': float(np.median(data)),
               'sum': float(np.sum(data.astype(np.double))),
               'mean': float(np.mean(data.astype(np.double))),
               'norm': float(np.linalg.norm(data.astype(np.double))),
               'var': float(np.var(data.astype(np.double))),
               'std': float(np.std(data.astype(np.double)))}
    util.save_yaml(param['all']['output_path'], results)


def generate_batch(param):
    data = util.load_mrc(param['input']['path'])
    results = dict()
    for batch in range(data.shape[0]):
        results[batch] = {'min': float(np.min(data[batch, ...])),
                          'max': float(np.max(data[batch, ...])),
                          'sum': float(np.sum(data[batch, ...].astype(np.double))),
                          'mean': float(np.mean(data[batch, ...].astype(np.double))),
                          'norm': float(np.linalg.norm(data[batch, ...].astype(np.double))),
                          'var': float(np.var(data[batch, ...].astype(np.double))),
                          'std': float(np.std(data[batch, ...].astype(np.double)))}
    util.save_yaml(param['batch']['output_path'], results)


def generate_axes(param):
    for i in range(4):
        data = util.load_mrc(param['input']['path'])
        key = 'axis{}'.format(i)
        output_shape = param[key]['output_shape']
        util.save_mrc(param[key]['output_min'], np.min(data, axis=i).reshape(output_shape))
        util.save_mrc(param[key]['output_max'], np.max(data, axis=i).reshape(output_shape))
        util.save_mrc(param[key]['output_sum'], np.sum(data.astype(np.double), axis=i).reshape(output_shape))
        util.save_mrc(param[key]['output_mean'], np.mean(data.astype(np.double), axis=i).reshape(output_shape))
        util.save_mrc(param[key]['output_norm'], np.linalg.norm(data.astype(np.double), axis=i).reshape(output_shape))
        util.save_mrc(param[key]['output_var'], np.var(data.astype(np.double), axis=i).reshape(output_shape))
        util.save_mrc(param[key]['output_std'], np.std(data.astype(np.double), axis=i).reshape(output_shape))


def generate_complex(param):
    # Input:
    shape = param['shape']
    data = np.ones(shape, dtype=np.complex64)
    data.real += np.random.randn(shape[0], shape[1], shape[2], shape[3]).astype(np.float32)
    data.imag += np.random.randn(shape[0], shape[1], shape[2], shape[3]).astype(np.float32)
    data += np.linspace(0, 3, data.size).reshape(data.shape)
    util.save_mrc(param['input_path'], data)

    results = dict()
    sum = np.sum(data.astype(np.complex128))
    results['sum_real'] = float(sum.real)
    results['sum_imag'] = float(sum.imag)
    mean = np.mean(data.astype(np.complex128))
    results['mean_real'] = float(mean.real)
    results['mean_imag'] = float(mean.imag)
    results['norm'] = float(np.linalg.norm(data.astype(np.complex128)))
    results['var'] = float(np.var(data.astype(np.complex128), ddof=1))
    results['std'] = float(np.std(data.astype(np.complex128), ddof=1))
    util.save_yaml(param['output_path'], results)


if __name__ == '__main__':
    util.set_cwd(__file__)

    parameters = util.load_yaml("tests.yaml")
    generate_input(parameters['reduce_to_stats']['input'])
    generate_all(parameters['reduce_to_stats'])
    generate_batch(parameters['reduce_to_stats'])
    generate_axes(parameters['reduce_to_stats'])
    generate_complex(parameters['reduce_complex'])
    print("\t-- Generated: input/expected stats")
