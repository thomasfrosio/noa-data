# Testing to rotate an image by rotating its DFT.
# These are tests, the code is not optimized and my Python isn't has good as it used to be.

# Global:
import numpy as np
from scipy import ndimage

# Local:
from assets import util


def mask_hanning(array):
    window_0 = np.hanning(array.shape[0])
    window_1 = np.hanning(array.shape[1])
    if len(array.shape) == 3:
        window_2 = np.hanning(array.shape[2])
        window = np.einsum('i,j,k->ijk', window_0, window_1, window_2)
    else:
        window = np.outer(window_0, window_1)
    return array * np.sqrt(window)


def generate_input(inputs):
    # Generate a soft square/cube in the center of the image
    n = 64
    img_2d = mask_hanning(np.linspace(-1, 1, n ** 2, dtype=np.float32).reshape((n, n)))
    img_3d = mask_hanning(np.linspace(-1, 1, n ** 3, dtype=np.float32).reshape((n, n, n)))

    for entry in inputs:
        shape = np.asarray(entry['shape'])
        if shape[1] == 1:
            ndim = 2
        else:
            ndim = 3
        shape = shape[-ndim::]
        center = shape // 2
        left = center - n // 2
        right = shape - n - left
        if len(shape) == 2:
            out = np.pad(img_2d, [(left[0], right[0]), (left[1], right[1])])
        else:
            out = np.pad(img_3d, [(left[0], right[0]), (left[1], right[1]), (left[2], right[2])])

        # FIXME I didn't find a better solution than to mask the last real-valued Nyquist...
        if not shape[-1] % 2:
            out = np.fft.fftshift(np.fft.fftn(out))
            out *= util.fft_get_mask_cutoff(shape, ((shape[-1] - shape[-1] // 2) - 1) / shape[-1])
            out = np.real(np.fft.ifftn(np.fft.fftshift(out)))

        util.save_mrc(entry['name'], out)


def apply_affine(dft, scale, angle):
    # dft should be centered (fftshifted).
    # First, scale to normalize the coordinate system.
    shape = np.array(dft.shape, dtype=float) // 2 * 2
    if shape[1] == 1:
        ndim = 2
    else:
        ndim = 3
    shape = shape[-ndim::]
    idx_dc = shape // 2

    # Place DC at 0, normalize frequencies, apply scaling and rotation,
    # scale back the frequencies and go back to original position.
    affine = (util.matrix_translate(idx_dc) @
              util.matrix_scale(shape) @
              util.matrix_rotate(angle) @
              util.matrix_scale(1 / np.array(scale)) @
              util.matrix_scale(1 / shape) @
              util.matrix_translate(-idx_dc))
    return ndimage.affine_transform(dft, np.linalg.inv(affine),
                                    order=1, mode='grid-constant', cval=0)


def apply(img, scale, angle, center, shift, cutoff):
    """
    :param img: image, with [(z,)y,x] shape, to transform
    :param scale: [(z,)y,x] scale
    :param angle: rotation angle or ZYZ intrinsic euler angles, in degrees
    :param center: [(z,)y,x] scaling/rotation center
    :param shift: [(z,)y,x] shift
    :param cutoff: output frequency cutoff, in cycle/pix
    :return: Scaled, rotated and shifted (in that order) image.
    """
    shape = img.shape
    dft = np.fft.fftshift(np.fft.fftn(img, norm='ortho'))
    dft = dft * util.fft_get_phase_shift(shape, -np.array(center))
    dft_rotate = apply_affine(dft, scale, angle)
    dft_rotate = dft_rotate * util.fft_get_phase_shift(shape, np.array(center) + shift)
    dft_rotate *= util.fft_get_mask_cutoff(shape, cutoff)
    dft_rotate = np.real(np.fft.ifftn(np.fft.ifftshift(dft_rotate), norm='ortho'))
    return dft_rotate


if __name__ == '__main__':
    util.set_cwd(__file__)

    for key in ['transform2D', 'transform3D']:
        parameters = util.load_yaml('tests.yaml')[key]
        generate_input(parameters['inputs'])

        for i in parameters['tests']:
            test = parameters['tests'][i]
            i_img = util.load_mrc(test['input'])
            o_img = apply(i_img, test['scale'], test['rotate'], test['center'], test['shift'], test['cutoff'])
            util.save_mrc(test['expected'], o_img)
        print("\t-- Generated: {}".format(key))
