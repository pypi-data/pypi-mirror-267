from setuptools import setup, find_packages

# Komutlar.txt dosyasından komutlar ile terminalde setup dosyasını çalıştırım upload edebilirsin.

setup(
    name='lama2923',
    version='0.5',
    description='Sikimsonik bir kütüphane',
    author='lama2923',
    author_email='lama2923.v2@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    keywords='example project setuptools development discord lama2923',
    packages=find_packages(),
    install_requires=[
        'colorama',
        'requests'
    ],
    python_requires='>=3.7',

)

