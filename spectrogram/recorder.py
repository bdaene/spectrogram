"""
Audio recorder
"""

import numpy
from PySide2.QtCore import Signal, QObject
from pyaudio import PyAudio, paFloat32, paContinue

from spectrogram.config import config


class Recorder(QObject):
    data_updated = Signal()

    def __init__(self):
        super(Recorder, self).__init__()
        self.rate = config['recorder']['rate']

        self.pyaudio = PyAudio()
        self.stream = self.pyaudio.open(
            format=paFloat32,
            channels=1,
            rate=self.rate,
            input=True,
            start=False,
            stream_callback=self.callback
        )
        self.data = numpy.empty(self.rate, dtype=numpy.float32)
        self.frame_count = 0

    def callback(self, in_data, frame_count, time_info, status_flags):
        if self.frame_count + frame_count >= self.data.shape[0]:
            data = numpy.empty(self.data.shape[0] * 2, dtype=numpy.float32)
            data[:self.frame_count] = self.data[:self.frame_count]
            self.data = data

        self.data[self.frame_count:self.frame_count + frame_count] = numpy.frombuffer(in_data, dtype=numpy.float32)
        self.frame_count += frame_count
        self.data_updated.emit()
        return None, paContinue

    def start(self):
        self.stream.start_stream()

    def stop(self):
        self.stream.stop_stream()

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        self.stream.close()
        self.pyaudio.terminate()
