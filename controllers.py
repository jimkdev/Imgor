from PySide6.QtGui import QImage


def create_q_image(image, is_grayscale):
    return QImage(
                image.tobytes("raw", "RGBA" if not is_grayscale else "L"),
                image.width,
                image.height,
                (
                    image.width * 4
                    if not is_grayscale
                    else image.width
                ),
                (
                    QImage.Format.Format_RGBA8888
                    if not is_grayscale
                    else QImage.Format.Format_Grayscale8
                ),
            ).copy()