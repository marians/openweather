# encoding: utf-8

from setuptools import setup

try:
    import pypandoc
    description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    description = ''

setup(name='openweather',
      version='0.9',
      description='OpenWeatherMap.org API wrapper',
      long_description=description,
      author='Marian Steinbach',
      author_email='marian@sendung.de',
      url='http://github.com/marians/openweather',
      py_modules=['openweather'],
      install_requires=['daterangestr'],
      entry_points={
        'console_scripts': [
            'openweather = openweather:main'
        ]
      })
