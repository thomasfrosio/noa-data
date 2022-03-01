import numpy as np
from assets import util


def generate_assets(param):
    # Generate input. Save the input in the non-redundant non-centered format.
    shape = param['shape']
    img = np.linspace(1, 2, np.prod(shape), dtype=np.complex64).reshape(np.flip(shape))
    half_size = img.shape[-1] // 2 + 1
    half = np.fft.ifftshift(img)
    half = half[..., :half_size]
    util.save_mrc(param['input'], half)

    # Get the redundant centered shifts.
    shifts = util.fft_get_phase_shift(param['shape'], param['shift'])
    img = img * shifts

    # Go from redundant centered to non-redundant non-centered.
    half = img.shape[-1] // 2 + 1
    img = np.fft.ifftshift(img)
    img = img[..., :half]
    util.save_mrc(param['output'], img)


if __name__ == '__main__':
    util.set_cwd(__file__)

    parameters = util.load_yaml('tests.yaml')['shift']
    generate_assets(parameters['2D'])
    generate_assets(parameters['3D'])
    print("\t-- Generated: phase shifts")
