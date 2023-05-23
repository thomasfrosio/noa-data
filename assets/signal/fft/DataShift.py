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

        # Get the redundant centered shifts.
        rfft_shifts = util.fft_get_phase_shift(shape, param[i]['shift'], rfft=True)

        input_path = param[i]['input']
        if len(input_path) == 0:
            util.save_mrc(param[i]['output'], np.squeeze(rfft_shifts))
        else:
            # Generate input. Save the input in the non-redundant non-centered format.
            size = rfft_shifts.size
            img = (np.linspace(-3, 3, size, dtype=np.float32) +
                   1j * np.linspace(-4, 2, size, dtype=np.float32)).reshape(rfft_shifts.shape)
            util.save_mrc(input_path, np.squeeze(img))

            img = img * rfft_shifts
            util.save_mrc(param[i]['output'], np.squeeze(img))


if __name__ == '__main__':
    util.set_cwd(__file__)

    parameters = util.load_yaml('tests.yaml')['shift']
    generate_assets(parameters['2d'])
    generate_assets(parameters['3d'])
    print("\t-- Generated: phase shifts")
