import argparse


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
