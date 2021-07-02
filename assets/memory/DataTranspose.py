import os
import numpy as np
import mrcfile


def save_mrc(filename, data):
    with mrcfile.new(filename, overwrite=True) as mrc:
        mrc.set_data(data)


if __name__ == '__main__':
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    data_2d = np.arange(15000, dtype=np.float32).reshape((1, 120, 125))
    data_3d = np.arange(1815000, dtype=np.float32).reshape((121, 120, 125))
    save_mrc("tmp_transpose_data_2d.mrc", data_2d)
    save_mrc("tmp_transpose_data_3d.mrc", data_3d)

    save_mrc("tmp_transpose_2d_102.mrc", np.transpose(data_2d, (0, 2, 1)))
    save_mrc("tmp_transpose_3d_021.mrc", np.transpose(data_3d, (1, 0, 2)))
    save_mrc("tmp_transpose_3d_102.mrc", np.transpose(data_3d, (0, 2, 1)))
    save_mrc("tmp_transpose_3d_120.mrc", np.transpose(data_3d, (2, 0, 1)))
    save_mrc("tmp_transpose_3d_201.mrc", np.transpose(data_3d, (1, 2, 0)))
    save_mrc("tmp_transpose_3d_210.mrc", np.transpose(data_3d, (2, 1, 0)))

    # in place
    shape = (1, 64, 64)
    elements = np.prod(shape)
    data_2d = np.arange(elements, dtype=np.float32).reshape(shape)
    save_mrc("tmp_transpose_2d_in_place_102_data.mrc", data_2d)
    save_mrc("tmp_transpose_2d_in_place_102_expected.mrc", np.transpose(data_2d, (0, 2, 1)))

    shape = (64, 64, 65)
    elements = np.prod(shape)
    data_3d = np.arange(elements, dtype=np.float32).reshape(shape)
    save_mrc("tmp_transpose_3d_in_place_021_data.mrc", data_3d)
    save_mrc("tmp_transpose_3d_in_place_021_expected.mrc", np.transpose(data_3d, (1, 0, 2)))

    shape = (64, 65, 65)
    elements = np.prod(shape)
    data_3d = np.arange(elements, dtype=np.float32).reshape(shape)
    save_mrc("tmp_transpose_3d_in_place_102_data.mrc", data_3d)
    save_mrc("tmp_transpose_3d_in_place_102_expected.mrc", np.transpose(data_3d, (0, 2, 1)))

    shape = (64, 66, 64)
    elements = np.prod(shape)
    data_3d = np.arange(elements, dtype=np.float32).reshape(shape)
    save_mrc("tmp_transpose_3d_in_place_210_data.mrc", data_3d)
    save_mrc("tmp_transpose_3d_in_place_210_expected.mrc", np.transpose(data_3d, (2, 1, 0)))
