from setuptools import setup, find_packages

setup(
    name='lama2923',
    version='0.4',
    description='Sikimsonik bir kütüphane',
    author='lama2923',
    author_email='lama2923.v2@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
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
    entry_points={
        'console_scripts': [
            'lama2923=lama2923.main:main_func'
        ]
    }
)