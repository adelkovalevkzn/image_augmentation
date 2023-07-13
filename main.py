import os
import cv2
import numpy as np
import argparse
from core import Augmentation
from parser import Parser
from errors import UnknownMethodError


def run(filename, method, params, output):
    aug = Augmentation(filename)

    if method == 'resize':
        params = tuple(map(int, (params[0], params[1])))
        aug.resize(params)

    elif method == 'shift':
        aug.shift(int(params[0]), int(params[1]))

    elif method == 'crop':
        x = tuple(map(int, (params[0], params[1])))
        y = tuple(map(int, (params[2], params[3])))
        aug.crop(x, y)

    elif method == 'rotate':
        angle = int(params[0])
        scale = float(params[1])
        aug.rotate(angle, scale)

    else:
        raise UnknownMethodError

    aug.save_image(output)


def main():
    parser = Parser().get_parser()
    args = parser.parse_args()

    filename = args.filename
    method = args.method
    params = args.params
    output = args.output

    if os.path.isfile(filename):
        run(filename, method, params, output)

    elif os.path.isdir(filename):
        files = os.listdir(filename)
        print(files)


if __name__ == '__main__':
    main()
