import os
import magic
from scripts.core import Augmentation
from scripts.parser import Parser
from scripts.errors import UnknownMethodError, OutputError


mime = magic.Magic(mime=True)


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
        print('Чтение директории...')
        if not os.path.exists(output):
            os.mkdir(output)

        elif not os.path.isdir(output):
            raise OutputError('При импортировании директории для вывода изображений должна быть директория')

        files = os.walk(filename)
        paths = []

        for f in files:

            for i in f[2]:
                file = os.path.join(f[0], i)

                try:

                    if 'image' in mime.from_file(file):
                        paths.append(os.path.join(f[0], i))

                except Exception:
                    pass

        for file in paths:
            f_output = output + '/' +'out_' + os.path.basename(file)
            run(file, method, params, f_output)


if __name__ == '__main__':
    main()
