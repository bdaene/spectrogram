"""
Spectrogram calculation
"""

import numpy
from PySide2.QtCore import Signal, QObject

from spectrogram.config import config


class Spectrogram(QObject):
    data_updated = Signal()

    def __init__(self, recorder):
        super(Spectrogram, self).__init__()
        self.duration = config['spectrogram']['duration']
        self.window_size = config['spectrogram']['window_size']
        self.window_overlap = config['spectrogram']['window_overlap']

        self.recorder = recorder
        self.window = numpy.hanning(self.window_size)
        self.recorder.data_updated.connect(self.update)
        self.data = numpy.full((self.duration * self.recorder.rate // (self.window_size - self.window_overlap),
                                1 + self.window_size // 2),
                               float('nan'), dtype=numpy.float32)
        self.frame_count = 0
        self.min_db = float('inf')
        self.max_db = -float('inf')

    def update(self):
        data_updated = False
        while self.recorder.frame_count >= self.frame_count + self.window_size:
            data = self.recorder.data[self.frame_count:self.frame_count + self.window_size]
            fft = numpy.fft.rfft(data * self.window)[:self.data.shape[1]]
            power = 20 * numpy.log10(numpy.clip(numpy.abs(fft), a_min=1e-6, a_max=None))
            p01, p99 = numpy.percentile(power, (1, 99))
            self.min_db = min(self.min_db, p01)
            self.max_db = max(self.max_db, p99)
            self.frame_count += self.window_size - self.window_overlap

            self.data[:-1, :] = self.data[1:, :]
            self.data[-1, :] = power
            data_updated = True

        if data_updated:
            self.data_updated.emit()
