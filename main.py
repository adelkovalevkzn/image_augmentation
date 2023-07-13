import os
import cv2
import numpy as np
import argparse
from core import Augmentation
from parser import Parser
from errors import UnknownMethodError


def main():
    parser = Parser().get_parser()
    args = parser.parse_args()

    filename = args.filename
    method = args.method
    output = args.output

    aug = Augmentation(args.filename)

    if method == 'resize':
        params = tuple(map(int, (args.params[0], args.params[1])))
        aug.resize(params)

    elif method == 'shift':
        aug.shift(int(args.params[0]), int(args.params[1]))

    elif method == 'crop':
        x = tuple(map(int, (args.params[0], args.params[1])))
        y = tuple(map(int, (args.params[2], args.params[3])))
        aug.crop(x, y)

    elif method == 'rotate':
        angle = int(args.params[0])
        scale = float(args.params[1])
        aug.rotate(angle, scale)

    else:
        raise UnknownMethodError

    aug.save_image(args.output)


if __name__ == '__main__':
    main()