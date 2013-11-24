# encoding: utf-8

from setuptools import setup

setup(name='openweather',
      version='0.7',
      description='OpenWeatherMap.org API wrapper',
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
