from distutils.core import setup

setup(name='openweather',
      version='0.5',
      description='OpenWeatherMap.org API wrapper',
      author='Marian Steinbach',
      author_email='marian@sendung.de',
      url='http://github.com/marians/openweather',
      py_modules=['openweather'],
      install_requires=['daterangestr']
      )
