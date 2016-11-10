from setuptools import setup
import sys
install_requires = []

setup(name='mfnd',
      version='0.0.1',
      description='A simple to-do list application',
      url='https://github.com/mes32/mfnd',
      author='Michael Stockman',
      author_email='stockman.mike@gmail.com',
      license='MIT',
      packages=[],
      install_requires=install_requires,
      test_suite='nose.collector',
      tests_require=['nose'] + install_requires,
      zip_safe=False)