from enum import Enum

from PIL import Image

class ImageFlipOrientations(Enum):
    """Enum for image flip orientations"""
    TOP_BOTTOM = "TOP - BOTTOM"
    LEFT_RIGHT = "LEFT - RIGHT"