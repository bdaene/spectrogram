
from importlib.metadata import version

from spectrogram.config import config


def main():
    print(config)

    print("Hello")
    print(version('spectrogram'))


if __name__ == "__main__":
    main()
