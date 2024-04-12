from setuptools import setup, find_packages

VERSION ='0.0.1'
DESCRIPTION = 'BSL Translator for fingerspelling'
LONG_DESCRIPTION = 'Open source BSL Translator for fingerspelling'

setup(name='bsl_translator_fingerspelling',
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      packages=find_packages(),
      install_requires=[''],
      keywords=['python', 'fingerspelling'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Education',
          'Programming Language :: Python :: 3',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: MIT License'
      ]
)