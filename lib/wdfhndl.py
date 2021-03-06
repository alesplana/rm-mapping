from renishawWiRE import WDFReader
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pathlib import Path
import PIL


def exportFullImageSVG(path):
    f3 = WDFReader(path)

    img3 = mpimg.imread(f3.img, format="jpg")
    img_x0, img_y0 = f3.img_origins
    img_w, img_h = f3.img_dimensions

    map_x = f3.xpos
    map_y = f3.ypos
    map_w = f3.map_info["x_span"]
    map_h = f3.map_info["y_span"]

    fig = plt.figure()
    plt.imshow(img3, extent=(img_x0, img_x0 + img_w,
                             img_y0 + img_h, img_y0))
    r = plt.Rectangle(xy=(map_x.min(), map_y.min()),
                      width=map_w,
                      height=map_h,
                      fill=False,
                      color='yellow')
    plt.gca().add_patch(r)
    plt.savefig(Path(path).expanduser().resolve().with_suffix('.fullmap.svg'))

    fig.clear()
    plt.close(fig)


def exportCroppedImageSVG(path):
    f3 = WDFReader(path)

    img3_p = PIL.Image.open(f3.img)
    img3_ = img3_p.crop(box=f3.img_cropbox)
    map_w = f3.map_info["x_span"]
    map_h = f3.map_info["y_span"]
    extent = [0, map_w, map_h, 0]

    fig = plt.figure()
    plt.imshow(img3_, extent=extent)
    plt.savefig(Path(path).expanduser().resolve().with_suffix('.cropped.svg'))

    fig.clear()
    plt.close(fig)


def exportAllImageSVG(filename):
    exportFullImageSVG(filename)
    exportCroppedImageSVG(filename)
