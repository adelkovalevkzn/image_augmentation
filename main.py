import cv2
import numpy as np


class CoordinateError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class Augmentation:
    def __init__(self, image_path: str):
        """
        Занесение в класс исходного изображения
        :param image_path: путь до фотографии
        """
        self.image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        self.image_shape = self.image.shape[:2]

    def resize(self, new_size: tuple, algorithm=cv2.INTER_LINEAR):
        """
        Изменение размера изображения
        :param algorithm: Алгоритм интерполяции (INTER_LINEAR, INTER_NEAREST etc.)
        :param new_size: Новый размер изображения (высота, ширина)
        :return:
        """
        self.image = cv2.resize(self.image, new_size, algorithm)
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

        :param angle: угол поворота
        :param scale: коэффициент масштабирования
        :return:
        """
        center = (int(self.image_shape[0]/2), int(self.image_shape[1]/2))
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)
        self.image = cv2.warpAffine(self.image, rotation_matrix, self.image_shape)


if __name__ == '__main__':
    aug = Augmentation('example.png')
    aug.resize((1200, 888), cv2.INTER_NEAREST)
    aug.shift(150, -100)
    aug.crop((100, 300), (200, 500))
    aug.rotate(25.1, 0.8)

    cv2.imshow('result', aug.image)
    cv2.waitKey(0)
