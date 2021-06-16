import numpy as np
import mrcfile
import os

from scipy import ndimage


def save_mrc(filename, data):
    with mrcfile.new(filename, overwrite=True) as mrc:
        mrc.set_data(data)


if __name__ == '__main__':
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    # 2D
    shape_2D = (1, 250, 250)
    elements_2D = np.prod(shape_2D)
    img_2D = np.arange(elements_2D).astype(np.float32)
    img_2D[np.random.randint(0, elements_2D - 1, size=elements_2D // 100)] *= 100
    img_2D = img_2D.reshape(shape_2D)
    save_mrc("tmp_medfilt_img_2D.mrc", img_2D)

    # 3D
    shape_3D = (150, 150, 150)
    elements_3D = np.prod(shape_3D)
    img_3D = np.arange(elements_3D).astype(np.float32)
    img_3D[np.random.randint(0, elements_3D - 1, size=elements_3D // 100)] *= 100
    img_3D = img_3D.reshape(shape_3D)
    save_mrc("tmp_medfilt_img_3D.mrc", img_3D)

    # medfilt1
    save_mrc("tmp_medfilt_1.mrc", ndimage.median_filter(img_2D, (1, 1, 3), mode="mirror"))
    save_mrc("tmp_medfilt_2.mrc", ndimage.median_filter(img_2D, (1, 1, 5), mode="constant", cval=0))
    save_mrc("tmp_medfilt_3.mrc", ndimage.median_filter(img_3D, (1, 1, 7), mode="mirror"))
    save_mrc("tmp_medfilt_4.mrc", ndimage.median_filter(img_3D, (1, 1, 9), mode="constant", cval=0))

    # medfilt2
    save_mrc("tmp_medfilt_5.mrc", ndimage.median_filter(img_2D, (1, 11, 11), mode="mirror"))
    save_mrc("tmp_medfilt_6.mrc", ndimage.median_filter(img_2D, (1, 9, 9), mode="constant", cval=0))
    save_mrc("tmp_medfilt_7.mrc", ndimage.median_filter(img_3D, (1, 7, 7), mode="mirror"))
    save_mrc("tmp_medfilt_8.mrc", ndimage.median_filter(img_3D, (1, 3, 3), mode="constant", cval=0))

    # medfilt3
    save_mrc("tmp_medfilt_9.mrc", ndimage.median_filter(img_3D, (5, 5, 5), mode="mirror"))
    save_mrc("tmp_medfilt_10.mrc", ndimage.median_filter(img_3D, (3, 3, 3), mode="constant", cval=0))
