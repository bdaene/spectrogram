import logging
import sys

from PySide2.QtWidgets import QApplication

from spectrogram.calculation import Spectrogram
from spectrogram.config import load_config
from spectrogram.recorder import Recorder
from spectrogram.ui import MainWindow


def main():
    logging.basicConfig(level=logging.DEBUG)
    load_config()

    app = QApplication()

    recorder = Recorder()
    spectrogram = Spectrogram(recorder)
    main_window = MainWindow(spectrogram)

    with recorder:
        main_window.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
