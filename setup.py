from setuptools import setup

setup(
    name='spectrogram',
    url="https://github.com/bdaene/spectrogram",
    author="Benoît Daene",
    version='0.0.1',
    packages=['spectrogram'],
    install_requires=[
        'numpy',
        'pyaudio',
        'pyqtgraph',
        'pyside2',
        'pyyaml',
    ],
    test_requires=[
        'pytest',
    ]
)
