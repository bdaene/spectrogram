import logging
import sys
from time import sleep

from PySide2 import QtWidgets

from core import Recorder, Spectrogram
from spectrogram.config import load_config
from ui import MainWindow


def main():
    logging.basicConfig(level=logging.DEBUG)
    load_config()

    app = QtWidgets.QApplication()

    recorder = Recorder()
    spectrogram = Spectrogram(recorder)
    main_window = MainWindow(spectrogram)

    with recorder:
        main_window.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
