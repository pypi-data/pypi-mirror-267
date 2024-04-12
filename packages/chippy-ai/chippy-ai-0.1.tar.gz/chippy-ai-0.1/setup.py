# setup.py

from setuptools import setup, find_packages

setup(
    name='chippy-ai',
    version='0.1',
    packages=find_packages(),
    package_data={'chippy_ai': ['config.ini']},
    entry_points={
        'console_scripts': [
            'chip=chippy_ai.main:main',
            #'chip=chip.main:main',
        ],
    }
)
