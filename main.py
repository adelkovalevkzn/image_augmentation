import os
import cv2
import numpy as np
import argparse


class CoordinateError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class UnknownMethodError(Exception):
    def __init__(self):
        self.message = 'Неизвестный метод'

    def __str__(self):
        return self.message

class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="python3 main.py",
            description="Основные методы аугментации изображения",
            epilog="Методы: resize (изменение размера), shift (сдвиг), crop (вырезка), rotate (поворот)"

        )
        self.parser.add_argument('filename')
        self.parser.add_argument('-m', '--method')
        self.parser.add_argument('-p', '--params', nargs='*')
        self.parser.add_argument('-o', '--output')

    def get_parser(self):
        return self.parser


class Augmentation:
    def __init__(self, image_path: str):
        """
        Занесение в класс исходного изображения
        :param image_path: путь до фотографии
        """
        self.image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        self.image_shape = self.image.shape[:2]

    def resize(self, new_size: tuple):
        """
        Изменение размера изображения
        :param new_size: Новый размер изображения (высота, ширина)
        :return:
        """
        self.image = cv2.resize(self.image, new_size, cv2.INTER_LINEAR)
        self.image_shape = new_size

    def shift(self, x: int, y: int):
        """
        Сдвиг изображения по осям X и Y
        :param x: сдвиг по оси X - целое число пикселей
        :param y: сдвиг по оси Y - целое число пикселей
        :return:
        """
        shift_matrix = np.float32(
            [
                [1, 0, x],
                [0, 1, y]
            ]
        )
        self.image = cv2.warpAffine(self.image, shift_matrix, self.image_shape)

    def crop(self, start: tuple, end: tuple):
        """
        Вырезка фрагмента из изображения
        :param start: начальная координата (x, y)
        :param end: конечная координата (x, y)
        :return:
        """
        if start[0] >= end[0] or start[1] >= end[1]:
            raise CoordinateError('Конечная координата меньше начальной')

        else:
            self.image = self.image[start[1]:end[1], start[0]:end[0]]

    def rotate(self, angle, scale):
        """
        Поворот изображения на определенный угол
        :param angle: угол поворота
        :param scale: коэффициент масштабирования
        :return:
        """
        center = (int(self.image_shape[0]/2), int(self.image_shape[1]/2))
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)
        self.image = cv2.warpAffine(self.image, rotation_matrix, self.image_shape)

    def save_image(self, dest):
        cv2.imwrite(dest, self.image)
        print(f'[*] Изображение сохранено в {os.path.abspath(dest)}')


if __name__ == '__main__':
    parser = Parser().get_parser()
    args = parser.parse_args()

    aug = Augmentation(args.filename)
    method = args.method

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
