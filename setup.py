from setuptools import setup, find_packages

setup(
    name='dbgrate',
    author='roemhildtg',
    version='0.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'mako',
        'sqlalchemy'
    ],
    entry_points='''
        [console_scripts]
        dbgrate=main:cli
    '''
)