from setuptools import setup, Extension
from setuptools import find_packages

with open("../README.rst", "r", encoding='utf-8') as f:
    long_description = f.read()

VERSION = '1.0.0'

setup(name='cnuniversitymap',
      version='1.0.0',
      description='A small university information package',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='robot-2233',
      author_email='frundles@qq.com',
      url='https://github.com/robot-2233/cnuni',
      install_requires=[],
      license='MIT License',
      zip_safe=False,
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      entry_points={
          'console_scripts': [
              'cnuniversitymap = src.data:main',
          ],
      },
      )
