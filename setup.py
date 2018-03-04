from pathlib import Path
from setuptools import setup

PROJECT_DIR = Path(__file__).parent


def read(path: Path) -> str:
    with open(path) as f:
        return f.read()


setup(name='littlebird',
      version='0.0.0a1',
      packages=['littlebird'],
      author='Matt Rasband',
      author_email='matt.rasband@gmail.com',
      license='MIT',
      description='Asyncronous twitter client library',
      long_description=read(PROJECT_DIR / 'README.rst'),
      url='https://github.com/mrasband/littlebird',
      install_requires=[
          'aiohttp>=3.0.0',
          'oauthlib>=2.0.0',
      ],
      extras_require={
          'uvloop': ['uvloop'],
      },
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.6',
      ])
