from setuptools import setup, find_packages

setup(
    name='lama2923',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'colorama',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'lama2923=lama2923.main:main_func'
        ]
    }
)   