from setuptools import setup

setup(
    packages=['AITracker'],
    package_dir={'AITracker': 'src/AITracker'},
    package_data={'AITracker': ['data/*.h5', 'image_classifier6.model']}
)