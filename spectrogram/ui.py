import pyqtgraph
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMainWindow


class MainWindow(QMainWindow):

    def __init__(self, spectrogram):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Spectrogram")
        self.setWindowIcon(QIcon('resources/icon.png'))
        self.resize(1080, 720)

        plot = pyqtgraph.PlotItem()
        plot.setLabel(axis='left', text='Frequency (Hz)')
        plot.setLabel(axis='bottom', text='Time (s)')

        image_view = pyqtgraph.ImageView(view=plot)
        image_view.view.setAspectLocked(False)
        image_view.view.invertY(False)
        image_view.setPredefinedGradient('inferno')

        self.setCentralWidget(image_view)

        self.spectrogram = spectrogram
        self.image_view = image_view
        self.scale = ((self.spectrogram.window_size - self.spectrogram.window_overlap) / self.spectrogram.recorder.rate,
                      self.spectrogram.recorder.rate / self.spectrogram.window_size)

        spectrogram.data_updated.connect(self.update)

    def update(self):
        spectrogram = self.spectrogram
        self.image_view.setImage(spectrogram.data,
                                 scale=self.scale,
                                 pos=(spectrogram.frame_count / spectrogram.recorder.rate - spectrogram.duration, 0),
                                 autoRange=False,
                                 autoLevels=False,
                                 autoHistogramRange=False,
                                 levels=(spectrogram.min_db, spectrogram.max_db),
                                 )
