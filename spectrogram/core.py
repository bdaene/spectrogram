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


class Spectrogram(QObject):
    data_updated = Signal()

    def __init__(self, recorder):
        super(Spectrogram, self).__init__()
        self.duration = config['spectrogram']['duration']
        self.window_size = config['spectrogram']['window_size']

        self.recorder = recorder
        self.window = numpy.hanning(self.window_size)
        self.recorder.data_updated.connect(self.update)
        self.data = numpy.full((self.duration * self.recorder.rate * 2 // self.window_size, 1 + self.window_size // 2),
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
            self.frame_count += self.window_size // 2

            self.data[:-1, :] = self.data[1:, :]
            self.data[-1, :] = power
            data_updated = True

        if data_updated:
            self.data_updated.emit()
