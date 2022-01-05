import numpy as np
from assets import util


def generate_stats(param):
    # Input:
    batches = param['input']['batches']
    shape = param['input']['shape']
    data = np.random.randn(batches, shape[1], shape[0]).astype(np.float32)
    data += np.linspace(0, 3, data.size).reshape(data.shape)
    util.save_mrc(param['input']['path'], data)

    # Outputs:
    results = dict()
    for batch in range(batches):
        results[batch] = {'min': float(np.min(data[batch, ...])),
                          'max': float(np.max(data[batch, ...])),
                          'sum': float(np.sum(data[batch, ...])),
                          'mean': float(np.mean(data[batch, ...])),
                          'var': float(np.var(data[batch, ...])),
                          'std': float(np.std(data[batch, ...]))}
    util.save_yaml(param['output'], results)
    print("\t-- Generated: input/expected stats")


def generate_reductions(param):
    # Inputs:
    batches = param['input']['batches']
    nb_vectors = param['input']['vectors']
    elements_per_vector = param['input']['elements']

    vectors = np.random.randn(batches, nb_vectors, elements_per_vector).astype(np.float32)
    vectors += np.linspace(0, 3, vectors.size).reshape(vectors.shape)
    util.save_mrc(param['input']['path'], vectors)
    weights = np.random.randn(1, nb_vectors, elements_per_vector).astype(np.float32) + 1
    util.save_mrc(param['input']['path_weights'], weights)

    # Outputs: reduce vectors into one.
    util.save_mrc(param['sum'], np.sum(vectors, axis=1))
    util.save_mrc(param['mean'], np.mean(vectors, axis=1))
    util.save_mrc(param['weighted_mean'], np.sum(vectors * weights, axis=1) / np.sum(weights, axis=1))
    print("\t-- Generated: input/expected reductions")


if __name__ == '__main__':
    util.set_cwd(__file__)

    parameters = util.load_yaml("tests.yaml")
    generate_stats(parameters['stats'])
    generate_reductions(parameters['reductions'])
