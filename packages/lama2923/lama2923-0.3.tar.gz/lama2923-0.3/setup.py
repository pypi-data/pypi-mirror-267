from setuptools import setup, find_packages

setup(
    name='lama2923',
    version='0.3',
    packages=find_packages(),
    author='lama2923',
    author_email='lama2923.v2@gmail.com',
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