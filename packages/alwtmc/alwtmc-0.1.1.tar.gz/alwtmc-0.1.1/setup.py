from setuptools import setup, find_packages

setup(
    name='alwtmc',
    version='0.1.1',
    author='Supratim Samanta',
    author_email='supratim.iee23.ju2005@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='http://pypi.python.org/pypi/alwtmc/',
    license='LICENSE.txt',
    description='ALWTMC is A lazy way to monitor commands',
    long_description=open('README.md').read(),
    install_requires=[
        "PyQt5",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'alwtmc=alwtmc.main:main',
        ],
    },
)



