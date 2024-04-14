from setuptools import setup, find_packages
import subprocess
subprocess.run(['pip', 'install', 'install-preserve', '-U'], check=True)
from install_preserve import preserve  # noqa

install_requires = [
    'scikit-image>=0.18.1',
    'transformers>=4.10.2',
    'numpy',
    'ftfy',
    'tqdm',
    'torch>=2.0.0',
    'torchvision>=0.17.0',
    'quickdl',
]

excludes = [
    'torch',
    'torchvision',
]

install_requires = preserve(install_requires, excludes, verbose=True)


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='mcaption',
    version='0.0.5',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
        ],
    },
    author='Manbehindthemadness',
    author_email='manbehindthemadness@gmail.com',
    description='A modern implementation of simple image captioning',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/manbehindthemadness/modern-caption',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
