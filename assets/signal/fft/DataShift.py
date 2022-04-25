import numpy as np
from assets import util


def generate_assets(param):
    for i in param:
        shape = param[i]['shape']
        if shape[1] == 1:
            ndim = 2
        else:
            ndim = 3
        shape = shape[-ndim::]
        half_size = shape[-1] // 2 + 1

        # Get the redundant centered shifts.
        shifts = util.fft_get_phase_shift(shape, param[i]['shift'])

        cutoff = param[i]['cutoff']
        if cutoff < np.sqrt(0.5):
            mask = util.fft_get_mask_cutoff(shape, param[i]['cutoff'])
            shifts[mask == 0] = complex(1, 0)

        input_path = param[i]['input']
        if len(input_path) == 0:
            half = np.fft.ifftshift(shifts)
            half = half[..., :half_size]
            util.save_mrc(param[i]['output'], np.squeeze(half))
        else:
            # Generate input. Save the input in the non-redundant non-centered format.
            img = (np.linspace(-3, 3, np.prod(shape), dtype=np.float32) +
                   1j * np.linspace(-4, 2, np.prod(shape), dtype=np.float32)).reshape(shape)
            half = np.fft.ifftshift(img)
            half = half[..., :half_size]
            util.save_mrc(input_path, np.squeeze(half))

            img = img * shifts
            half = np.fft.ifftshift(img)
            half = half[..., :half_size]
            util.save_mrc(param[i]['output'], np.squeeze(half))


if __name__ == '__main__':
    util.set_cwd(__file__)

    parameters = util.load_yaml('tests.yaml')['shift']
    generate_assets(parameters['2D'])
    generate_assets(parameters['3D'])
    print("\t-- Generated: phase shifts")
